# 获取用户关系统计

## 接口描述

获取指定用户的关系统计数据，包含关注数、粉丝数、黑名单数等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间展示用户关系统计。

---

## 接口地址

```
GET https://api.bilibili.com/x/relation/stat
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注                       |
| ------------ | ---- | -------- | -------- | -------------------------- |
| vmid         | num  | 用户 UID | **必要** | 目标用户的 UID             |
| web_location | str  | 来源标识 | 非必要   | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/relation/stat?vmid=3690995472402999&web_location=333.1387
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 |            |

### `data` 对象

| 字段             | 类型     | 内容         | 备注                 |
| ---------------- | -------- | ------------ | -------------------- |
| mid              | num      | 用户 UID     |                      |
| following        | num      | 关注数       |                      |
| whisper          | num      | 悄悄关注数   | 功能已下线，可能为 0 |
| black            | num      | 黑名单数     |                      |
| follower         | num      | 粉丝数       |                      |
| fans_medal_toast | null/obj | 粉丝勋章提示 | 通常为 null          |
| fans_effect      | null/obj | 粉丝影响力   | 通常为 null          |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "mid": 3690995472402999,
        "following": 69,
        "whisper": 0,
        "black": 10,
        "follower": 38,
        "fans_medal_toast": null,
        "fans_effect": null
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
curl 'https://api.bilibili.com/x/relation/stat?vmid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`whisper` 字段**：悄悄关注功能已下线，该字段可能始终为 `0`。
3. **数据缓存**：统计数据可能存在缓存，不是实时更新的。


---

### 📂 空间相关接口汇总

| 文件名                        | 功能                                           |
| ----------------------------- | ---------------------------------------------- |
| `bili-space-user-info-api.md` | 用户基本信息（昵称、签名、等级、勋章、大会员） |
| `bili-space-upstat-api.md`    | 用户内容统计（播放数、获赞数、专栏阅读数）     |
| `bili-relation-stat-api.md`   | 用户关系统计（关注数、粉丝数、黑名单数）       |
| `bili-space-archive-api.md`   | 用户投稿列表                                   |
| `bili-space-bangumi-api.md`   | 用户追番列表                                   |
| `bili-space-top-api.md`       | 用户置顶视频                                   |
