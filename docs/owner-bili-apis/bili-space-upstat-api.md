# 获取用户空间统计数据

## 接口描述

获取指定用户的统计数据，包含视频播放数、获赞数、专栏阅读数等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间展示用户统计数据。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/upstat
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注                       |
| ------------ | ---- | -------- | -------- | -------------------------- |
| mid          | num  | 用户 UID | **必要** | 目标用户的 UID             |
| web_location | str  | 来源标识 | 非必要   | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/upstat?mid=3690995472402999&web_location=333.1387
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

| 字段    | 类型 | 内容         | 备注 |
| ------- | ---- | ------------ | ---- |
| archive | obj  | 视频统计数据 |      |
| article | obj  | 专栏统计数据 |      |
| likes   | num  | 获赞总数     |      |

### `archive` 对象

| 字段      | 类型 | 内容         | 备注       |
| --------- | ---- | ------------ | ---------- |
| view      | num  | 视频总播放数 |            |
| vt        | num  | 视频类型     | 0 表示普通 |
| enable_vt | num  | 是否启用 VT  | 0 表示否   |

### `article` 对象

| 字段 | 类型 | 内容         | 备注 |
| ---- | ---- | ------------ | ---- |
| view | num  | 专栏总阅读数 |      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "archive": {
            "enable_vt": 0,
            "view": 1451,
            "vt": 0
        },
        "article": {
            "view": 0
        },
        "likes": 352
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
curl 'https://api.bilibili.com/x/space/upstat?mid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **统计维度**：
   - `archive.view`：视频播放数
   - `article.view`：专栏阅读数
   - `likes`：获赞总数（包括视频、专栏等所有内容的点赞）
3. **数据更新**：统计数据存在缓存，可能不是实时更新的。
