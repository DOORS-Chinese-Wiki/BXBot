# 消息通知设置

## 接口描述

获取当前用户的消息通知与互动提醒设置。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于消息中心设置页面展示。


## 接口地址

```
GET https://api.vc.bilibili.com/link_setting/v1/link_setting/get
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名                | 类型 | 内容                 | 必要性 | 备注       |
| --------------------- | ---- | -------------------- | ------ | ---------- |
| `msg_notify`          | num  | 消息通知开关         | 非必要 | 固定传 `1` |
| `show_unfollowed_msg` | num  | 是否展示未关注人消息 | 非必要 | 固定传 `1` |
| `build`               | num  | 构建版本             | 非必要 | 固定传 `0` |
| `mobi_app`            | str  | 平台标识             | 非必要 | `web`      |
| `web_location`        | str  | 来源标识             | 非必要 | `0.0`      |

> **说明**：所有参数均为固定值，实际业务逻辑由服务端根据当前用户返回对应设置。


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

| 字段                       | 类型     | 内容                 | 备注                   |
| -------------------------- | -------- | -------------------- | ---------------------- |
| `show_unfollowed_msg`      | num      | 是否展示未关注人消息 | `0`：不展示，`1`：展示 |
| `msg_notify`               | num      | 消息通知总开关       | `0`：关闭，`1`：开启   |
| `set_like`                 | num      | 点赞提醒             | `0`：关闭，`1`：开启   |
| `set_comment`              | num      | 评论提醒             | `0`：关闭，`1`：开启   |
| `set_at`                   | num      | @ 提醒               | `0`：关闭，`1`：开启   |
| `is_group_fold`            | num      | 是否折叠群组消息     | `0`：不折叠，`1`：折叠 |
| `should_receive_group`     | num      | 是否接收群组消息     | `0`：不接收，`1`：接收 |
| `receive_unfollow_msg`     | num      | 是否接收未关注人消息 | `0`：不接收，`1`：接收 |
| `followed_reply`           | num      | 关注的人回复提醒     | `0`：关闭，`1`：开启   |
| `keys_reply`               | num      | 关键词回复提醒       | `0`：关闭，`1`：开启   |
| `recv_reply`               | num      | 接收回复提醒         | `0`：关闭，`1`：开启   |
| `voyage_reply`             | num      | 旅程回复提醒         | `0`：关闭，`1`：开启   |
| `recommend_followed_reply` | num      | 推荐关注回复提醒     | `0`：关闭，`1`：开启   |
| `ai_intercept`             | num      | AI 评论过滤          | `0`：关闭，`1`：开启   |
| `anti_harassment`          | null/obj | 反骚扰设置           | 当前为 `null`          |
| `set_recv_reply`           | num      | 接收回复设置         | `0`：关闭，`1`：开启   |
| `set_recv_like`            | num      | 接收点赞设置         | `0`：关闭，`1`：开启   |
| `set_new_follow`           | num      | 新关注提醒           | `0`：关闭，`1`：开启   |


## 响应示例

```json
{
    "code": 0,
    "msg": "0",
    "message": "0",
    "ttl": 1,
    "data": {
        "show_unfollowed_msg": 0,
        "msg_notify": 1,
        "set_like": 0,
        "set_comment": 0,
        "set_at": 0,
        "is_group_fold": 1,
        "should_receive_group": 1,
        "receive_unfollow_msg": 1,
        "followed_reply": 0,
        "keys_reply": 0,
        "recv_reply": 0,
        "voyage_reply": 0,
        "recommend_followed_reply": 0,
        "ai_intercept": 1,
        "anti_harassment": null,
        "set_recv_reply": 0,
        "set_recv_like": 0,
        "set_new_follow": 0
    }
}
```


## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -403   | 风控拦截                    |


## 调用示例（curl）

```bash
curl 'https://api.vc.bilibili.com/link_setting/v1/link_setting/get?msg_notify=1&show_unfollowed_msg=1&build=0&mobi_app=web&web_location=0.0' \
  -X GET \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **GET 请求固定参数**：`msg_notify=1`、`show_unfollowed_msg=1` 为固定值。
3. **响应字段均为开关类配置**：`0` 关闭，`1` 开启。
4. **`anti_harassment`**：当前为 `null`，可能是预留字段。


## 相关接口

| 功能         | 接口路径                                                     | 说明                                  |
| ------------ | ------------------------------------------------------------ | ------------------------------------- |
| 未读消息数   | `https://api.bilibili.com/x/msgfeed/unread`                  | 获取 at、回复、点赞、系统通知等未读数 |
| 未读私信数   | `https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread` | 获取未读私信数                        |
| 私信历史记录 | `https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs` | 获取私信聊天记录                      |
