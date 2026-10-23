# 账号安全中心信息

## 接口描述

获取当前登录用户的账号安全中心信息，包含手机/邮箱绑定状态、实名认证状态、第三方社交账号绑定情况、账号安全评分等。

> 该接口位于通行证域名 `passport.bilibili.com`，用于账号安全中心页面展示。

---

## 接口地址

```
GET https://passport.bilibili.com/x/safecenter/user/info
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注         |
| --------------- | ---- | ---------- | ------ | ------------ |
| web_location    | str  | 来源标识   | 非必要 | 固定传 `0.0` |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1`   |

**示例请求 URL：**

```
https://passport.bilibili.com/x/safecenter/user/info?web_location=0.0&x-bili-redirect=1
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

| 字段         | 类型 | 内容             | 备注             |
| ------------ | ---- | ---------------- | ---------------- |
| account_info | obj  | 账号绑定信息     |                  |
| member_info  | obj  | 会员信息         | 包含实名认证状态 |
| sns_info     | obj  | 社交账号绑定信息 |                  |
| account_safe | obj  | 账号安全评分     |                  |

### `account_info` 对象

| 字段               | 类型 | 内容             | 备注                  |
| ------------------ | ---- | ---------------- | --------------------- |
| mid                | num  | 用户 UID         |                       |
| hide_tel           | str  | 手机号（脱敏）   | 如 `"178*****732"`    |
| hide_mail          | str  | 邮箱（脱敏）     | 如 `"376*****qq.com"` |
| bind_mail          | bool | 是否绑定邮箱     |                       |
| bind_tel           | bool | 是否绑定手机     |                       |
| tel_verify         | bool | 手机是否已验证   |                       |
| mail_verify        | bool | 邮箱是否已验证   |                       |
| bind_safe_question | bool | 是否绑定安全提问 |                       |
| unneeded_check     | bool | 是否无需检查     |                       |
| is_tourist         | bool | 是否游客账号     |                       |

### `member_info` 对象

| 字段            | 类型 | 内容             | 备注                            |
| --------------- | ---- | ---------------- | ------------------------------- |
| nickname        | str  | 用户昵称         |                                 |
| face            | str  | 头像地址         |                                 |
| realname_status | bool | **实名认证状态** | `true`：已实名，`false`：未实名 |

### `sns_info` 对象

| 字段        | 类型 | 内容              | 备注 |
| ----------- | ---- | ----------------- | ---- |
| bind_google | bool | 是否绑定 Google   |      |
| bind_fb     | bool | 是否绑定 Facebook |      |
| bind_apple  | bool | 是否绑定 Apple    |      |
| bind_qq     | bool | 是否绑定 QQ       |      |
| bind_weibo  | bool | 是否绑定 微博     |      |
| bind_wechat | bool | 是否绑定 微信     |      |

### `account_safe` 对象

| 字段  | 类型 | 内容         | 备注     |
| ----- | ---- | ------------ | -------- |
| score | num  | 账号安全评分 | 满分 100 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "account_info": {
            "hide_tel": "178*****732",
            "hide_mail": "376*****qq.com",
            "bind_mail": true,
            "bind_tel": true,
            "tel_verify": true,
            "mail_verify": true,
            "unneeded_check": false,
            "bind_safe_question": true,
            "mid": 3690995472402999,
            "is_tourist": false
        },
        "member_info": {
            "nickname": "YunLv_L",
            "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
            "realname_status": false
        },
        "sns_info": {
            "bind_google": false,
            "bind_fb": false,
            "bind_apple": false,
            "bind_qq": false,
            "bind_weibo": false,
            "bind_wechat": true
        },
        "account_safe": {
            "score": 80
        }
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
curl 'https://passport.bilibili.com/x/safecenter/user/info?web_location=0.0&x-bili-redirect=1' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **实名认证状态**：位于 `member_info.realname_status`，`true` 表示已实名，`false` 表示未实名。
3. **敏感信息脱敏**：手机号、邮箱均返回脱敏后的值，无法获取完整信息。
4. **安全评分**：`score` 字段反映账号安全等级（0-100），通常绑定手机、邮箱、社交账号等会提高评分。
5. **第三方绑定**：`sns_info` 中的字段均为 `bool` 类型，表示当前用户是否绑定了对应的第三方账号。
6. **接口用途**：该接口主要用于账号安全中心页面展示，也可用于检测当前用户的实名认证状态。
