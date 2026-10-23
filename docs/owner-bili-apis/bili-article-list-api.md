# 获取用户图文动态列表

## 接口描述

获取指定用户发布的所有图文动态（专栏/文章）列表，包含封面、标题、点赞数等信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于用户空间的图文动态列表展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/polymer/web-dynamic/v1/opus/feed/space
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容         | 必要性   | 备注                                   |
| ------------ | ---- | ------------ | -------- | -------------------------------------- |
| host_mid     | num  | 目标用户 UID | **必要** | 要查询的用户 ID                        |
| page         | num  | 页码         | 非必要   | 默认 1                                 |
| offset       | str  | 翻页偏移量   | 非必要   | 首次请求传空字符串                     |
| type         | str  | 内容类型     | **必要** | `article`：图文动态，`video`：视频动态 |
| web_location | str  | 来源标识     | 非必要   | 固定传 `0.0`                           |
| w_rid        | str  | WBI 签名     | **必要** | 见 WBI 签名算法                        |
| wts          | num  | WBI 时间戳   | **必要** | 秒级 Unix 时间戳                       |

**示例请求 URL：**

```
https://api.bilibili.com/x/polymer/web-dynamic/v1/opus/feed/space?host_mid=1447574&page=1&offset=&type=article&web_location=0.0&w_rid=xxx&wts=xxx
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

| 字段       | 类型  | 内容           | 备注             |
| ---------- | ----- | -------------- | ---------------- |
| has_more   | bool  | 是否有更多数据 | `true`：有下一页 |
| items      | array | 图文动态列表   |                  |
| offset     | str   | 下一页偏移量   | 翻页时使用       |
| update_num | num   | 更新数量       |                  |

### `items` 数组元素

| 字段     | 类型 | 内容              | 备注         |
| -------- | ---- | ----------------- | ------------ |
| content  | str  | 图文动态标题/描述 |              |
| cover    | obj  | 封面图信息        |              |
| jump_url | str  | 跳转链接          | 相对路径     |
| opus_id  | str  | 图文动态 ID       | 全局唯一标识 |
| stat     | obj  | 统计数据          |              |

### `cover` 对象

| 字段   | 类型 | 内容       | 备注 |
| ------ | ---- | ---------- | ---- |
| url    | str  | 封面图地址 |      |
| width  | num  | 封面图宽度 |      |
| height | num  | 封面图高度 |      |

### `stat` 对象

| 字段 | 类型 | 内容   | 备注       |
| ---- | ---- | ------ | ---------- |
| like | str  | 点赞数 | 字符串格式 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "has_more": false,
        "items": [
            {
                "content": "【洛少爷】动态表情包",
                "cover": {
                    "height": 188,
                    "url": "https://i0.hdslb.com/bfs/article/xxx.png",
                    "width": 640
                },
                "jump_url": "//www.bilibili.com/opus/762888042855792643",
                "opus_id": "762888042855792643",
                "stat": {
                    "like": "2910"
                }
            }
        ],
        "offset": "",
        "update_num": 0
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | WBI 签名缺失或错误          |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/polymer/web-dynamic/v1/opus/feed/space?host_mid=1447574&page=1&offset=&type=article&web_location=0.0&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`type` 参数**：`article` 表示图文动态，`video` 表示视频动态。
3. **`jump_url` 为相对路径**：需要拼接 `https://www.bilibili.com` 使用。
4. **分页**：使用 `page` 参数翻页，`offset` 为空字符串时表示第一页。
5. **与原项目区别**：原项目 `docs/article/list.md` 可能是旧版专栏列表接口，本接口为 V2 动态体系的图文列表。
