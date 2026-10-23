# 黑名单管理 API

## 接口列表

### 1. 黑名单列表查询
### 2. 添加黑名单（拉黑）
### 3. 移除黑名单（取消拉黑）

---

# 1. 黑名单列表查询

## 接口描述

获取当前登录用户的黑名单列表，支持分页查询。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示用户已拉黑的账号列表。

---

## 接口地址

```
GET https://api.bilibili.com/x/relation/blacks
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注                         |
| --------------- | ---- | ---------- | ------ | ---------------------------- |
| pn              | num  | 页码       | 非必要 | 默认 1                       |
| ps              | num  | 每页数量   | 非必要 | 默认 20                      |
| re_version      | num  | 版本号     | 非必要 | 固定传 `0` 即可              |
| jsonp           | str  | JSONP 回调 | 非必要 | 固定传 `jsonp`，历史遗留参数 |
| web_location    | str  | 来源标识   | 非必要 | 固定传 `0.0`                 |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1`                   |

**示例请求 URL：**

```
https://api.bilibili.com/x/relation/blacks?pn=1&ps=20&re_version=0&jsonp=jsonp&web_location=0.0&x-bili-redirect=1
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

| 字段       | 类型  | 内容           | 备注                   |
| ---------- | ----- | -------------- | ---------------------- |
| list       | array | 黑名单用户列表 | 每个元素为一个用户对象 |
| total      | num   | 黑名单总人数   |                        |
| re_version | num   | 版本号         |                        |

### `list` 数组元素

| 字段            | 类型 | 内容          | 备注              |
| --------------- | ---- | ------------- | ----------------- |
| mid             | num  | 用户 UID      |                   |
| uname           | str  | 用户昵称      |                   |
| face            | str  | 头像地址      |                   |
| sign            | str  | 用户签名      | 可能为空          |
| face_nft        | num  | 是否 NFT 头像 | 0：否             |
| handle          | str  | 用户 handle   | 通常为空          |
| attribute       | num  | 属性位        | `128` 表示已拉黑  |
| mtime           | num  | 拉黑时间戳    | Unix 时间戳（秒） |
| tag             | null | 标签          | 通常为 null       |
| special         | num  | 特殊标记      | 0 表示无          |
| official_verify | obj  | 官方认证信息  |                   |
| vip             | obj  | 大会员信息    |                   |
| name_render     | obj  | 昵称渲染      | 通常为空对象      |
| nft_icon        | str  | NFT 图标      |                   |
| rec_reason      | str  | 推荐理由      | 通常为空          |
| track_id        | str  | 追踪 ID       | 通常为空          |
| follow_time     | str  | 关注时间      | 通常为空          |

### `official_verify` 对象

| 字段 | 类型 | 内容     | 备注      |
| ---- | ---- | -------- | --------- |
| type | num  | 认证类型 | 0：未认证 |
| desc | str  | 认证描述 |           |

### `vip` 对象

| 字段                 | 类型 | 内容         | 备注        |
| -------------------- | ---- | ------------ | ----------- |
| vipType              | num  | 大会员类型   | 0：非大会员 |
| vipDueDate           | num  | 到期时间戳   |             |
| dueRemark            | str  | 到期备注     |             |
| accessStatus         | num  | 访问状态     |             |
| vipStatus            | num  | 大会员状态   | 0：无效     |
| vipStatusWarn        | str  | 状态警告     |             |
| themeType            | num  | 主题类型     |             |
| label                | obj  | 标签信息     | 空对象      |
| avatar_subscript     | num  | 头像角标     |             |
| nickname_color       | str  | 昵称颜色     |             |
| avatar_subscript_url | str  | 头像角标地址 |             |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": [
            {
                "mid": 1029014093,
                "attribute": 128,
                "mtime": 1783132757,
                "tag": null,
                "special": 0,
                "uname": "bili_39343073317",
                "face": "https://i0.hdslb.com/bfs/face/member/noface.jpg",
                "sign": "",
                "face_nft": 0,
                "handle": "",
                "official_verify": {
                    "type": 0,
                    "desc": ""
                },
                "vip": {
                    "vipType": 0,
                    "vipDueDate": 0,
                    "dueRemark": "",
                    "accessStatus": 0,
                    "vipStatus": 0,
                    "vipStatusWarn": "",
                    "themeType": 0,
                    "label": {
                        "path": "",
                        "text": "",
                        "label_theme": "",
                        "text_color": "",
                        "bg_style": 0,
                        "bg_color": "",
                        "border_color": ""
                    },
                    "avatar_subscript": 0,
                    "nickname_color": "",
                    "avatar_subscript_url": ""
                },
                "name_render": {},
                "nft_icon": "",
                "rec_reason": "",
                "track_id": "",
                "follow_time": ""
            }
        ],
        "re_version": 0,
        "total": 10
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
curl 'https://api.bilibili.com/x/relation/blacks?pn=1&ps=20&re_version=0&jsonp=jsonp&web_location=0.0&x-bili-redirect=1' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口目前不需要 WBI 签名，直接 GET 即可。
2. **`attribute=128`**：表示该用户处于黑名单中，是判断拉黑状态的关键字段。
3. **`mtime`**：拉黑时间戳（秒级），可用于排序。
4. **分页**：`ps` 最大可能为 50，建议使用 20。
5. **黑名单上限**：
   - 粉丝量 < 1 万：上限 1000 人
   - 粉丝量 ≥ 1 万：上限 10000 人

---

# 2. 添加黑名单（拉黑）

## 接口描述

将指定用户加入当前登录用户的黑名单（拉黑）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于黑名单管理。

---

## 接口地址

```
POST https://api.bilibili.com/x/relation/modify
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注                                                         |
| --------------- | ---- | ---------- | ------ | ------------------------------------------------------------ |
| statistics      | str  | 统计信息   | 非必要 | URL 编码的 JSON，如 `%7B%22appId%22:100,%22platform%22:5%7D` |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1`                                                   |


## 请求参数（表单数据 `x-www-form-urlencoded`）

| 参数名 | 类型 | 内容         | 必要性   | 备注                           |
| ------ | ---- | ------------ | -------- | ------------------------------ |
| fid    | num  | 目标用户 UID | **必要** | 要拉黑的用户 ID                |
| act    | num  | 操作类型     | **必要** | `5` 表示添加黑名单             |
| csrf   | str  | CSRF Token   | **必要** | 位于 Cookie 中的 `bili_jct` 值 |
| re_src | num  | 操作来源     | 非必要   | 固定传 `116`                   |
| jsonp  | str  | JSONP 回调   | 非必要   | 固定传 `jsonp`                 |

**示例请求体：**

```
fid=1029014093&csrf=1eaefa721216ddee6444fcbedace61b2&act=5&re_src=116&jsonp=jsonp
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1
}
```

**响应示例（已拉黑）：**

```json
{
    "code": -404,
    "message": "已拉黑，请勿重复操作",
    "ttl": 1
}
```

**响应示例（达到上限）：**

```json
{
    "code": -304,
    "message": "黑名单人数已达上限",
    "ttl": 1
}
```

> **注意**：以上错误码为根据常见接口规律推测，实际以抓包为准。

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -304   | 黑名单人数已达上限                       |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| -404   | 目标用户已在黑名单中                     |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/relation/modify?statistics=%7B%22appId%22:100,%22platform%22:5%7D' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'fid=1029014093' \
  --data-urlencode 'csrf=xxx' \
  --data-urlencode 'act=5' \
  --data-urlencode 're_src=116' \
  --data-urlencode 'jsonp=jsonp'
```

---

## 注意事项

1. **`act` 参数区分**：
   - `act=5`：添加黑名单（拉黑）
   - `act=6`：移除黑名单（取消拉黑）
2. **黑名单上限**：
   - 粉丝量 < 1 万：上限 1000 人
   - 粉丝量 ≥ 1 万：上限 10000 人
3. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
4. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
5. **幂等性**：如果目标用户已在黑名单中，再次调用会返回错误码 `-404`。
6. **与移除操作共用接口**：`/x/relation/modify` 同时承担添加和移除黑名单的功能，通过 `act` 参数区分。

---

# 3. 移除黑名单（取消拉黑）

## 接口描述

将指定用户从当前登录用户的黑名单中移除（取消拉黑）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于黑名单管理。

---

## 接口地址

```
POST https://api.bilibili.com/x/relation/modify
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注       |
| --------------- | ---- | ---------- | ------ | ---------- |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1` |

---

## 请求参数（表单数据 `x-www-form-urlencoded`）

| 参数名 | 类型 | 内容         | 必要性   | 备注                           |
| ------ | ---- | ------------ | -------- | ------------------------------ |
| fid    | num  | 目标用户 UID | **必要** | 要移除黑名单的用户 ID          |
| act    | num  | 操作类型     | **必要** | `6` 表示移除黑名单             |
| csrf   | str  | CSRF Token   | **必要** | 位于 Cookie 中的 `bili_jct` 值 |
| re_src | num  | 操作来源     | 非必要   | 固定传 `116`                   |
| jsonp  | str  | JSONP 回调   | 非必要   | 固定传 `jsonp`                 |

**示例请求体：**

```
fid=1029014093&csrf=1eaefa721216ddee6444fcbedace61b2&act=6&re_src=116&jsonp=jsonp
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1
}
```

**响应示例（失败，不在黑名单中）：**

```json
{
    "code": -404,
    "message": "对方不在你的黑名单中",
    "ttl": 1
}
```

**响应示例（CSRF 验证失败）：**

```json
{
    "code": -403,
    "message": "访问权限不足",
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
| -404   | 目标用户不在黑名单中                     |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/relation/modify?x-bili-redirect=1' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'fid=1029014093' \
  --data-urlencode 'csrf=xxx' \
  --data-urlencode 'act=6' \
  --data-urlencode 're_src=116' \
  --data-urlencode 'jsonp=jsonp'
```

---

## 注意事项

1. **`act` 参数区分**：
   - `act=5`：添加黑名单（拉黑）
   - `act=6`：移除黑名单（取消拉黑）
2. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
3. **无需 WBI 签名**：该接口目前不需要 WBI 签名。
4. **幂等性**：如果目标用户已不在黑名单中，再次调用会返回错误码 `-404`。
5. **与添加操作共用接口**：`/x/relation/modify` 同时承担添加和移除黑名单的功能，通过 `act` 参数区分。


## 相关接口汇总

| 功能       | 接口路径             | 请求方式 | 签名 | 关键参数               |
| ---------- | -------------------- | -------- | ---- | ---------------------- |
| 黑名单列表 | `/x/relation/blacks` | GET      | 无   | `pn`、`ps`             |
| 添加黑名单 | `/x/relation/modify` | POST     | 无   | `act=5`、`fid`、`csrf` |
| 移除黑名单 | `/x/relation/modify` | POST     | 无   | `act=6`、`fid`、`csrf` |
