# UP主认证条件查询

## 接口描述

查询当前用户是否满足申请 UP主认证（个人认证/黄V）的各项前置条件。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人认证申请入口的前置条件判断。

---

## 接口地址

```
GET https://api.bilibili.com/x/member/official/conditions
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注           |
| --------------- | ---- | ---------- | ------ | -------------- |
| jsonp           | str  | JSONP 回调 | 非必要 | 固定传 `jsonp` |
| web_location    | str  | 来源标识   | 非必要 | 固定传 `0.0`   |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1`     |

**示例请求 URL：**

```
https://api.bilibili.com/x/member/official/conditions?jsonp=jsonp&web_location=0.0&x-bili-redirect=1
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 |            |

### `data` 对象

| 字段           | 类型 | 内容              | 备注                            |
| -------------- | ---- | ----------------- | ------------------------------- |
| bind_tel       | bool | 是否绑定手机      | `true`：已绑定，`false`：未绑定 |
| realname       | bool | 是否实名认证      | `true`：已实名，`false`：未实名 |
| follower_count | bool | 粉丝数是否 ≥ 10万 | `true`：达标，`false`：未达标   |
| archive_count  | bool | 投稿数是否 ≥ 1    | `true`：达标，`false`：未达标   |
| invited        | bool | 是否被官方邀请    | `true`：已受邀，`false`：未受邀 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "bind_tel": true,
        "realname": false,
        "follower_count": false,
        "archive_count": true,
        "invited": false
    }
}
```

---

## 页面展示对应关系

该接口返回的字段对应 UP主认证申请页面的条件清单：

| 字段             | 页面文案          | 状态（示例）                 |
| ---------------- | ----------------- | ---------------------------- |
| `bind_tel`       | ✅ 绑定手机用户    | 已满足                       |
| `realname`       | 提交实名认证      | 未满足（需用户完成实名认证） |
| `follower_count` | 粉丝数累计 ≥ 10万 | 未满足（需粉丝数达标）       |
| `archive_count`  | ✅ 相关投稿数 ≥ 1  | 已满足                       |
| `invited`        | 官方邀请          | 未满足（通常用于特殊通道）   |

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
curl 'https://api.bilibili.com/x/member/official/conditions?jsonp=jsonp&web_location=0.0&x-bili-redirect=1' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限当前用户**：该接口只能查询当前登录用户自己的认证条件状态。
3. **条件为 `bool` 类型**：`true` 表示该条件已满足，`false` 表示未满足。
4. **`invited` 字段**：`true` 表示用户收到了官方邀请，可能有独立的认证申请入口。
5. **粉丝数门槛**：`follower_count` 需要 **≥ 10 万** 才为 `true`。
6. **投稿数门槛**：`archive_count` 需要 **≥ 1** 个投稿才为 `true`。

---

## 相关接口

| 功能             | 接口路径                        | 说明                                  |
| ---------------- | ------------------------------- | ------------------------------------- |
| UP主认证条件查询 | `/x/member/official/conditions` | 查询认证前置条件                      |
| 账号安全中心信息 | `/x/safecenter/user/info`       | 包含实名认证状态（`realname_status`） |
| 用户空间信息     | `/x/space/wbi/acc/info`         | 包含粉丝数、投稿数等信息              |
