# 硬币系统 API

## 接口列表

### 1. 硬币余额查询
### 2. 硬币收支记录查询
### 3. 今日投币经验查询
### 4. 用户投币视频列表

---

# 1. 硬币余额查询

## 接口描述

获取当前登录用户的硬币余额。

> 该接口位于账号域名 `account.bilibili.com`，用于查询用户持有的硬币数量（B站免费货币，用于投币支持UP主等）。

---

## 接口地址

```
GET https://account.bilibili.com/site/getCoin
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容       | 必要性 | 备注                                   |
| --------------- | ---- | ---------- | ------ | -------------------------------------- |
| web_location    | str  | 来源标识   | 非必要 | 固定传 `333.33` 即可，可能用于统计来源 |
| x-bili-redirect | str  | 重定向标识 | 非必要 | 固定传 `1`                             |

**示例请求 URL：**

```
https://account.bilibili.com/site/getCoin?web_location=333.33&x-bili-redirect=1
```

---

## 响应结构

### 根对象

| 字段   | 类型 | 内容     | 备注                                                 |
| ------ | ---- | -------- | ---------------------------------------------------- |
| code   | num  | 状态码   | 0 表示成功                                           |
| status | bool | 状态标识 | `true` / `false`（疑似历史遗留字段，以 `code` 为准） |
| data   | obj  | 数据本体 |                                                      |

### `data` 对象

| 字段  | 类型 | 内容         | 备注                                 |
| ----- | ---- | ------------ | ------------------------------------ |
| money | num  | 当前硬币余额 | 单位：个，保留一位小数（如 `130.5`） |

**响应示例（成功）：**

```json
{
    "code": 0,
    "status": true,
    "data": {
        "money": 130.5
    }
}
```

---

## 错误码

| 状态码 | 含义                                                  |
| ------ | ----------------------------------------------------- |
| 0      | 请求成功                                              |
| -101   | 未登录（Cookie 无效或过期）                           |
| 其他   | 参见 `message` 字段（实际响应中可能不返回 `message`） |

---

## 调用示例（curl）

```bash
curl 'https://account.bilibili.com/site/getCoin?web_location=333.33&x-bili-redirect=1' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **硬币 ≠ B币**：硬币是B站免费货币，每日登录可获取（移动端1枚/天，PC端1枚/天），用于投币支持UP主；B币是充值货币，1 B币 = 1 元。
2. **精度**：硬币余额可能为小数（如 `130.5`），因为投币时可以投 0.5 枚（部分场景）。
3. **`status` 字段**：疑似历史遗留字段，实际是否成功应以 `code` 为准（`code=0` 为成功）。
4. **认证**：必须携带有效的 `SESSDATA` Cookie，否则返回 `-101`。


# 2. 硬币收支记录查询

## 接口描述

获取当前登录用户的硬币收支明细记录，包含收入（如登录奖励）和支出（如投币打赏、活动扣除等）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示硬币变动日志。

---

## 接口地址

```
GET https://api.bilibili.com/x/member/web/coin/log
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容           | 必要性 | 备注                               |
| --------------- | ---- | -------------- | ------ | ---------------------------------- |
| jsonp           | str  | JSONP 回调标识 | 非必要 | 固定传 `jsonp`，可能为历史遗留参数 |
| web_location    | str  | 来源标识       | 非必要 | 固定传 `333.33` 即可               |
| x-bili-redirect | str  | 重定向标识     | 非必要 | 固定传 `1`                         |

> **说明**：该接口目前似乎不支持分页参数，仅返回最近若干条记录。具体条数限制需进一步验证。

**示例请求 URL：**

```
https://api.bilibili.com/x/member/web/coin/log?jsonp=jsonp&web_location=333.33&x-bili-redirect=1
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

| 字段  | 类型  | 内容         | 备注               |
| ----- | ----- | ------------ | ------------------ |
| list  | array | 硬币记录列表 | 每条记录为一个对象 |
| count | num   | 记录总数     | 当前返回的记录条数 |

### `list` 数组元素

| 字段   | 类型 | 内容     | 备注                                   |
| ------ | ---- | -------- | -------------------------------------- |
| time   | str  | 变动时间 | 格式 `YYYY-MM-DD HH:mm:ss`             |
| delta  | num  | 变动数量 | 正数表示收入，负数表示支出             |
| reason | str  | 变动原因 | 如 `"登录奖励"`、`"给视频 BVxxx 打赏"` |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "list": [
            {
                "time": "2026-07-11 05:49:19",
                "delta": 1,
                "reason": "登录奖励"
            },
            {
                "time": "2026-07-10 20:19:50",
                "delta": -2,
                "reason": "给视频 BV1wBMe69EhH 打赏"
            },
            {
                "time": "2026-07-10 04:22:06",
                "delta": 1,
                "reason": "登录奖励"
            }
        ],
        "count": 9
    }
}
```

---

## 常见变动原因（`reason`）

| 原因                | 方向 | 说明                        |
| ------------------- | ---- | --------------------------- |
| `登录奖励`          | 收入 | 每日登录PC/APP获得 1 枚硬币 |
| `给视频 BVxxx 打赏` | 支出 | 给视频投币                  |
| `给专栏打赏`        | 支出 | 给专栏投币                  |
| `老粉计划扣除`      | 支出 | 参与老粉计划被扣除的硬币    |
| `活动奖励`          | 收入 | 参与活动获得                |
| `任务奖励`          | 收入 | 完成任务获得                |

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
curl 'https://api.bilibili.com/x/member/web/coin/log?jsonp=jsonp&web_location=333.33&x-bili-redirect=1' \
  -H 'Origin: https://account.bilibili.com' \
  -H 'Referer: https://account.bilibili.com/' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **数据范围限制**：根据实际使用观察，该接口**仅返回最近约一周的硬币记录**，无法查询更早的历史数据（可能为服务端限制）。
2. **分页**：从抓包数据来看，该接口目前似乎**不支持分页参数**，仅返回最近的若干条记录。如需分页，可能需要额外参数或另有接口。
3. **`jsonp` 参数**：疑似历史遗留参数，不影响 JSON 响应格式。
4. **`delta` 方向**：
   - 正数（如 `1`）：收入（登录奖励、活动奖励等）
   - 负数（如 `-2`）：支出（投币、扣除等）
5. **认证**：必须携带有效的 `SESSDATA` Cookie，否则返回 `-101`。
6. **记录数量**：`count` 字段与 `list` 数组长度一致，表示本次返回的记录条数，不一定代表总记录数。


# 3. 今日投币经验查询

## 接口描述

查询当前登录用户今日通过投币已获得的经验值。每日投币可获得经验值，上限为 **50 点**。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于判断今日投币任务是否已完成。

---

## 接口地址

```
GET https://api.bilibili.com/x/web-interface/coin/today/exp
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数

无请求参数。仅需携带有效的 Cookie（`SESSDATA`）。

**示例请求 URL：**

```
https://api.bilibili.com/x/web-interface/coin/today/exp
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容                 | 备注       |
| ------- | ---- | -------------------- | ---------- |
| code    | num  | 状态码               | 0 表示成功 |
| message | str  | 状态信息             | `"OK"`     |
| ttl     | num  | 1                    |            |
| data    | num  | 今日投币已获得经验值 | 范围：0-50 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 0
}
```

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": 50
}
```

---

## 字段说明

| data 值 | 含义                 |
| ------- | -------------------- |
| 0       | 今日还未投币获得经验 |
| 1-49    | 今日已获得部分经验   |
| 50      | 今日投币经验已拿满   |

> **说明**：每日投币经验上限为 **50 点**，达到 50 后继续投币不再获得经验值。

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
curl 'https://api.bilibili.com/x/web-interface/coin/today/exp' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限当前用户**：该接口只能查询当前登录用户自己的投币经验。
3. **每日上限固定 50 点**：达到上限后，`data` 字段值为 `50`，继续投币不再增加经验。
4. **缓存**：数据可能存在缓存，不是实时更新的，但误差很小。


# 4. 用户投币视频列表

## 接口描述

获取指定用户投过币的视频列表（投币历史记录）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间“我的投币”页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/coin/video
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注           |
| ------------ | ---- | -------- | -------- | -------------- |
| vmid         | num  | 用户 UID | **必要** | 目标用户的 UID |
| pn           | num  | 页码     | 非必要   | 默认 1         |
| ps           | num  | 每页数量 | 非必要   | 默认 ？        |
| web_location | str  | 来源标识 | 非必要   | `333.1387`     |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/coin/video?vmid=3690995472402999&web_location=333.1387
```

---

## 响应结构

### 根对象

| 字段    | 类型  | 内容         | 备注       |
| ------- | ----- | ------------ | ---------- |
| code    | num   | 状态码       | 0 表示成功 |
| message | str   | 状态信息     | `"OK"`     |
| ttl     | num   | 1            |            |
| data    | array | 投币视频列表 |            |

### `data` 数组元素（关键字段）

| 字段    | 类型 | 内容       | 备注                           |
| ------- | ---- | ---------- | ------------------------------ |
| aid     | num  | 视频 AV ID |                                |
| bvid    | str  | 视频 BV ID |                                |
| title   | str  | 视频标题   |                                |
| pic     | str  | 封面图地址 |                                |
| pubdate | num  | 发布时间戳 |                                |
| owner   | obj  | UP 主信息  | 包含 `mid`、`name`、`face`     |
| stat    | obj  | 统计数据   |                                |
| coins   | num  | 投币数量   | **该用户给这个视频投了多少币** |
| time    | num  | 投币时间戳 |                                |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": [
        {
            "aid": 113433592792165,
            "bvid": "BV1XkDgYQEUG",
            "title": "【Hi-Res】《远走高飞》金志文",
            "pic": "http://i1.hdslb.com/bfs/archive/xxx.jpg",
            "owner": {
                "mid": 3546683705133415,
                "name": "大猫一日同风起"
            },
            "stat": {
                "view": 38059,
                "like": 222
            },
            "coins": 1,
            "time": 1782472975
        }
    ]
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
curl 'https://api.bilibili.com/x/space/coin/video?vmid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **查询他人投币列表**：`vmid` 可指定任意用户 UID，但若对方隐私设置，可能返回空列表。
3. **投币数量**：`coins` 字段表示该用户给这个视频投了多少枚硬币（通常为 1 或 2）。
4. **分页支持**：该接口支持 `pn` 和 `ps` 分页参数。


## 相关接口汇总

| 功能             | 接口路径                          | 请求方式 | 说明                       |
| ---------------- | --------------------------------- | -------- | -------------------------- |
| 硬币余额查询     | `/site/getCoin`                   | GET      | 查询当前用户持有的硬币总数 |
| 硬币收支记录     | `/x/member/web/coin/log`          | GET      | 硬币收支明细日志           |
| 今日投币经验     | `/x/web-interface/coin/today/exp` | GET      | 查询今日投币已获得经验值   |
| 投币操作         | `/x/web-interface/coin/add`       | POST     | 给视频/专栏投币            |
| 用户投币视频列表 | `/x/space/coin/video`             | GET      | 获取用户投过币的视频列表   |
