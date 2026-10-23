# 获取私信消息列表

## 接口描述

获取当前用户与指定联系人的私信消息记录。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于私信会话页面展示历史消息。**该接口需要 WBI 签名。**


## 接口地址

```
GET https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：✅ 需要


## 请求参数（URL Query）

| 参数名             | 类型    | 内容         | 必要性   | 备注                 |
| ------------------ | ------- | ------------ | -------- | -------------------- |
| `size`             | num     | 拉取消息数量 | **必要** | 每页条数             |
| `session_type`     | num     | 会话类型     | **必要** | `1`：私聊            |
| `talker_id`        | num     | 对话方 UID   | **必要** | 对方的用户 ID        |
| `begin_seqno`      | str/num | 起始消息序号 | **必要** | 从该序号开始往前拉取 |
| `end_seqno`        | str/num | 结束消息序号 | 非必要   | 默认为空             |
| `sender_device_id` | num     | 发送设备 ID  | 非必要   | 固定传 `1`           |
| `build`            | num     | 构建版本     | 非必要   | 固定传 `0`           |
| `mobi_app`         | str     | 平台标识     | 非必要   | `web`                |
| `web_location`     | str     | 来源标识     | 非必要   | `0.0`                |
| `w_rid`            | str     | WBI 签名     | **必要** | 见 WBI 签名算法      |
| `wts`              | num     | WBI 时间戳   | **必要** | 秒级 Unix 时间戳     |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `msg`     | str  | 状态信息 | `"0"`      |
| `message` | str  | 状态信息 | `"0"`      |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段        | 类型    | 内容           | 备注             |
| ----------- | ------- | -------------- | ---------------- |
| `messages`  | array   | 消息列表       | 按时间倒序排列   |
| `has_more`  | num     | 是否有更多消息 | `0`：无，`1`：有 |
| `min_seqno` | str/num | 当前页最小序号 | 用于翻页         |
| `max_seqno` | str/num | 当前页最大序号 | 用于翻页         |

### `messages` 数组元素

| 字段            | 类型    | 内容                    | 备注                     |
| --------------- | ------- | ----------------------- | ------------------------ |
| `sender_uid`    | num     | 发送者 UID              |                          |
| `receiver_type` | num     | 接收者类型              | `1`：用户                |
| `receiver_id`   | num     | 接收者 UID              |                          |
| `msg_type`      | num     | 消息类型                | `1`：文本消息            |
| `content`       | str     | 消息内容（JSON 字符串） | 需 JSON 解析获取实际文本 |
| `msg_seqno`     | str/num | 消息序号                | 全局唯一                 |
| `timestamp`     | num     | 发送时间戳              | Unix 时间戳（秒）        |
| `at_uids`       | array   | @ 的用户 UID 列表       | `[0]` 表示无 @           |
| `msg_key`       | num     | 消息唯一标识            |                          |
| `msg_status`    | num     | 消息状态                | `0`：正常                |
| `notify_code`   | str     | 通知码                  | 通常为空                 |
| `msg_source`    | num     | 消息来源                | `7`：Web 端              |


## 响应示例

```json
{
    "code": 0,
    "msg": "0",
    "message": "0",
    "ttl": 1,
    "data": {
        "messages": [
            {
                "sender_uid": 1401939780,
                "receiver_type": 1,
                "receiver_id": 3690995472402999,
                "msg_type": 1,
                "content": "{\"content\":\"OK\"}",
                "msg_seqno": 2505681756610579,
                "timestamp": 1785046271,
                "at_uids": [0],
                "msg_key": 7666715356483981513,
                "msg_status": 0,
                "notify_code": "",
                "msg_source": 7
            }
        ],
        "has_more": 0,
        "min_seqno": 2505681756610579,
        "max_seqno": 2505681756610579
    }
}
```


## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | WBI 签名缺失或错误          |
| -403   | 风控拦截                    |
| -404   | 会话不存在                  |


## 调用示例（curl）

```bash
curl 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?size=20&session_type=1&talker_id=1401939780&begin_seqno=2505680951296006&sender_device_id=1&mobi_app=web&w_rid=xxx&wts=xxx' \
  -X GET \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **需要 WBI 签名**：该接口必须携带 `w_rid` 和 `wts`，否则返回 `-400`。
2. **`content` 字段为 JSON 字符串**：实际消息文本需解析 `{"content":"..."}` 提取。
3. **分页方式**：使用 `begin_seqno` 游标分页，首次请求传入 `0` 或 `max_seqno`。
4. **`has_more`**：`1` 表示有更早的历史消息。
5. **`msg_source`**：`7` 表示消息来自 Web 端发送。
