"""B 站新版接口层单元测试：WBI 签名（官方向量）、请求体构造、错误映射。"""

from __future__ import annotations

import unittest

import httpx

from bxbot.pipeline import BiliContentRejected, BiliRiskError
from bxbot.publishers.bilibili.dyn_api import (
    BiliApiError,
    BiliDynClient,
    build_content,
    build_create_dyn_body,
    build_pics,
    build_submit_check_body,
    make_upload_id,
)
from bxbot.publishers.bilibili.wbi import get_mixin_key, sign_params


class TestWbi(unittest.TestCase):
    def test_mixin_key_vector_1(self):
        # wbi.md 文档示例：img+sub → mixin_key
        self.assertEqual(
            get_mixin_key(
                "7cd084941338484aae1ad9425b84077c4932caff0ff746eab6f01bf08b70ac45"
            ),
            "ea1db124af3c7062474693fa704f4ff8",
        )

    def test_mixin_key_vector_2(self):
        # Java 示例：img=653657… sub=6e4909… → 72136226c6a73669787ee4fd02a74c27
        self.assertEqual(
            get_mixin_key(
                "653657f524a547ac981ded72ea1720576e4909c702f846728e64f6007736a338"
            ),
            "72136226c6a73669787ee4fd02a74c27",
        )

    def test_sign_deterministic_and_sorted(self):
        signed = sign_params(
            {"foo": "114", "bar": "514", "baz": 1919810},
            img_key="a" * 32,
            sub_key="b" * 32,
            wts=1702204169,
        )
        self.assertEqual(int(signed["wts"]), 1702204169)
        self.assertIn("w_rid", signed)
        self.assertEqual(len(signed["w_rid"]), 32)
        # 同参数同时间戳 → 同签名
        again = sign_params(
            {"foo": "114", "bar": "514", "baz": 1919810},
            img_key="a" * 32,
            sub_key="b" * 32,
            wts=1702204169,
        )
        self.assertEqual(signed["w_rid"], again["w_rid"])

    def test_sign_filters_special_chars(self):
        signed = sign_params(
            {"foo": "one!one'four*", "bar": "五一四"},
            img_key="a" * 32,
            sub_key="b" * 32,
            wts=100,
        )
        self.assertNotIn("!", signed["foo"])
        self.assertNotIn("'", signed["foo"])
        self.assertNotIn("*", signed["foo"])


class TestBodyBuilders(unittest.TestCase):
    def test_content(self):
        c = build_content("你好", title="t")
        self.assertEqual(c["contents"][0]["raw_text"], "你好")
        self.assertEqual(c["contents"][0]["type"], 1)
        self.assertEqual(c["title"], "t")

    def test_upload_id_format(self):
        uid = make_upload_id(12345, ts=1700000000, rnd=7788)
        self.assertEqual(uid, "12345_1700000000_7788")

    def test_submit_check_body_text(self):
        body = build_submit_check_body(build_content("hi"), aigc_flag=2)
        self.assertEqual(body["scene"], 2)
        self.assertIsNone(body["attach_card"])
        self.assertEqual(body["option"]["aigc"], 2)
        self.assertNotIn("pics", body)

    def test_submit_check_body_with_pics(self):
        pics = build_pics(
            [
                {
                    "img_src": "http://x/1.jpg",
                    "img_width": 1,
                    "img_height": 2,
                    "img_size": 3.5,
                }
            ]
        )
        body = build_submit_check_body(build_content("hi"), pics=pics, aigc_flag=0)
        self.assertEqual(body["pics"][0]["img_src"], "http://x/1.jpg")
        self.assertEqual(body["create_option"]["pic_mode"], 0)

    def test_create_dyn_body(self):
        pics = build_pics([{"img_src": "http://x/1.jpg"}])
        body = build_create_dyn_body(build_content("hi"), upload_id="1_2_3", pics=pics)
        dyn = body["dyn_req"]
        self.assertEqual(dyn["upload_id"], "1_2_3")
        self.assertEqual(dyn["meta"]["app_meta"]["from"], "create.dynamic.web")
        self.assertIn("pics", dyn)
        self.assertIn("option", dyn)

    def test_create_dyn_body_text(self):
        body = build_create_dyn_body(build_content("hi"), upload_id="1_2_3")
        dyn = body["dyn_req"]
        self.assertNotIn("pics", dyn)
        self.assertEqual(dyn["option"]["private_pub"], 0)


class TestErrorMapping(unittest.TestCase):
    def _resp(self, payload: dict) -> httpx.Response:
        return httpx.Response(200, json=payload)

    def _client(self) -> BiliDynClient:
        return BiliDynClient({"SESSDATA": "s", "bili_jct": "j"}, mid="1")

    def test_ok_passthrough(self):
        c = self._client()
        payload = c._check(self._resp({"code": 0, "data": {"x": 1}}), context="t")
        self.assertEqual(payload["data"]["x"], 1)

    def test_risk_codes_raise_bili_risk(self):
        c = self._client()
        for code in (-403, -412, -352, -799):
            with self.assertRaises(BiliRiskError):
                c._check(self._resp({"code": code, "message": "拦截"}), context="t")

    def test_other_codes_raise_api_error(self):
        c = self._client()
        with self.assertRaises(BiliApiError) as cm:
            c._check(
                self._resp({"code": -111, "message": "CSRF 校验失败"}), context="t"
            )
        self.assertEqual(cm.exception.code, -111)
        self.assertNotIsInstance(cm.exception, BiliRiskError)

    def test_content_rejected_is_not_risk(self):
        # submit_check 的内容拒绝走 BiliContentRejected（由 dyn_api.submit_check 抛出）
        self.assertFalse(issubclass(BiliContentRejected, BiliRiskError))


if __name__ == "__main__":
    unittest.main()
