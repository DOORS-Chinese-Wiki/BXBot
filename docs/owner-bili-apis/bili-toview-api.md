# 稍后再看 API

## 接口列表

### 1. 稍后再看列表
### 2. 添加到稍后再看
### 3. 从稍后再看移除（单条）
### 4. 批量删除稍后再看（多选）
### 5. 清空稍后再看

---

# 1. 稍后再看列表

## 接口描述

获取当前登录用户的“稍后再看”列表中的所有视频。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示用户添加到“稍后再看”的视频列表。

---

## 接口地址

```
GET https://api.bilibili.com/x/v2/history/toview/web
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性 | 备注         |
| ------------ | ---- | -------- | ------ | ------------ |
| web_location | str  | 来源标识 | 非必要 | 固定传 `0.0` |

> **注意**：该接口没有分页参数，一次性返回所有稍后再看的视频。

**示例请求 URL：**

```
https://api.bilibili.com/x/v2/history/toview/web?web_location=0.0
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

| 字段  | 类型  | 内容             | 备注                                                         |
| ----- | ----- | ---------------- | ------------------------------------------------------------ |
| count | num   | 稍后再看列表总数 |                                                              |
| list  | array | 视频列表         | 每个元素为一个视频对象，结构与视频信息接口类似，且包含 `pages`（分P详情）、`add_at`（添加时间戳）、`progress`（播放进度）、`viewed`（是否已看）等扩展字段 |

### `list` 数组元素（关键字段）

| 字段          | 类型  | 内容                   | 备注                                                       |
| ------------- | ----- | ---------------------- | ---------------------------------------------------------- |
| aid           | num   | 视频 AV ID             |                                                            |
| bvid          | str   | 视频 BV ID             |                                                            |
| title         | str   | 视频标题               |                                                            |
| pic           | str   | 封面图地址             |                                                            |
| duration      | num   | 视频总时长（秒）       |                                                            |
| pubdate       | num   | 发布时间戳             | Unix 时间戳（秒）                                          |
| owner         | obj   | UP 主信息              | 包含 `mid`、`name`、`face`                                 |
| stat          | obj   | 统计数据               | 播放量、点赞、投币、收藏等                                 |
| pages         | array | 分 P 列表              | 每个元素包含 `cid`、`page`、`part`、`duration` 等          |
| cid           | num   | 当前分 P 的 CID        |                                                            |
| progress      | num   | 播放进度（秒）         |                                                            |
| add_at        | num   | 添加到稍后再看的时间戳 | Unix 时间戳（秒）                                          |
| viewed        | bool  | 是否已观看             | `true`/`false`                                             |
| uri           | str   | 播放链接               | `https://www.bilibili.com/medialist/play/watchlater/BVxxx` |
| first_frame   | str   | 首帧图片地址           |                                                            |
| short_link_v2 | str   | 短链接                 | 如 `https://b23.tv/BVxxx`                                  |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "count": 8,
        "list": [
            {
                "aid": 116669783476738,
                "bvid": "BV1spVQ6xEqu",
                "title": "【动画歌曲伴奏】别找了！最全最好的《开心宝贝》/《开心超人联盟》动画歌曲伴奏都在这里——",
                "pic": "http://i2.hdslb.com/bfs/archive/xxx.jpg",
                "duration": 2190,
                "owner": {
                    "mid": 3537116862613508,
                    "name": "九米寒冰",
                    "face": "https://i2.hdslb.com/bfs/face/xxx.jpg"
                },
                "stat": {
                    "view": 1116,
                    "like": 32
                },
                "pages": [
                    {
                        "cid": 38751371919,
                        "page": 1,
                        "part": "开心往前飞",
                        "duration": 78
                    }
                ],
                "cid": 38751371919,
                "progress": 0,
                "add_at": 1780660675,
                "viewed": false,
                "uri": "https://www.bilibili.com/medialist/play/watchlater/BV1spVQ6xEqu"
            }
        ]
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
curl 'https://api.bilibili.com/x/v2/history/toview/web?web_location=0.0' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口目前不需要 WBI 签名，直接 GET 即可。
2. **无分页**：该接口一次性返回所有稍后再看的视频，没有 `pn`/`ps` 分页参数。
3. **`add_at` 字段**：表示该视频被添加到稍后再看的时间戳，可用于排序。
4. **`viewed` 字段**：`true` 表示已观看，但仍在稍后再看列表中（未移除）。
5. **`pages` 数组**：返回完整的分 P 信息，包括每个分 P 的 `cid`、时长和标题。
6. **返回结构与视频信息接口类似**：该接口返回的 `list` 元素结构与视频信息接口（`/x/web-interface/view`）的 `data` 对象高度相似，额外增加了 `add_at`、`progress`、`viewed`、`uri` 等扩展字段。
7. **最大容量**：稍后再看列表有数量上限，目前为 **100 个**。


# 2. 添加到稍后再看

## 接口描述

将指定视频添加到当前登录用户的“稍后再看”列表中。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于管理稍后再看列表。

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/toview/add
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data` 或 `application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名 | 类型 | 内容       | 必要性   | 备注                             |
| ------ | ---- | ---------- | -------- | -------------------------------- |
| aid    | num  | 视频 AID   | **必要** | 可通过 `bvid` 从视频信息接口获取 |
| csrf   | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值   |

**示例请求体：**

```
aid=116854534180306&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1
}
```

**响应示例（已存在）：**

```json
{
    "code": -404,
    "message": "视频已存在于稍后再看列表",
    "ttl": 1
}
```

> **注意**：以上错误码为推测，实际以抓包为准。

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| -404   | 视频不存在或已存在                       |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/toview/add' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'aid=116854534180306' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **AID 获取方式**：视频的 `aid` 可以通过 `bvid` 调用视频信息接口 `/x/web-interface/view` 获取，也可直接从页面源码或响应中提取。
2. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
3. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
4. **幂等性**：如果视频已存在于稍后再看列表中，再次添加会返回错误码。
5. **列表上限**：稍后再看列表有数量上限（目前为 **100 个**），超出后添加可能失败。


# 3. 从稍后再看移除（单条）

## 接口描述

从当前登录用户的“稍后再看”列表中移除指定视频（单条删除）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于管理稍后再看列表。

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/toview/del
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data` 或 `application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名 | 类型 | 内容       | 必要性   | 备注                           |
| ------ | ---- | ---------- | -------- | ------------------------------ |
| aid    | num  | 视频 AID   | **必要** | 要移除的视频 ID                |
| csrf   | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

**示例请求体：**

```
aid=116854534180306&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1
}
```

**响应示例（不存在）：**

```json
{
    "code": -404,
    "message": "视频不在稍后再看列表中",
    "ttl": 1
}
```

> **注意**：以上错误码为推测，实际以抓包为准。

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| -404   | 视频不在稍后再看列表中                   |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/toview/del' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'aid=116854534180306' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **单条删除**：该接口一次只能移除一个视频，如需清空全部，请使用清空接口。
2. **参数结构与添加接口完全一致**：仅接口路径从 `/add` 变为 `/del`。
3. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
4. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
5. **幂等性**：如果视频不在稍后再看列表中，再次调用会返回错误码。
6. **与添加接口共用参数**：`aid` 是唯一标识，通过视频信息接口获取。


# 4. 批量删除稍后再看（多选）

## 接口描述

从当前登录用户的“稍后再看”列表中批量移除多个视频。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于一次性删除多个稍后再看视频。**该接口需要 WBI 签名。**

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/toview/v2/dels
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data` 或 `application/x-www-form-urlencoded`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数

### URL Query 参数（WBI 签名）

| 参数名 | 类型 | 内容       | 必要性   | 备注             |
| ------ | ---- | ---------- | -------- | ---------------- |
| w_rid  | str  | WBI 签名   | **必要** | 见 WBI 签名算法  |
| wts    | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳 |

### 表单参数

| 参数名    | 类型 | 内容          | 必要性   | 备注                                      |
| --------- | ---- | ------------- | -------- | ----------------------------------------- |
| resources | str  | 视频 AID 列表 | **必要** | 多个 AID 用英文逗号分隔，如 `123,456,789` |
| csrf      | str  | CSRF Token    | **必要** | 位于 Cookie 中的 `bili_jct` 值            |

**示例请求体：**

```
resources=116871378507379,116783382006679&csrf=51e2f74218c9e721a5d4c74db15cc8f6
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1
}
```

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -400   | WBI 签名缺失或错误                       |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/toview/v2/dels?w_rid=c359b0ff5bb00d2c1dcdd54f892966f2&wts=1783753147' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'resources=116871378507379,116783382006679' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误或带 `v_voucher` 的响应。
2. **`resources` 参数格式**：多个 AID 用英文逗号分隔，**不含空格**。
3. **与单条删除的区别**：
   - 单条删除 `/del`：传 `aid`，**无需 WBI 签名**
   - 批量删除 `/v2/dels`：传 `resources`（逗号分隔），**需要 WBI 签名**
4. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
5. **部分失败处理**：如果部分 AID 无效或不在稍后再看列表中，接口是否部分成功暂未验证（待补充）。


# 5. 清空稍后再看

## 接口描述

清空当前登录用户的“稍后再看”列表，移除所有视频。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于一次性清空整个稍后再看列表。**该接口需要 WBI 签名。**

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/toview/clear
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data` 或 `application/x-www-form-urlencoded`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数

### URL Query 参数（WBI 签名）

| 参数名 | 类型 | 内容       | 必要性   | 备注             |
| ------ | ---- | ---------- | -------- | ---------------- |
| w_rid  | str  | WBI 签名   | **必要** | 见 WBI 签名算法  |
| wts    | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳 |

### 表单参数

| 参数名     | 类型 | 内容       | 必要性   | 备注                           |
| ---------- | ---- | ---------- | -------- | ------------------------------ |
| clean_type | num  | 清理类型   | 非必要   | `0` 表示清空全部               |
| csrf       | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

**示例请求体：**

```
clean_type=0&csrf=51e2f74218c9e721a5d4c74db15cc8f6
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1
}
```

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -400   | WBI 签名缺失或错误                       |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/toview/clear?w_rid=305c3f18f69533f9528e547dc18a4cdf&wts=1783752994' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'clean_type=0' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误或带 `v_voucher` 的响应。这是与 `/add` 和 `/del` 接口最大的区别。
2. **`clean_type` 参数**：目前抓到的值为 `0`，表示清空全部。可能存在其他值对应不同的清理模式（如按类型清理），待后续验证。
3. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
4. **清空操作不可逆**：调用后稍后再看列表将变为空，无法恢复（除非重新添加）。


## 相关接口汇总

| 功能           | 接口路径                       | 请求方式 | 签名方式 | 关键参数                        |
| -------------- | ------------------------------ | -------- | -------- | ------------------------------- |
| 稍后再看列表   | `/x/v2/history/toview/web`     | GET      | 无       | `web_location`                  |
| 添加到稍后再看 | `/x/v2/history/toview/add`     | POST     | 无       | `aid`、`csrf`                   |
| 单条删除       | `/x/v2/history/toview/del`     | POST     | 无       | `aid`、`csrf`                   |
| 批量删除       | `/x/v2/history/toview/v2/dels` | POST     | WBI      | `resources`（逗号分隔）、`csrf` |
| 清空全部       | `/x/v2/history/toview/clear`   | POST     | WBI      | `clean_type=0`、`csrf`          |
