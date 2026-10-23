好的，收到！`/log/web` 是B站前端埋点日志上报接口，用于记录用户行为数据，不影响主业务逻辑，Drop掉是安全的。

---

# 观看历史 API

## 接口列表

### 1. 观看历史列表（游标分页）

### 2. 历史记录搜索

### 3. 移除单条历史记录

### 4. 清空全部历史记录

---

# 1. 观看历史列表（游标分页）

## 接口描述

获取当前登录用户的观看历史记录，支持按视频、直播、专栏等类型筛选，采用游标分页方式。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于历史记录页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/web-interface/history/cursor
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容       | 必要性 | 备注                                                         |
| ------------ | ---- | ---------- | ------ | ------------------------------------------------------------ |
| max          | num  | 游标最大值 | 非必要 | 首次请求传 `0`，后续使用响应中的 `cursor.max`                |
| view_at      | num  | 游标时间戳 | 非必要 | 首次请求传 `0`，后续使用响应中的 `cursor.view_at`            |
| business     | str  | 业务类型   | 非必要 | 空字符串表示全部；`"archive"`：视频，`"live"`：直播，`"article"`：专栏 |
| ps           | num  | 每页数量   | 非必要 | 默认 `20`，最大可能为 `50`                                   |
| type         | str  | 类型       | 非必要 | 固定传 `"all"`                                               |
| web_location | str  | 来源标识   | 非必要 | 固定传 `333.1391` 或类似值                                   |

**示例请求 URL：**

```
https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business=&ps=20&type=all&web_location=333.1391
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

| 字段   | 类型  | 内容                 | 备注 |
| ------ | ----- | -------------------- | ---- |
| cursor | obj   | 游标信息（用于翻页） |      |
| tab    | array | 可用的类型 Tab       |      |
| list   | array | 历史记录列表         |      |

### `cursor` 对象

| 字段     | 类型 | 内容         | 备注                                |
| -------- | ---- | ------------ | ----------------------------------- |
| max      | num  | 游标最大值   | 下一页请求时作为 `max` 参数传入     |
| view_at  | num  | 游标时间戳   | 下一页请求时作为 `view_at` 参数传入 |
| business | str  | 当前业务类型 | 如 `"archive"`                      |
| ps       | num  | 每页数量     |                                     |

### `tab` 数组元素

| 字段 | 类型 | 内容     | 备注                               |
| ---- | ---- | -------- | ---------------------------------- |
| type | str  | 类型标识 | `"archive"`、`"live"`、`"article"` |
| name | str  | 类型名称 | `"视频"`、`"直播"`、`"专栏"`       |

### `list` 数组元素

| 字段        | 类型 | 内容             | 备注                    |
| ----------- | ---- | ---------------- | ----------------------- |
| title       | str  | 视频标题         |                         |
| long_title  | str  | 长标题           | 通常为空                |
| cover       | str  | 封面图地址       |                         |
| covers      | null | 封面列表         | 通常为 null             |
| uri         | str  | 跳转链接         | 番剧/影视可能有值       |
| history     | obj  | 历史记录详情     | 包含核心信息            |
| videos      | num  | 视频数量         |                         |
| author_name | str  | UP主名称         |                         |
| author_face | str  | UP主头像地址     |                         |
| author_mid  | num  | UP主 UID         |                         |
| view_at     | num  | 观看时间戳       | Unix 时间戳（秒）       |
| progress    | num  | 播放进度（秒）   | `-1` 表示已看完或未记录 |
| badge       | str  | 角标             | 如 `"纪录片"`           |
| show_title  | str  | 展示标题         | 部分条目有特殊格式      |
| duration    | num  | 视频总时长（秒） |                         |
| current     | str  | 当前集数         | 通常为空                |
| total       | num  | 总集数           |                         |
| new_desc    | str  | 新描述           | 通常为空                |
| is_finish   | num  | 是否完结         | 1：已完结               |
| is_fav      | num  | 是否已收藏       | 1：已收藏               |
| kid         | num  | 记录 ID          | 唯一标识                |
| tag_name    | str  | 标签名称         | 如 `"翻唱"`、`"日常"`   |
| live_status | num  | 直播状态         | 0：未直播               |

### `history` 对象

| 字段     | 类型 | 内容       | 备注                             |
| -------- | ---- | ---------- | -------------------------------- |
| oid      | num  | 对象 ID    | 视频的 `aid` 或番剧 ID           |
| epid     | num  | 剧集 ID    | 番剧/影视使用                    |
| bvid     | str  | 视频 BV ID | 视频类型时有值                   |
| page     | num  | 分 P 页码  |                                  |
| cid      | num  | 视频 CID   |                                  |
| part     | str  | 分 P 标题  |                                  |
| business | str  | 业务类型   | `"archive"`：视频，`"pgc"`：番剧 |
| dt       | num  | 数据类型   | 2 或 3，可能表示视频类型         |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "cursor": {
            "max": 116830408541952,
            "view_at": 1783744068,
            "business": "archive",
            "ps": 20
        },
        "tab": [
            { "type": "archive", "name": "视频" },
            { "type": "live", "name": "直播" },
            { "type": "article", "name": "专栏" }
        ],
        "list": [
            {
                "title": "视频标题",
                "cover": "http://i2.hdslb.com/bfs/archive/xxx.jpg",
                "history": {
                    "oid": 116890202542351,
                    "bvid": "BV1ucMH6hEtE",
                    "cid": 39795230935,
                    "business": "archive"
                },
                "author_name": "UP主名称",
                "author_mid": 1447574,
                "view_at": 1783750805,
                "progress": 89,
                "duration": 211,
                "is_fav": 1,
                "tag_name": "翻唱"
            }
        ]
    }
}
```

---

## 翻页说明

该接口使用**游标分页**（Cursor-based Pagination），而非传统的页码分页：

1. **首次请求**：`max=0&view_at=0`
2. **后续请求**：使用响应中 `cursor.max` 和 `cursor.view_at` 作为下一次请求的 `max` 和 `view_at` 参数
3. **最后一页**：当 `list` 为空数组时，表示没有更多数据

**示例（翻到下一页）：**

```
GET /x/web-interface/history/cursor?max=116830408541952&view_at=1783744068&business=&ps=20&type=all&web_location=333.1391
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
curl 'https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business=&ps=20&type=all&web_location=333.1391' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **游标分页**：不是传统的 `pn`/`ps` 分页，使用 `max` 和 `view_at` 游标翻页。
2. **`business` 筛选**：
   - 空字符串：全部
   - `"archive"`：仅视频
   - `"live"`：仅直播
   - `"article"`：仅专栏
3. **`progress` 字段**：
   - `-1`：已看完或未记录进度
   - 其他数值：播放进度（秒）
4. **`is_fav`**：1 表示该视频已在收藏夹中。
5. **`badge`**：番剧/影视条目会有角标（如 `"纪录片"`），普通视频为空。
6. **`uri`**：番剧/影视条目会有跳转链接，普通视频为空。


# 2. 历史记录搜索

## 接口描述

在当前登录用户的观看历史记录中进行搜索，支持按关键词、时间范围、视频时长等条件筛选。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于在历史记录中搜索已观看过的内容。

---

## 接口地址

```
GET https://api.bilibili.com/x/web-interface/history/search
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名           | 类型 | 内容               | 必要性   | 备注                                                         |
| ---------------- | ---- | ------------------ | -------- | ------------------------------------------------------------ |
| keyword          | str  | 搜索关键词         | **必要** | URL 编码，如 `%E6%B4%9B%E5%B0%91%E7%88%B7`                   |
| pn               | num  | 页码               | 非必要   | 默认 1                                                       |
| business         | str  | 业务类型           | 非必要   | `"all"`：全部，`"archive"`：视频，`"live"`：直播，`"article"`：专栏 |
| add_time_start   | num  | 添加时间起始       | 非必要   | Unix 时间戳（秒），0 表示不限                                |
| add_time_end     | num  | 添加时间结束       | 非必要   | Unix 时间戳（秒），0 表示不限                                |
| arc_max_duration | num  | 视频最大时长（秒） | 非必要   | 0 表示不限                                                   |
| arc_min_duration | num  | 视频最小时长（秒） | 非必要   | 0 表示不限                                                   |
| device_type      | num  | 设备类型           | 非必要   | 0 表示不限                                                   |
| web_location     | str  | 来源标识           | 非必要   | 固定传 `0.0`                                                 |

**示例请求 URL：**

```
https://api.bilibili.com/x/web-interface/history/search?pn=1&keyword=%E6%B4%9B%E5%B0%91%E7%88%B7&business=all&add_time_start=0&add_time_end=0&arc_max_duration=0&arc_min_duration=0&device_type=0&web_location=0.0
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

| 字段     | 类型  | 内容           | 备注                                |
| -------- | ----- | -------------- | ----------------------------------- |
| has_more | bool  | 是否有更多数据 | `true`：有下一页，`false`：最后一页 |
| page     | obj   | 分页信息       |                                     |
| list     | array | 历史记录列表   | 结构同历史列表接口的 `list` 元素    |

### `page` 对象

| 字段  | 类型 | 内容     | 备注 |
| ----- | ---- | -------- | ---- |
| pn    | num  | 当前页码 |      |
| total | num  | 总记录数 |      |

### `list` 数组元素

与观看历史列表接口中的 `list` 元素结构完全相同，详见该文档。

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "has_more": true,
        "page": {
            "pn": 1,
            "total": 76
        },
        "list": [
            {
                "title": "【洛少爷翻唱】... | 巴拉莱卡",
                "cover": "http://i2.hdslb.com/bfs/archive/xxx.jpg",
                "history": {
                    "oid": 116890202542351,
                    "bvid": "BV1ucMH6hEtE",
                    "cid": 39795230935,
                    "business": "archive"
                },
                "author_name": "洛少爷",
                "author_mid": 1447574,
                "view_at": 1783750955,
                "progress": 2,
                "duration": 211,
                "is_fav": 1,
                "tag_name": "翻唱"
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
curl 'https://api.bilibili.com/x/web-interface/history/search?pn=1&keyword=%E6%B4%9B%E5%B0%91%E7%88%B7&business=all&add_time_start=0&add_time_end=0&arc_max_duration=0&arc_min_duration=0&device_type=0&web_location=0.0' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **页码分页**：该接口使用传统的 `pn`（页码）分页，与历史列表接口的游标分页不同。
2. **关键词必须携带**：`keyword` 为空时，该接口行为可能异常或返回空列表。
3. **`business` 筛选**：
   - `"all"`：全部
   - `"archive"`：仅视频
   - `"live"`：仅直播
   - `"article"`：仅专栏
4. **`add_time_start` / `add_time_end`**：用于筛选特定时间段内观看的记录，单位为秒。
5. **`arc_max_duration` / `arc_min_duration`**：仅对视频类型有效，单位为秒。
6. **搜索范围**：该接口仅搜索当前用户的观看历史记录，而非全站搜索。


# 3. 移除单条历史记录

## 接口描述

从当前登录用户的观看历史中移除单条记录。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于历史记录管理。

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/delete
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名 | 类型 | 内容            | 必要性   | 备注                                                    |
| ------ | ---- | --------------- | -------- | ------------------------------------------------------- |
| kid    | str  | 历史记录条目 ID | **必要** | 格式为 `{business}_{oid}`，如 `archive_116899698449221` |
| csrf   | str  | CSRF Token      | **必要** | 位于 Cookie 中的 `bili_jct`                             |

**示例请求体：**

```
kid=archive_116899698449221&csrf=40bc00dc2d06cb9fdc96b22b2d9377a9
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
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| -404   | 记录不存在                               |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/delete' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'kid=archive_116899698449221' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **`kid` 参数格式**：`{business}_{oid}`，其中 `business` 为历史记录业务类型（`archive`=视频，`live`=直播，`article`=专栏），`oid` 为历史记录条目 ID（可从历史记录列表接口的 `kid` 字段获取）。
2. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
4. **幂等性**：若记录已被删除或不存在，再次调用会返回错误码。


# 4. 清空全部历史记录

## 接口描述

清空当前登录用户的全部观看历史记录。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于历史记录管理。

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/clear
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名   | 类型 | 内容       | 必要性   | 备注                                                         |
| -------- | ---- | ---------- | -------- | ------------------------------------------------------------ |
| business | str  | 业务类型   | 非必要   | 空字符串表示清空全部类型；`"archive"`：仅清空视频，`"live"`：仅清空直播，`"article"`：仅清空专栏 |
| csrf     | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值                               |

**示例请求体：**

```
business=&csrf=40bc00dc2d06cb9fdc96b22b2d9377a9
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
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/clear' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'business=' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **`business` 参数**：空字符串表示清空全部；指定类型则仅清空该类型的历史记录。
2. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
4. **不可逆操作**：清空后无法恢复，请谨慎使用。
5. **接口区分**：
   - `/x/v2/history/delete`：删除单条历史记录
   - `/x/v2/history/clear`：清空全部历史记录


## 相关接口汇总

| 功能         | 接口路径                          | 请求方式 | WBI 签名 |
| ------------ | --------------------------------- | -------- | -------- |
| 观看历史列表 | `/x/web-interface/history/cursor` | GET      | ❌        |
| 历史记录搜索 | `/x/web-interface/history/search` | GET      | ❌        |
| 移除单条历史 | `/x/v2/history/delete`            | POST     | ❌        |
| 清空全部历史 | `/x/v2/history/clear`             | POST     | ❌        |
