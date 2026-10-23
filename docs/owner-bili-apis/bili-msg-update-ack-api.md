# 标记私信已读

## 接口描述

将指定会话的所有消息标记为已读，清零未读数。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于私信会话中上报已读状态。


## 接口地址

```
POST https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（表单数据）

| 参数名         | 类型 | 内容             | 必要性   | 备注                                                 |
| -------------- | ---- | ---------------- | -------- | ---------------------------------------------------- |
| `talker_id`    | num  | 对方 UID         | **必要** |                                                      |
| `session_type` | num  | 会话类型         | **必要** | `1`：私聊                                            |
| `ack_seqno`    | num  | 已读到的消息序号 | **必要** | 将该序号及之前所有消息标记为已读，通常取 `max_seqno` |
| `build`        | num  | 构建版本         | 非必要   | 固定传 `0`                                           |
| `mobi_app`     | str  | 平台标识         | 非必要   | `web`                                                |
| `csrf`         | str  | CSRF Token       | **必要** | Cookie 中的 `bili_jct`                               |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `msg`     | str  | 状态信息 | `"OK"`     |
| `message` | str  | 状态信息 | `"OK"`     |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 | 空对象     |


## 响应示例

```json
{
    "code": 0,
    "msg": "OK",
    "message": "OK",
    "ttl": 1,
    "data": {}
}
```


## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -111   | CSRF 校验失败               |
| -403   | 访问权限不足 / 风控拦截     |
| -404   | 会话不存在                  |


## 调用示例（curl）

```bash
curl 'https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'talker_id=1401939780' \
  --data-urlencode 'session_type=1' \
  --data-urlencode 'ack_seqno=2537570613571591' \
  --data-urlencode 'build=0' \
  --data-urlencode 'mobi_app=web' \
  --data-urlencode 'csrf=xxx'
```


## 注意事项

1. **`ack_seqno` 来源**：从私信会话列表（`new_sessions`）的 `max_seqno` 字段获取。
2. **未读数归零**：调用成功后，该会话的 `unread_count` 会被重置为 `0`。
3. **幂等性**：重复上报相同或更小的 `ack_seqno` 不会产生副作用。
4. **不需要 WBI 签名**：该接口不需要 WBI 签名，仅需 CSRF 防护。


## 相关接口

| 功能         | 接口路径                                    | 说明                       |
| ------------ | ------------------------------------------- | -------------------------- |
| 私信会话列表 | `/session_svr/v1/session_svr/new_sessions`  | 获取所有会话及 `max_seqno` |
| 私信历史记录 | `/svr_sync/v1/svr_sync/fetch_session_msgs`  | 获取详细消息               |
| 私信未读数   | `/session_svr/v1/session_svr/single_unread` | 查询未读统计               |
