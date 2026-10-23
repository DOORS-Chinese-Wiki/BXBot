# 私信会话列表

## 接口描述

获取当前用户的所有私信会话列表，包含每个会话的最新消息、未读数、置顶状态等信息。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于私信列表页面展示。**该接口需要 WBI 签名。**


## 接口地址

```
GET https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：✅ 需要


## 请求参数（URL Query）

| 参数名         | 类型 | 内容       | 必要性   | 备注                                  |
| -------------- | ---- | ---------- | -------- | ------------------------------------- |
| `begin_ts`     | num  | 起始时间戳 | 非必要   | 用于分页，首次请求传 `0` 或当前时间戳 |
| `build`        | num  | 构建版本   | 非必要   | 固定传 `0`                            |
| `mobi_app`     | str  | 平台标识   | 非必要   | `web`                                 |
| `web_location` | str  | 来源标识   | 非必要   | `0.0`                                 |
| `w_rid`        | str  | WBI 签名   | **必要** | 见 WBI 签名算法                       |
| `wts`          | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳                      |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `msg`     | str  | 状态信息 | `"OK"`     |
| `message` | str  | 状态信息 | `"OK"`     |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段                    | 类型  | 内容           | 备注             |
| ----------------------- | ----- | -------------- | ---------------- |
| `session_list`          | array | 会话列表       |                  |
| `has_more`              | num   | 是否有更多     | `0`：无，`1`：有 |
| `anti_disturb_cleaning` | bool  | 防骚扰清理     | `false`          |
| `is_address_list_empty` | num   | 通讯录是否为空 | `0`：否          |
| `show_level`            | bool  | 是否显示等级   | `false`          |

### `session_list` 数组元素

| 字段                   | 类型 | 内容           | 备注           |
| ---------------------- | ---- | -------------- | -------------- |
| `talker_id`            | num  | 对方 UID       |                |
| `session_type`         | num  | 会话类型       | `1`：私聊      |
| `at_seqno`             | num  | @ 消息序号     | `0` 表示无 @   |
| `top_ts`               | num  | 置顶时间戳     | `0` 表示未置顶 |
| `group_name`           | str  | 分组名称       | 通常为空       |
| `group_cover`          | str  | 分组封面       | 通常为空       |
| `is_follow`            | num  | 是否关注对方   | `1`：已关注    |
| `is_dnd`               | num  | 是否免打扰     | `0`：关闭      |
| `ack_seqno`            | num  | 已读序号       |                |
| `ack_ts`               | num  | 已读时间戳     |                |
| `session_ts`           | num  | 会话更新时间戳 |                |
| `unread_count`         | num  | 未读消息数     |                |
| `last_msg`             | obj  | 最后一条消息   | 见下方         |
| `group_type`           | num  | 分组类型       | `0`：普通      |
| `can_fold`             | num  | 是否可折叠     | `0`：否        |
| `status`               | num  | 状态           | `0`：正常      |
| `max_seqno`            | num  | 最大消息序号   |                |
| `new_push_msg`         | num  | 新推送消息     | `0`：无        |
| `setting`              | num  | 设置           | `0`            |
| `is_guardian`          | num  | 是否监护人     | `0`：否        |
| `is_intercept`         | num  | 是否拦截       | `0`：否        |
| `is_trust`             | num  | 是否信任       | `0`：否        |
| `system_msg_type`      | num  | 系统消息类型   | `0`            |
| `live_status`          | num  | 直播状态       | `0`：未直播    |
| `biz_msg_unread_count` | num  | 业务消息未读数 |                |
| `user_label`           | null | 用户标签       | 通常为 `null`  |

### `last_msg` 对象

| 字段            | 类型  | 内容                    | 备注              |
| --------------- | ----- | ----------------------- | ----------------- |
| `sender_uid`    | num   | 发送者 UID              |                   |
| `receiver_type` | num   | 接收者类型              | `1`：用户         |
| `receiver_id`   | num   | 接收者 UID              |                   |
| `msg_type`      | num   | 消息类型                | `1`：文本         |
| `content`       | str   | 消息内容（JSON 字符串） | 需解析            |
| `msg_seqno`     | num   | 消息序号                |                   |
| `timestamp`     | num   | 发送时间戳              | Unix 时间戳（秒） |
| `at_uids`       | array | @ 的用户 UID 列表       | 通常为 `null`     |
| `msg_key`       | num   | 消息唯一标识            |                   |
| `msg_status`    | num   | 消息状态                | `0`：正常         |
| `notify_code`   | str   | 通知码                  | 通常为空          |
| `msg_source`    | num   | 消息来源                | `7`：Web 端       |


## 响应示例

```json
{
    "code": 0,
    "msg": "OK",
    "message": "OK",
    "ttl": 1,
    "data": {
        "session_list": [
            {
                "talker_id": 1401939780,
                "session_type": 1,
                "at_seqno": 0,
                "top_ts": 1785117407748995,
                "group_name": "",
                "group_cover": "",
                "is_follow": 1,
                "is_dnd": 0,
                "ack_seqno": 2537569304756230,
                "ack_ts": 1786946922973949,
                "session_ts": 1786946995800589,
                "unread_count": 1,
                "last_msg": {
                    "sender_uid": 1401939780,
                    "receiver_type": 1,
                    "receiver_id": 3690995472402999,
                    "msg_type": 1,
                    "content": "{\"content\":\"API Test!\"}",
                    "msg_seqno": 2537570613571591,
                    "timestamp": 1786946995,
                    "at_uids": null,
                    "msg_key": 7674878903886812670,
                    "msg_status": 0,
                    "notify_code": "",
                    "msg_source": 7
                },
                "group_type": 0,
                "can_fold": 0,
                "status": 0,
                "max_seqno": 2537570613571591,
                "new_push_msg": 0,
                "setting": 0,
                "is_guardian": 0,
                "is_intercept": 0,
                "is_trust": 0,
                "system_msg_type": 0,
                "live_status": 0,
                "biz_msg_unread_count": 0,
                "user_label": null
            }
        ],
        "has_more": 0,
        "anti_disturb_cleaning": false,
        "is_address_list_empty": 0,
        "show_level": false
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


## 调用示例（curl）

```bash
curl 'https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts=0&build=0&mobi_app=web&web_location=0.0&w_rid=xxx&wts=xxx' \
  -X GET \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **需要 WBI 签名**：该接口必须携带 WBI 签名。
2. **`top_ts` 判断置顶**：`top_ts` 不为 `0` 时表示该会话被置顶。
3. **`unread_count`**：该会话的未读消息数。
4. **`last_msg.content` 为 JSON 字符串**：实际文本需解析 `{"content":"..."}` 提取。
5. **`is_follow`**：`1` 表示已关注对方，可用于判断是否陌生人来信。
6. **分页**：使用 `begin_ts` 游标分页，`has_more` 为 `1` 时继续请求。


## 相关接口

| 功能          | 接口路径                                    | 说明                       |
| ------------- | ------------------------------------------- | -------------------------- |
| 私信历史记录  | `/svr_sync/v1/svr_sync/fetch_session_msgs`  | 获取与指定联系人的详细消息 |
| 私信未读数    | `/session_svr/v1/session_svr/single_unread` | 获取私信未读统计           |
| 置顶/取消置顶 | `/session_svr/v1/session_svr/set_top`       | 设置会话置顶状态           |
