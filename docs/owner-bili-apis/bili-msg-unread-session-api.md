# 私信未读数

## 接口描述

获取当前用户私信的未读数量，按会话类型分类统计。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于私信列表展示未读角标。


## 接口地址

```
GET https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名         | 类型 | 内容           | 必要性 | 备注       |
| -------------- | ---- | -------------- | ------ | ---------- |
| `unread_type`  | num  | 未读类型       | 非必要 | 固定传 `0` |
| `show_dustbin` | num  | 是否显示垃圾箱 | 非必要 | 固定传 `1` |
| `build`        | num  | 构建版本       | 非必要 | 固定传 `0` |
| `mobi_app`     | str  | 平台标识       | 非必要 | `web`      |
| `web_location` | str  | 来源标识       | 非必要 | `0.0`      |

> **说明**：所有参数均为固定值，不影响返回结果，仅用于客户端标识。


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

| 字段                      | 类型 | 内容                     | 备注 |
| ------------------------- | ---- | ------------------------ | ---- |
| `unfollow_unread`         | num  | 未关注用户私信未读数     |      |
| `follow_unread`           | num  | 已关注用户私信未读数     |      |
| `unfollow_push_msg`       | num  | 未关注用户推送消息未读数 |      |
| `dustbin_push_msg`        | num  | 垃圾箱推送消息未读数     |      |
| `dustbin_unread`          | num  | 垃圾箱私信未读数         |      |
| `biz_msg_unfollow_unread` | num  | 业务消息（未关注）未读数 |      |
| `biz_msg_follow_unread`   | num  | 业务消息（已关注）未读数 |      |
| `custom_unread`           | num  | 自定义消息未读数         |      |


## 响应示例

```json
{
    "code": 0,
    "msg": "0",
    "message": "0",
    "ttl": 1,
    "data": {
        "unfollow_unread": 0,
        "follow_unread": 0,
        "unfollow_push_msg": 0,
        "dustbin_push_msg": 0,
        "dustbin_unread": 0,
        "biz_msg_unfollow_unread": 0,
        "biz_msg_follow_unread": 0,
        "custom_unread": 0
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
curl 'https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread?unread_type=0&show_dustbin=1&build=0&mobi_app=web&web_location=0.0' \
  -X GET \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **所有未读数为数值类型**，`0` 表示无未读。
3. **与通知未读数接口区分**：本接口仅统计私信相关未读，不包括 at、回复、点赞等。


## 相关接口

| 功能           | 接口路径                                                     | 说明                     |
| -------------- | ------------------------------------------------------------ | ------------------------ |
| 通知消息未读数 | `https://api.vc.bilibili.com/x/im/web/msgfeed/unread`        | at、回复、点赞、系统通知 |
| 私信历史记录   | `https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs` | 获取私信聊天记录         |
| 消息通知设置   | `https://api.vc.bilibili.com/link_setting/v1/link_setting/get` | 获取消息通知开关设置     |
