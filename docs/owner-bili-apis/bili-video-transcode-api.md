# 视频转码状态查询

## 接口描述

查询指定视频稿件的转码状态，包含各清晰度（360P、480P、720P、1080P、1080P+60帧等）的转码进度和结果。

> 该接口位于创作中心域名 `member.bilibili.com`，用于UP主查看视频上传后的转码处理状态。

---

## 接口地址

```
GET https://member.bilibili.com/x/web/detail/xcode
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
| cid          | num  | 视频 CID   | **必要** | 视频分 P 的 CID    |
| web_location | str  | 来源标识   | 非必要   | 固定传 `0.0`       |

**示例请求 URL：**

```
https://member.bilibili.com/x/web/detail/xcode?bvid=BV1JXNgzxE3P&cid=36550019278&web_location=0.0
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

| 字段                | 类型  | 内容               | 备注         |
| ------------------- | ----- | ------------------ | ------------ |
| cid                 | num   | 视频 CID           |              |
| xcode_tip           | str   | 转码提示信息       | 通常为空     |
| fail_tip            | str   | 失败提示信息       | 通常为空     |
| xcode_state         | num   | 整体转码状态       | 2：转码完成  |
| transcode_list      | array | 各清晰度转码详情   |              |
| xcode_begin_at      | num   | 转码开始时间戳     | 0 表示未开始 |
| max_estimate_time   | num   | 最大预估时间       | 0 表示已完成 |
| max_estimate_end_at | num   | 最大预估结束时间戳 | 0 表示已完成 |

### `transcode_list` 数组元素

| 字段           | 类型 | 内容               | 备注                                                        |
| -------------- | ---- | ------------------ | ----------------------------------------------------------- |
| resolution     | str  | 清晰度名称         | 如 `"360P 流畅"`、`"1080P 60帧"`                            |
| status         | str  | 转码状态           | `"success"`：成功，`"processing"`：处理中，`"failed"`：失败 |
| estimated_time | num  | 预估剩余时间（秒） | 0 表示已完成                                                |
| completed_at   | num  | 完成时间戳         | 0 表示未完成                                                |
| start_time     | num  | 开始时间戳         | 0 表示未开始                                                |
| time_now       | num  | 当前时间戳         | Unix 时间戳（秒）                                           |
| failure_reason | str  | 失败原因           | 成功时为空                                                  |

---

## 转码状态说明（`status`）

| 状态         | 含义     | 备注                  |
| ------------ | -------- | --------------------- |
| `success`    | 转码成功 | 该清晰度可播放        |
| `processing` | 转码中   | 需等待                |
| `failed`     | 转码失败 | 查看 `failure_reason` |

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
curl 'https://member.bilibili.com/x/web/detail/xcode?bvid=BV1JXNgzxE3P&cid=36550019278&web_location=0.0' \
  -H 'Referer: https://member.bilibili.com/' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限 UP 主**：该接口只能查询当前用户自己稿件的转码状态。
3. **`xcode_state`**：`2` 表示所有清晰度均已转码完成。
4. **清晰度列表动态**：返回的 `transcode_list` 仅包含视频实际拥有的清晰度，并非固定列表。例如，原视频没有 4K 画质时，列表中不会包含 `"4K 超清"`。
5. **`cid` 获取**：可通过视频信息接口 `/x/web-interface/view` 获取。
