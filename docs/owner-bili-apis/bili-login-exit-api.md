# 退出登录（注销）

## 接口描述

退出当前登录的账号，使会话失效（Cookie 中的 `SESSDATA` 失效）。

> 该接口位于通行证域名 `passport.bilibili.com`，用于用户主动退出登录。

---

## 接口地址

```
POST https://passport.bilibili.com/login/exit/v2
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| biliCSRF | str | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |
| gourl | str | 退出后跳转链接 | 非必要 | URL 编码，默认为 `https://www.bilibili.com/` |

**示例请求体：**

```
biliCSRF=40bc00dc2d06cb9fdc96b22b2d9377a9&gourl=https%3A%2F%2Fwww.bilibili.com%2Fhistory
```

---

## 响应结构

### 根对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| code | num | 状态码 | 0 表示成功 |
| message | str | 状态信息 | `"OK"` |
| ttl | num | 1 | |
| data | obj | 数据本体 | 通常为空对象或包含跳转信息 |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {}
}
```

**响应示例（失败）：**

```json
{
    "code": -403,
    "message": "CSRF 校验失败",
    "ttl": 1,
    "data": null
}
```

---

## 错误码

| 状态码 | 含义 |
| ------ | ---- |
| 0 | 操作成功 |
| -101 | 未登录（Cookie 无效或过期） |
| -403 | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| -500 | 服务器错误 |
| 其他 | 参见 `message` 字段 |

---

## 调用示例（curl）

```bash
curl 'https://passport.bilibili.com/login/exit/v2' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'biliCSRF=xxx' \
  --data-urlencode 'gourl=https%3A%2F%2Fwww.bilibili.com%2F'
```

---

## 注意事项

1. **`biliCSRF` 参数**：必须与 Cookie 中的 `bili_jct` 值一致，用于防止 CSRF 攻击。
2. **`gourl` 参数**：指定退出后跳转的页面，通常为 `https://www.bilibili.com/`，若未传则跳转到首页。
3. **无需 WBI 签名**：该接口不需要 WBI 签名。
4. **会话失效**：调用成功后，服务端会使当前 `SESSDATA` 失效，后续请求需重新登录。
5. **Cookie 清理**：客户端（浏览器或 APP）在收到成功响应后应主动清除本地存储的 Cookie 和缓存。

---

## 相关接口

| 功能 | 接口路径 | 请求方式 | 说明 |
| ---- | -------- | -------- | ---- |
| 退出登录 | `/login/exit/v2` | POST | 注销当前会话 |
| 登录信息 | `/x/web-interface/nav` | GET | 获取当前登录状态，可用于验证是否退出成功 |
| 登录操作 | 见 `/docs/login/login_action` | — | 登录方式（密码/短信/二维码） |

---

> ⚠️ **注意**：该接口为 V2 版本，原项目中可能为 `/login/exit`（旧版），建议优先使用 V2 接口。响应示例中 `data` 字段可能包含 `redirect_url` 等跳转信息，具体以实际响应为准。