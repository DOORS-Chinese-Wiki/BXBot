# 消息通知未读数

## 接口描述

获取当前用户各类消息的未读数量，包括 at、回复、点赞、系统通知等。

> 该接口位于消息域名 `api.vc.bilibili.com`，用于消息中心展示未读消息角标。


## 接口地址

```
GET https://api.vc.bilibili.com/x/im/web/msgfeed/unread
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名         | 类型 | 内容     | 必要性 | 备注       |
| -------------- | ---- | -------- | ------ | ---------- |
| `build`        | num  | 构建版本 | 非必要 | 固定传 `0` |
| `mobi_app`     | str  | 平台标识 | 非必要 | `web`      |
| `web_location` | str  | 来源标识 | 非必要 | `0.0`      |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `message` | str  | 状态信息 | `"0"`      |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段            | 类型 | 内容             | 备注             |
| --------------- | ---- | ---------------- | ---------------- |
| `at`            | num  | @ 我的未读数     |                  |
| `coin`          | num  | 投币未读数       |                  |
| `danmu`         | num  | 弹幕未读数       |                  |
| `favorite`      | num  | 收藏未读数       |                  |
| `like`          | num  | 点赞未读数       |                  |
| `recv_like`     | num  | 收到的点赞未读数 |                  |
| `recv_reply`    | num  | 收到的回复未读数 |                  |
| `reply`         | num  | 评论回复未读数   |                  |
| `sys_msg`       | num  | 系统通知未读数   |                  |
| `sys_msg_style` | num  | 系统通知样式     | `1`：默认样式    |
| `up`            | num  | UP 主相关未读数  | 如 UP 主助手消息 |


## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "at": 0,
        "coin": 0,
        "danmu": 0,
        "favorite": 0,
        "like": 0,
        "recv_like": 0,
        "recv_reply": 0,
        "reply": 0,
        "sys_msg": 0,
        "sys_msg_style": 1,
        "up": 0
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
curl 'https://api.vc.bilibili.com/x/im/web/msgfeed/unread?build=0&mobi_app=web&web_location=0.0' \
  -X GET \
  -H 'Referer: https://message.bilibili.com/' \
  -H 'Origin: https://message.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **与 `api.bilibili.com/x/msgfeed/unread` 的区别**：两者返回结构略有不同，本接口字段更丰富（含 `coin`、`danmu`、`favorite` 等）。
3. **所有未读数为数值类型**，`0` 表示无未读。


## 相关接口

| 功能                   | 接口路径                                                     | 说明                                        |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| 通知消息未读数（旧版） | `https://api.bilibili.com/x/msgfeed/unread`                  | 返回 `at`、`like`、`reply`、`sys_msg`、`up` |
| 私信未读数             | `https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread` | 返回未关注/已关注用户私信未读数             |
| 消息通知设置           | `https://api.vc.bilibili.com/link_setting/v1/link_setting/get` | 获取消息通知开关设置                        |
