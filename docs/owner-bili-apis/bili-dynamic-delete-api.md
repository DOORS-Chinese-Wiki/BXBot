# 删除动态

## 接口描述

删除指定的动态内容。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于删除已发布的动态。**仅需 CSRF 认证，无需 WBI 签名。**

---

## 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/operate/remove
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **签名方式**：❌ 不需要 WBI 签名，仅需 CSRF

---

## 请求参数

### URL Query 参数

| 参数名   | 类型 | 内容       | 必要性   | 备注                           |
| -------- | ---- | ---------- | -------- | ------------------------------ |
| platform | str  | 平台标识   | 非必要   | 固定传 `web`                   |
| csrf     | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

### 请求体参数（JSON）

| 参数名     | 类型 | 内容              | 必要性   | 备注                          |
| ---------- | ---- | ----------------- | -------- | ----------------------------- |
| dyn_id_str | str  | 动态 ID（字符串） | **必要** | 从发布接口返回的 `dyn_id_str` |
| dyn_type   | num  | 动态类型          | **必要** | `2`：图文动态                 |
| rid_str    | str  | 资源 ID（字符串） | **必要** | 从发布接口返回的 `dyn_rid`    |

**示例请求体：**

```json
{
    "dyn_id_str": "1224308010054058001",
    "dyn_type": 2,
    "rid_str": "401538909"
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
| -403   | 风控拦截（无权限删除该动态）             |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/dynamic/feed/operate/remove?platform=web&csrf=xxx' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://t.bilibili.com/' \
  -H 'Origin: https://t.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-raw '{
    "dyn_id_str": "1224308010054058001",
    "dyn_type": 2,
    "rid_str": "401538909"
  }'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名，仅需 CSRF 防护。
2. **`rid_str` 来源**：从动态发布接口返回的 `dyn_rid` 字段获取。
3. **`dyn_type`**：`2` 表示图文动态，其他类型数值待验证。
4. **删除不可逆**：动态删除后无法恢复，请谨慎操作。
5. **权限限制**：只能删除自己发布的动态。
6. **`data` 为空**：操作成功时 `data` 为空对象，不返回额外数据。


### 📂 动态模块文件清单

| 文件                             | 内容                 |
| -------------------------------- | -------------------- |
| `bili-dynamic-feed-api.md`       | 动态首页推荐流       |
| `bili-article-list-api.md`       | 图文动态列表（专栏） |
| `bili-space-dynamic-feed-api.md` | 用户空间动态列表     |
| `bili-dynamic-publish-api.md`    | 动态发布             |
| `bili-dynamic-thumb-api.md`      | 动态点赞/取消点赞    |
| **`bili-dynamic-delete-api.md`** | **动态删除（新增）** |
