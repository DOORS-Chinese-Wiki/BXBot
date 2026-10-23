# 置顶/取消置顶私信

## 接口描述

设置或取消私信会话的置顶状态。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于控制私信列表的置顶会话。该接口**不需要** WBI 签名。

---

## 接口地址

```
POST https://api.vc.bilibili.com/session_svr/v1/session_svr/set_top
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（表单数据）

| 参数名         | 类型 | 内容       | 必要性   | 备注                         |
| -------------- | ---- | ---------- | -------- | ---------------------------- |
| `talker_id`    | num  | 对方 UID   | **必要** | 要置顶/取消置顶的私信对象    |
| `session_type` | num  | 会话类型   | **必要** | `1`：私聊                    |
| `op_type`      | num  | 操作类型   | **必要** | `0`：设置置顶，`1`：取消置顶 |
| `build`        | num  | 构建版本   | 非必要   | 固定传 `0`                   |
| `mobi_app`     | str  | 平台标识   | 非必要   | 固定传 `web`                 |
| `csrf`         | str  | CSRF Token | **必要** | Cookie 中的 `bili_jct`       |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `msg`     | str  | 状态信息 | `"0"`      |
| `message` | str  | 状态信息 | `"0"`      |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 | 空对象     |


## 响应示例

```json
{
    "code": 0,
    "msg": "0",
    "message": "0",
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


## 调用示例（curl）

```bash
# 设置置顶
curl 'https://api.vc.bilibili.com/session_svr/v1/session_svr/set_top' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'talker_id=1447574' \
  --data-urlencode 'session_type=1' \
  --data-urlencode 'op_type=0' \
  --data-urlencode 'build=0' \
  --data-urlencode 'mobi_app=web' \
  --data-urlencode 'csrf=xxx'
```


## 注意事项

1. `op_type=0` 为设置置顶，`op_type=1` 为取消置顶。
2. 该接口不需要 WBI 签名。
3. `talker_id` 为对方的 UID，不是会话 ID。


## 相关接口

| 功能     | 接口路径                                    | 说明             |
| -------- | ------------------------------------------- | ---------------- |
| 私信列表 | `/session_svr/v1/session_svr/sessions`      | 获取所有私信会话 |
| 私信未读 | `/session_svr/v1/session_svr/single_unread` | 获取私信未读数   |
