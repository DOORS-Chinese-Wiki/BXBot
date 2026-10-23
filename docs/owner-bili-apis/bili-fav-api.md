# 收藏夹 API

## 接口列表

1. 获取用户创建的收藏夹列表
2. 获取收藏夹内容列表
3. 创建收藏夹
4. 修改收藏夹
5. 删除收藏夹
6. 添加/删除收藏夹资源
7. 批量删除收藏夹资源
8. 复制收藏夹资源
9. 移动收藏夹资源

---

# 1. 获取用户创建的收藏夹列表

## 接口描述

获取当前登录用户创建的所有收藏夹列表，用于在收藏视频时展示可选收藏夹。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于获取用户创建的收藏夹列表。

---

## 接口地址

```
GET https://api.bilibili.com/x/v3/fav/folder/created/list-all
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容      | 必要性   | 备注           |
| ------------ | ---- | --------- | -------- | -------------- |
| type         | num  | 资源类型  | 非必要   | `2` 表示视频   |
| rid          | num  | 资源 ID   | 非必要   | 视频 AV ID     |
| up_mid       | num  | UP 主 UID | **必要** | 视频 UP 主 UID |
| web_location | str  | 来源标识  | 非必要   | 固定传 `0.0`   |

**示例请求 URL：**

```
https://api.bilibili.com/x/v3/fav/folder/created/list-all?type=2&rid=116883860818880&up_mid=3690995472402999&web_location=0.0
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

| 字段   | 类型  | 内容       | 备注        |
| ------ | ----- | ---------- | ----------- |
| count  | num   | 收藏夹总数 |             |
| list   | array | 收藏夹列表 |             |
| season | null  | 剧集信息   | 通常为 null |

### `list` 数组元素

| 字段              | 类型 | 内容                 | 备注          |
| ----------------- | ---- | -------------------- | ------------- |
| id                | num  | 收藏夹 ID（完整 ID） | 用于 API 操作 |
| fid               | num  | 收藏夹 ID（短 ID）   | 用于 URL 展示 |
| mid               | num  | 用户 UID             |               |
| attr              | num  | 收藏夹属性           | 见下方说明    |
| title             | str  | 收藏夹名称           |               |
| fav_state         | num  | 收藏状态             | 0：未收藏     |
| media_count       | num  | 收藏夹内视频数量     |               |
| is_kid_playlist   | bool | 是否儿童播放列表     |               |
| kid_playlist_desc | str  | 儿童播放列表描述     |               |

**`attr` 属性说明：**

| 值   | 含义                 |
| ---- | -------------------- |
| 20   | 默认收藏夹（未分类） |
| 22   | 普通收藏夹           |
| 2    | 公开收藏夹           |
| 55   | 私有收藏夹           |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "count": 12,
        "list": [
            {
                "id": 3784180099,
                "fid": 37841800,
                "mid": 3690995472402999,
                "attr": 20,
                "title": "未分类",
                "fav_state": 0,
                "media_count": 18,
                "is_kid_playlist": false,
                "kid_playlist_desc": ""
            },
            {
                "id": 3980707099,
                "fid": 39807070,
                "mid": 3690995472402999,
                "attr": 55,
                "title": "123",
                "fav_state": 0,
                "media_count": 0,
                "is_kid_playlist": false,
                "kid_playlist_desc": ""
            }
        ],
        "season": null
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
curl 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?type=2&rid=116883860818880&up_mid=3690995472402999&web_location=0.0' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`type=2`**：表示视频资源，为常用值。
3. **`rid` 和 `up_mid`**：通常用于在视频页面调用，用于判断该视频是否已收藏到各收藏夹。


# 2. 获取收藏夹内容列表

## 接口描述

获取指定收藏夹中的视频资源列表，支持分页和排序。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于查看收藏夹内容。

---

## 接口地址

```
GET https://api.bilibili.com/x/v3/fav/resource/list
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容      | 必要性   | 备注                                       |
| ------------ | ---- | --------- | -------- | ------------------------------------------ |
| media_id     | num  | 收藏夹 ID | **必要** | 收藏夹的 `id` 或 `fid`                     |
| pn           | num  | 页码      | 非必要   | 默认 1                                     |
| ps           | num  | 每页数量  | 非必要   | 默认 20，最大 40                           |
| keyword      | str  | 关键词    | 非必要   | 搜索收藏夹内视频                           |
| order        | str  | 排序方式  | 非必要   | `mtime`：按收藏时间，`pubtime`：按发布时间 |
| type         | num  | 资源类型  | 非必要   | `0` 表示全部                               |
| tid          | num  | 分区 ID   | 非必要   | `0` 表示全部                               |
| platform     | str  | 平台标识  | 非必要   | `web`                                      |
| web_location | str  | 来源标识  | 非必要   | `0.0`                                      |

**示例请求 URL：**

```
https://api.bilibili.com/x/v3/fav/resource/list?media_id=4051071199&pn=1&ps=40&keyword=&order=mtime&type=0&tid=0&platform=web&web_location=0.0
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

| 字段     | 类型  | 内容       | 备注           |
| -------- | ----- | ---------- | -------------- |
| info     | obj   | 收藏夹信息 |                |
| medias   | array | 视频列表   |                |
| has_more | bool  | 是否有更多 | `true`/`false` |
| ttl      | num   | 缓存时间   |                |

### `info` 对象

| 字段        | 类型 | 内容        | 备注 |
| ----------- | ---- | ----------- | ---- |
| id          | num  | 收藏夹 ID   |      |
| fid         | num  | 收藏夹短 ID |      |
| mid         | num  | 用户 UID    |      |
| attr        | num  | 收藏夹属性  |      |
| title       | str  | 收藏夹名称  |      |
| cover       | str  | 封面图地址  |      |
| upper       | obj  | UP 主信息   |      |
| cover_type  | num  | 封面类型    |      |
| cnt_info    | obj  | 统计信息    |      |
| type        | num  | 类型        |      |
| intro       | str  | 简介        |      |
| ctime       | num  | 创建时间戳  |      |
| mtime       | num  | 修改时间戳  |      |
| media_count | num  | 视频总数    |      |
| is_top      | bool | 是否置顶    |      |

### `medias` 数组元素

| 字段     | 类型 | 内容                  | 备注             |
| -------- | ---- | --------------------- | ---------------- |
| id       | num  | 资源 ID（视频 AV ID） |                  |
| type     | num  | 资源类型              | `2` 表示视频     |
| title    | str  | 视频标题              |                  |
| cover    | str  | 封面图地址            |                  |
| intro    | str  | 简介                  |                  |
| page     | num  | 分 P 页码             |                  |
| duration | num  | 视频时长（秒）        |                  |
| upper    | obj  | UP 主信息             |                  |
| attr     | num  | 属性                  |                  |
| cnt_info | obj  | 统计信息              |                  |
| ctime    | num  | 创建时间戳            |                  |
| pubtime  | num  | 发布时间戳            |                  |
| fav_time | num  | 收藏时间戳            |                  |
| bvid     | str  | 视频 BV ID            |                  |
| bv_id    | str  | 视频 BV ID（别名）    |                  |
| ugc      | obj  | UGC 信息              | 包含 `first_cid` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "info": {
            "id": 4051071199,
            "fid": 40510711,
            "title": "春晚名单",
            "media_count": 17
        },
        "medias": [
            {
                "id": 116867335325336,
                "type": 2,
                "title": "水球炸弹挑战，室友非酋附体，太刺激了！",
                "cover": "http://i1.hdslb.com/bfs/archive/xxx.jpg",
                "duration": 96,
                "upper": {
                    "mid": 1938121503,
                    "name": "峻宁峻宁"
                },
                "cnt_info": {
                    "play": 456418,
                    "collect": 7174
                },
                "fav_time": 1783414696,
                "bvid": "BV1LAT26VEsa"
            }
        ],
        "has_more": false
    }
}
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`media_id` 来源**：从收藏夹列表接口的 `id` 或 `fid` 字段获取，两者均可。
3. **分页限制**：`ps` 最大为 40，超过可能被截断。
4. **`order` 排序**：`mtime`（按收藏时间排序，最新在前），`pubtime`（按发布时间排序）。


# 3. 创建收藏夹

## 接口描述

为当前登录用户创建新的收藏夹。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于创建收藏夹。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/folder/add
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名  | 类型 | 内容       | 必要性   | 备注                        |
| ------- | ---- | ---------- | -------- | --------------------------- |
| title   | str  | 收藏夹名称 | **必要** | 最长 20 字符？              |
| intro   | str  | 收藏夹简介 | 非必要   |                             |
| privacy | num  | 隐私设置   | 非必要   | `0`：公开，`1`：私密        |
| cover   | str  | 封面图地址 | 非必要   | 通常为空                    |
| csrf    | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` |

**示例请求体：**

```
title=1&intro=Description&privacy=0&cover=&csrf=1eaefa721216ddee6444fcbedace61b2
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

| 字段        | 类型 | 内容        | 备注    |
| ----------- | ---- | ----------- | ------- |
| id          | num  | 收藏夹 ID   | 完整 ID |
| fid         | num  | 收藏夹短 ID |         |
| mid         | num  | 用户 UID    |         |
| attr        | num  | 收藏夹属性  |         |
| title       | str  | 收藏夹名称  |         |
| cover       | str  | 封面图地址  |         |
| upper       | obj  | UP 主信息   |         |
| cover_type  | num  | 封面类型    |         |
| cnt_info    | obj  | 统计信息    |         |
| type        | num  | 类型        |         |
| intro       | str  | 简介        |         |
| ctime       | num  | 创建时间戳  |         |
| mtime       | num  | 修改时间戳  |         |
| state       | num  | 状态        |         |
| fav_state   | num  | 收藏状态    |         |
| like_state  | num  | 点赞状态    |         |
| media_count | num  | 视频数量    |         |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "id": 3980707099,
        "fid": 39807070,
        "mid": 3690995472402999,
        "attr": 6,
        "title": "1",
        "intro": "Description",
        "media_count": 0
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 操作成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -403   | CSRF 验证失败               |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v3/fav/folder/add' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'title=我的收藏夹' \
  --data-urlencode 'intro=这是我的收藏夹简介' \
  --data-urlencode 'privacy=0' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
2. **无需 WBI 签名**：该接口不需要 WBI 签名。
3. **`privacy` 参数**：`0` 为公开，`1` 为私密。公开收藏夹会出现在个人空间。


# 4. 修改收藏夹

## 接口描述

修改当前登录用户创建的收藏夹信息（名称、简介、隐私设置等）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于编辑收藏夹。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/folder/edit
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名   | 类型 | 内容       | 必要性   | 备注                        |
| -------- | ---- | ---------- | -------- | --------------------------- |
| media_id | num  | 收藏夹 ID  | **必要** | 要修改的收藏夹 ID           |
| title    | str  | 新名称     | 非必要   |                             |
| intro    | str  | 新简介     | 非必要   |                             |
| privacy  | num  | 隐私设置   | 非必要   | `0`：公开，`1`：私密        |
| cover    | str  | 封面图地址 | 非必要   |                             |
| csrf     | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` |

**示例请求体：**

```
media_id=3980707099&title=123&intro=Descriptions&privacy=1&cover=&csrf=1eaefa721216ddee6444fcbedace61b2
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

与创建收藏夹返回的 `data` 结构相同。

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "id": 3980707099,
        "fid": 39807070,
        "mid": 3690995472402999,
        "attr": 55,
        "title": "123",
        "intro": "Descriptions",
        "media_count": 0
    }
}
```

---

## 注意事项

1. **`media_id` 来源**：从收藏夹列表接口的 `id` 字段获取。
2. **参数可选**：只需传入需要修改的字段，未传的字段保持不变。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。
4. **特殊收藏夹**：未分类收藏夹可修改，不能删除。


# 5. 删除收藏夹

## 接口描述

删除当前登录用户创建的收藏夹。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于删除收藏夹。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/folder/del
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data` 或 `application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名    | 类型 | 内容       | 必要性   | 备注                        |
| --------- | ---- | ---------- | -------- | --------------------------- |
| media_ids | num  | 收藏夹 ID  | **必要** | 要删除的收藏夹 ID           |
| platform  | str  | 平台标识   | 非必要   | `web`                       |
| csrf      | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` |

**示例请求体：**

```
media_ids=3980707099&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型    | 内容     | 备注       |
| ------- | ------- | -------- | ---------- |
| code    | num     | 状态码   | 0 表示成功 |
| message | str     | 状态信息 | `"OK"`     |
| ttl     | num     | 1        |            |
| data    | num/obj | 数据     | 通常为 `0` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 0
}
```

---

## 注意事项

1. **不可逆操作**：删除收藏夹后无法恢复，其中的收藏视频不会被删除，只是移除了收藏夹关系。
2. **`media_ids` 参数名**：注意是 `media_ids`（复数），即使只删除一个也使用此参数名。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。
4. **特殊收藏夹**：未分类收藏夹不能删除。


# 6. 添加/删除收藏夹资源

## 接口描述

向指定收藏夹添加视频或从指定收藏夹移除视频（统一接口，通过参数区分操作）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于收藏/取消收藏视频。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/resource/deal
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名        | 类型 | 内容            | 必要性   | 备注                        |
| ------------- | ---- | --------------- | -------- | --------------------------- |
| rid           | num  | 资源 ID         | **必要** | 视频 AV ID（`aid`）         |
| type          | num  | 资源类型        | **必要** | `2` 表示视频                |
| add_media_ids | str  | 添加到收藏夹 ID | 二选一   | 多个用逗号分隔              |
| del_media_ids | str  | 从收藏夹移除 ID | 二选一   | 多个用逗号分隔              |
| platform      | str  | 平台标识        | 非必要   | `web`                       |
| from_spmid    | str  | 来源标识        | 非必要   |                             |
| spmid         | str  | 来源标识        | 非必要   |                             |
| statistics    | str  | 统计信息        | 非必要   | URL 编码的 JSON             |
| csrf          | str  | CSRF Token      | **必要** | 位于 Cookie 中的 `bili_jct` |

> **说明**：`add_media_ids` 和 `del_media_ids` 至少传一个。如果同时传入，则同时执行添加和删除操作。

**示例请求体（添加收藏）：**

```
rid=116883860818880&type=2&add_media_ids=3980707099&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

**示例请求体（取消收藏）：**

```
rid=116883860818880&type=2&del_media_ids=3980707099&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
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

| 字段        | 类型 | 内容     | 备注        |
| ----------- | ---- | -------- | ----------- |
| prompt      | bool | 是否提示 |             |
| ga_data     | null | 数据     | 通常为 null |
| toast_msg   | str  | 提示消息 |             |
| success_num | num  | 成功数量 |             |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "prompt": true,
        "ga_data": null,
        "toast_msg": "",
        "success_num": 0
    }
}
```

---

## 注意事项

1. **添加与删除共用接口**：通过 `add_media_ids` 和 `del_media_ids` 区分。
2. **`add_media_ids` 格式**：多个收藏夹 ID 用英文逗号分隔，如 `123,456,789`。
3. **`rid` 与 `type`**：`rid` 为视频 AV ID，`type=2` 表示视频资源。
4. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。


# 7. 批量删除收藏夹资源

## 接口描述

从指定收藏夹中批量移除多个视频。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于批量取消收藏视频。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/resource/batch-del
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名    | 类型 | 内容       | 必要性   | 备注                                    |
| --------- | ---- | ---------- | -------- | --------------------------------------- |
| resources | str  | 资源列表   | **必要** | 格式：`{资源ID}:{类型}`，多个用逗号分隔 |
| media_id  | num  | 收藏夹 ID  | **必要** |                                         |
| platform  | str  | 平台标识   | 非必要   | `web`                                   |
| csrf      | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct`             |

**示例请求体（删除单个）：**

```
resources=116821667676986:2&media_id=3980707099&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

**示例请求体（删除多个）：**

```
resources=115987739446417:2,116867335325336:2&media_id=3980707099&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |
| data    | num  | 数据     | 通常为 `0` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 0
}
```

---

## 注意事项

1. **`resources` 参数格式**：`{资源ID}:{类型}`，多个用英文逗号分隔，**不含空格**。
2. **资源类型**：`2` 表示视频。
3. **与 `/deal` 接口的区别**：
   - `/deal`：添加/删除收藏夹资源（单次操作一个视频）
   - `/batch-del`：批量删除收藏夹资源（一次删除多个视频）
4. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。


# 8. 复制收藏夹资源

## 接口描述

将视频从源收藏夹复制到目标收藏夹。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于在收藏夹之间复制资源。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/resource/copy
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名       | 类型 | 内容          | 必要性   | 备注                                    |
| ------------ | ---- | ------------- | -------- | --------------------------------------- |
| resources    | str  | 资源列表      | **必要** | 格式：`{资源ID}:{类型}`，多个用逗号分隔 |
| src_media_id | num  | 源收藏夹 ID   | **必要** |                                         |
| tar_media_id | num  | 目标收藏夹 ID | **必要** |                                         |
| mid          | num  | 用户 UID      | **必要** | 当前用户 UID                            |
| platform     | str  | 平台标识      | 非必要   | `web`                                   |
| csrf         | str  | CSRF Token    | **必要** | 位于 Cookie 中的 `bili_jct`             |

**示例请求体：**

```
resources=116867335325336:2&src_media_id=4051071199&tar_media_id=3980707099&mid=3690995472402999&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |
| data    | num  | 数据     | 通常为 `0` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 0
}
```

---

## 注意事项

1. **复制 vs 移动**：复制会在目标收藏夹中新增一份资源，源收藏夹保留原资源。
2. **`mid` 参数**：当前用户的 UID，从 Cookie 中的 `DedeUserID` 获取。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。


# 9. 移动收藏夹资源

## 接口描述

将视频从源收藏夹移动到目标收藏夹（从源收藏夹移除并添加到目标收藏夹）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于在收藏夹之间移动资源。

---

## 接口地址

```
POST https://api.bilibili.com/x/v3/fav/resource/move
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名       | 类型 | 内容          | 必要性   | 备注                                    |
| ------------ | ---- | ------------- | -------- | --------------------------------------- |
| resources    | str  | 资源列表      | **必要** | 格式：`{资源ID}:{类型}`，多个用逗号分隔 |
| src_media_id | num  | 源收藏夹 ID   | **必要** |                                         |
| tar_media_id | num  | 目标收藏夹 ID | **必要** |                                         |
| mid          | num  | 用户 UID      | **必要** | 当前用户 UID                            |
| platform     | str  | 平台标识      | 非必要   | `web`                                   |
| csrf         | str  | CSRF Token    | **必要** | 位于 Cookie 中的 `bili_jct`             |

**示例请求体：**

```
resources=116867335325336:2&src_media_id=3980707099&tar_media_id=4051071199&mid=3690995472402999&platform=web&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |
| data    | num  | 数据     | 通常为 `0` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 0
}
```

---

## 注意事项

1. **移动 vs 复制**：移动会从源收藏夹移除资源，仅保留在目标收藏夹中。
2. **`mid` 参数**：当前用户的 UID，从 Cookie 中的 `DedeUserID` 获取。
3. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数。
4. **与 `/copy` 接口参数一致**：仅接口路径和语义不同。


## 相关接口汇总

| 功能                     | 接口路径                                | 请求方式 | CSRF |
| ------------------------ | --------------------------------------- | -------- | ---- |
| 获取用户创建的收藏夹列表 | `GET /x/v3/fav/folder/created/list-all` | GET      | ❌    |
| 获取收藏夹内容列表       | `GET /x/v3/fav/resource/list`           | GET      | ❌    |
| 创建收藏夹               | `POST /x/v3/fav/folder/add`             | POST     | ✅    |
| 修改收藏夹               | `POST /x/v3/fav/folder/edit`            | POST     | ✅    |
| 删除收藏夹               | `POST /x/v3/fav/folder/del`             | POST     | ✅    |
| 添加/删除收藏夹资源      | `POST /x/v3/fav/resource/deal`          | POST     | ✅    |
| 批量删除收藏夹资源       | `POST /x/v3/fav/resource/batch-del`     | POST     | ✅    |
| 复制收藏夹资源           | `POST /x/v3/fav/resource/copy`          | POST     | ✅    |
| 移动收藏夹资源           | `POST /x/v3/fav/resource/move`          | POST     | ✅    |
