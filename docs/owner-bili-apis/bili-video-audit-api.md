# 视频稿件审核状态查询

## 接口描述

查询指定视频稿件的审核状态，包含审核进度、驳回原因、侵权投诉详情等。

> 该接口位于创作中心域名 `member.bilibili.com`，用于UP主查看稿件审核结果和驳回原因。

---

## 接口地址

```
GET https://member.bilibili.com/x/web/detail/audit
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容       | 必要性   | 备注               |
| ------------ | ---- | ---------- | -------- | ------------------ |
| bvid         | str  | 视频 BV ID | **必要** | 要查询的稿件 BV 号 |
| web_location | str  | 来源标识   | 非必要   | 固定传 `0.0`       |

**示例请求 URL：**

```
https://member.bilibili.com/x/web/detail/audit?bvid=BV1JXNgzxE3P&web_location=0.0
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 |            |

### `data` 对象

| 字段               | 类型     | 内容             | 备注                  |
| ------------------ | -------- | ---------------- | --------------------- |
| aid                | num      | 视频 AV ID       |                       |
| state              | num      | 稿件审核状态码   | 见下方状态码表        |
| aegis_state        | num      | 风控状态         |                       |
| audit_process      | null/obj | 审核进度信息     | 通常为 null           |
| political_editable | num      | 政治内容可编辑   | 0：否                 |
| political_media    | num      | 政治相关媒体     | 0：否                 |
| is_interactive     | num      | 是否互动视频     | 0：否                 |
| appeal             | obj      | 申诉信息         |                       |
| problem_detail     | array    | 问题详情列表     | 驳回/侵权时的详细信息 |
| limited_open       | num      | 限制开放状态     |                       |
| app_appeal_url     | str      | APP端申诉链接    |                       |
| app_appeal_state   | num      | APP端申诉状态    |                       |
| state_panel        | num      | 状态面板类型     |                       |
| is_owner           | bool     | 是否为稿件所有者 |                       |

### `appeal` 对象

| 字段      | 类型 | 内容         | 备注  |
| --------- | ---- | ------------ | ----- |
| open_apid | num  | 是否开启申诉 | 0：否 |
| reject    | str  | 拒绝原因     |       |
| jump_url  | str  | 跳转链接     |       |

### `problem_detail` 数组元素

| 字段                      | 类型  | 内容             | 备注              |
| ------------------------- | ----- | ---------------- | ----------------- |
| type                      | str   | 问题类型         | `"archive"`：稿件 |
| reject_reason             | str   | 驳回原因描述     | 如侵权投诉说明    |
| reject_reason_url         | str   | 驳回原因详情链接 |                   |
| modify_advise             | str   | 修改建议         |                   |
| problem_description       | str   | 问题描述         |                   |
| problem_description_title | str   | 问题描述标题     |                   |
| reject_reason_id          | num   | 驳回原因 ID      |                   |
| picture_data              | array | 图片数据         |                   |
| reject_video_explain      | obj   | 驳回视频说明     |                   |
| index                     | num   | 索引             |                   |
| violation_time            | str   | 违规时间         |                   |
| violation_position        | str   | 违规位置         |                   |

---

## 稿件状态码（`state`）

| 状态码 | 含义     | 备注                                       |
| ------ | -------- | ------------------------------------------ |
| -4     | 审核驳回 | 稿件被拒绝，查看 `problem_detail` 获取原因 |
| 0      | 审核中   | 等待审核                                   |
| 1      | 审核通过 | 稿件已发布                                 |
| 其他   | 待补充   |                                            |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "aid": 116192907956253,
        "state": -4,
        "aegis_state": 4,
        "audit_process": null,
        "political_editable": 0,
        "political_media": 0,
        "is_interactive": 0,
        "appeal": {
            "open_apid": 0,
            "reject": "",
            "jump_url": ""
        },
        "problem_detail": [
            {
                "type": "archive",
                "reject_reason": "收到权利人秦皇岛易数科技有限公司就《DiskGenius》关于您稿件的侵权投诉并根据其要求及著作权法等相关法律规定对该稿件进行下线处理",
                "reject_reason_url": "https://member.bilibili.com/platform/convention/content?index=2-1&navhide=1",
                "modify_advise": "建议在获得权利人授权许可后，使用相关素材进行创作。\n如您认为您的稿件不侵权，可通过【创作中心-内容管理-稿件管理】途径提出恢复申请并提交不侵权声明及相关证明材料。",
                "problem_description": "",
                "problem_description_title": "",
                "reject_reason_id": 2920317,
                "picture_data": [],
                "reject_video_explain": {
                    "title": "",
                    "link": {
                        "web": "",
                        "app": ""
                    }
                },
                "index": 0,
                "violation_time": "",
                "violation_position": ""
            }
        ],
        "limited_open": 0,
        "app_appeal_url": "",
        "app_appeal_state": 0,
        "state_panel": 3,
        "is_owner": true
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://member.bilibili.com/x/web/detail/audit?bvid=BV1JXNgzxE3P&web_location=0.0' \
  -H 'Referer: https://member.bilibili.com/' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限 UP 主**：该接口只能查询当前用户自己稿件的审核状态。
3. **`state=-4`**：表示稿件被驳回，此时 `problem_detail` 中会包含详细的驳回原因和修改建议。
4. **侵权投诉**：当稿件因侵权被驳回时，`reject_reason` 会显示权利人的投诉信息。
5. **申诉入口**：部分驳回情况可通过 `appeal.jump_url` 发起申诉。


### 📂 创作中心模块文件清单

| 文件                          | 内容                     |
| ----------------------------- | ------------------------ |
| `bili-assist-list-api.md`     | UP主协管员（骑士团）列表 |
| `bili-assist-set-api.md`      | UP主协管员权限设置       |
| `bili-assist-add-api.md`      | UP主协管员添加           |
| `bili-assist-del-api.md`      | UP主协管员移除           |
| `bili-video-transcode-api.md` | 视频转码状态查询         |
| `bili-video-audit-api.md`     | 视频稿件审核状态查询     |
