# 动态点赞/取消点赞

## 接口描述

对指定动态进行点赞或取消点赞操作。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于动态互动。**仅需 CSRF 认证，无需 WBI 签名。**

---

## 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/dyn/thumb
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **签名方式**：❌ 不需要 WBI 签名，仅需 CSRF

---

## 请求参数

### URL Query 参数

| 参数名 | 类型 | 内容       | 必要性   | 备注                           |
| ------ | ---- | ---------- | -------- | ------------------------------ |
| csrf   | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

### 请求体参数（JSON）

| 参数名     | 类型 | 内容              | 必要性   | 备注                          |
| ---------- | ---- | ----------------- | -------- | ----------------------------- |
| dyn_id_str | str  | 动态 ID（字符串） | **必要** | 从发布接口返回的 `dyn_id_str` |
| up         | num  | 操作类型          | **必要** | `1`：点赞，`2`：取消点赞      |

**示例请求体（点赞）：**

```json
{
    "dyn_id_str": "1224308010054058001",
    "up": 1
}
```

**示例请求体（取消点赞）：**

```json
{
    "dyn_id_str": "1224308010054058001",
    "up": 2
}
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注              |
| ------- | ---- | -------- | ----------------- |
| code    | num  | 状态码   | 0 表示成功        |
| message | str  | 状态信息 | `"OK"`            |
| ttl     | num  | 1        |                   |
| data    | obj  | 数据本体 | 通常为空对象 `{}` |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {}
}
```

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -111   | CSRF 校验失败（`bili_jct` 不匹配或过期） |
| -403   | 风控拦截                                 |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

### 点赞

```bash
curl 'https://api.bilibili.com/x/dynamic/feed/dyn/thumb?csrf=xxx' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://t.bilibili.com/' \
  -H 'Origin: https://t.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-raw '{
    "dyn_id_str": "1224308010054058001",
    "up": 1
  }'
```

### 取消点赞

```bash
curl 'https://api.bilibili.com/x/dynamic/feed/dyn/thumb?csrf=xxx' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://t.bilibili.com/' \
  -H 'Origin: https://t.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-raw '{
    "dyn_id_str": "1224308010054058001",
    "up": 2
  }'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名，仅需 CSRF 防护。
2. **`up` 参数**：`1` 表示点赞，`2` 表示取消点赞。
3. **`dyn_id_str` 来源**：从动态发布接口返回的 `dyn_id_str` 字段获取。
4. **幂等性**：对已点赞的动态再次发送 `up:1` 是否会返回错误，待验证。
5. **`data` 为空**：操作成功时 `data` 为空对象，不返回额外数据。


### 📂 动态模块文件清单

| 文件                             | 内容                          |
| -------------------------------- | ----------------------------- |
| `bili-dynamic-feed-api.md`       | 动态首页推荐流                |
| `bili-article-list-api.md`       | 图文动态列表（专栏）          |
| `bili-space-dynamic-feed-api.md` | 用户空间动态列表              |
| `bili-dynamic-publish-api.md`    | 动态发布                      |
| **`bili-dynamic-thumb-api.md`**  | **动态点赞/取消点赞（新增）** |
