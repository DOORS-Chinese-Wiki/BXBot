# 粉丝勋章 API

## 接口列表

### 1. 粉丝勋章墙查询
### 2. 佩戴粉丝勋章
### 3. 取消佩戴粉丝勋章

---

# 1. 粉丝勋章墙查询

## 接口描述

获取指定用户的粉丝勋章墙列表，包含勋章详情、佩戴状态、亲密度等信息。

> 该接口位于直播域名 `api.live.bilibili.com`，用于个人空间展示粉丝勋章或查询他人勋章墙。

---

## 接口地址

```
GET https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`，但查询他人勋章墙时可能无需登录）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名    | 类型 | 内容         | 必要性 | 备注               |
| --------- | ---- | ------------ | ------ | ------------------ |
| target_id | num  | 目标用户 UID | 必要   | 要查询的用户的 UID |

**示例请求 URL：**

```
https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id=123456789
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

| 字段              | 类型  | 内容                   | 备注                   |
| ----------------- | ----- | ---------------------- | ---------------------- |
| list              | array | 勋章列表               | 每个元素为一个勋章对象 |
| count             | num   | 勋章总数               |                        |
| close_space_medal | num   | 是否关闭空间勋章展示   | 0：未关闭，1：关闭     |
| only_show_wearing | num   | 是否仅显示佩戴中的勋章 | 0：否，1：是           |
| name              | str   | 用户昵称               | 目标用户的昵称         |
| icon              | str   | 用户头像地址           |                        |
| uid               | num   | 用户 UID               |                        |
| level             | num   | 用户等级（直播等级）   |                        |

### `list` 数组元素

| 字段        | 类型 | 内容                 | 备注                                    |
| ----------- | ---- | -------------------- | --------------------------------------- |
| medal_info  | obj  | 勋章详细信息         |                                         |
| target_name | str  | 目标用户（UP主）昵称 | 即勋章所属的 UP 主                      |
| target_icon | str  | 目标用户头像地址     |                                         |
| link        | str  | 目标用户空间链接     | 如 `https://space.bilibili.com/1447574` |
| live_status | num  | 目标用户直播状态     | 0：未直播，1：直播中，2：轮播中？       |
| official    | num  | 是否认证             | 1：个人认证，2：机构认证等              |
| uinfo_medal | obj  | 用户侧勋章展示信息   | 用于前端渲染的额外字段                  |

### `medal_info` 对象

| 字段               | 类型 | 内容                   | 备注                             |
| ------------------ | ---- | ---------------------- | -------------------------------- |
| target_id          | num  | 勋章所属 UP 主的 UID   |                                  |
| level              | num  | 勋章等级               | 1-？                             |
| medal_name         | str  | 勋章名称               | 如 "洛府"                        |
| medal_color_start  | num  | 勋章起始颜色（十进制） | RGB 十进制数值                   |
| medal_color_end    | num  | 勋章结束颜色（十进制） |                                  |
| medal_color_border | num  | 勋章边框颜色（十进制） |                                  |
| guard_level        | num  | 大航海（舰长）等级     | 0：无，1：总督，2：提督，3：舰长 |
| wearing_status     | num  | 当前是否佩戴中         | 1：佩戴中，0：未佩戴             |
| medal_id           | num  | 勋章唯一 ID            |                                  |
| intimacy           | num  | 当前亲密度             |                                  |
| next_intimacy      | num  | 下一级所需亲密度       |                                  |
| today_feed         | num  | 今日已获得亲密度       |                                  |
| day_limit          | num  | 每日亲密度上限         | 通常为 20000                     |
| guard_icon         | str  | 大航海图标地址         | 通常为空                         |
| honor_icon         | str  | 荣誉图标地址           | 通常为空                         |

### `uinfo_medal` 对象

| 字段                  | 类型 | 内容                     | 备注                 |
| --------------------- | ---- | ------------------------ | -------------------- |
| name                  | str  | 勋章名称                 | 与 `medal_name` 相同 |
| level                 | num  | 勋章等级                 |                      |
| color_start           | num  | 起始颜色（十进制）       |                      |
| color_end             | num  | 结束颜色（十进制）       |                      |
| color_border          | num  | 边框颜色（十进制）       |                      |
| color                 | num  | 颜色（旧字段）           | 通常为 0             |
| id                    | num  | 勋章 ID                  | 与 `medal_id` 相同   |
| typ                   | num  | 类型                     | 通常为 0             |
| is_light              | num  | 是否点亮                 | 1：点亮              |
| ruid                  | num  | 目标用户 UID             | 与 `target_id` 相同  |
| guard_level           | num  | 大航海等级               |                      |
| score                 | num  | 分数                     | 通常为 0             |
| guard_icon            | str  | 大航海图标               |                      |
| honor_icon            | str  | 荣誉图标                 |                      |
| v2_medal_color_start  | str  | V2 起始颜色（RGBA 格式） | 如 `"#C770A499"`     |
| v2_medal_color_end    | str  | V2 结束颜色（RGBA 格式） |                      |
| v2_medal_color_border | str  | V2 边框颜色（RGBA 格式） |                      |
| v2_medal_color_text   | str  | V2 文字颜色（RGBA 格式） | 通常为 `"#FFFFFF"`   |
| v2_medal_color_level  | str  | V2 等级颜色（RGBA 格式） |                      |
| user_receive_count    | num  | 用户领取该勋章的次数？   | 通常为 0             |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "list": [
            {
                "medal_info": {
                    "target_id": 1447574,
                    "level": 16,
                    "medal_name": "示例勋章",
                    "medal_color_start": 12478086,
                    "medal_color_end": 12478086,
                    "medal_color_border": 12478086,
                    "guard_level": 0,
                    "wearing_status": 1,
                    "medal_id": 6375,
                    "intimacy": 93,
                    "next_intimacy": 139,
                    "today_feed": 0,
                    "day_limit": 20000,
                    "guard_icon": "",
                    "honor_icon": ""
                },
                "target_name": "UP主昵称",
                "target_icon": "https://i2.hdslb.com/bfs/face/xxx.jpg",
                "link": "https://space.bilibili.com/1447574",
                "live_status": 2,
                "official": 1,
                "uinfo_medal": {
                    "name": "示例勋章",
                    "level": 16,
                    "color_start": 12478086,
                    "color_end": 12478086,
                    "color_border": 12478086,
                    "color": 0,
                    "id": 6375,
                    "typ": 0,
                    "is_light": 1,
                    "ruid": 1447574,
                    "guard_level": 0,
                    "score": 0,
                    "guard_icon": "",
                    "honor_icon": "",
                    "v2_medal_color_start": "#C770A499",
                    "v2_medal_color_end": "#C770A499",
                    "v2_medal_color_border": "#C770A499",
                    "v2_medal_color_text": "#FFFFFF",
                    "v2_medal_color_level": "#C770A4E6",
                    "user_receive_count": 0
                }
            }
        ],
        "count": 1,
        "close_space_medal": 0,
        "only_show_wearing": 0,
        "name": "用户昵称",
        "icon": "https://i0.hdslb.com/bfs/face/xxx.jpg",
        "uid": 123456789,
        "level": 3
    }
}
```

---

## 错误码

| 状态码 | 含义                |
| ------ | ------------------- |
| 0      | 请求成功            |
| 其他   | 参见 `message` 字段 |

---

## 调用示例（curl）

```bash
curl 'https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id=123456789' \
  -H 'Referer: https://live.bilibili.com/' \
  -H 'Origin: https://live.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **`target_id` 为必填参数**，表示要查询的用户 UID。
2. **该接口似乎无需登录**即可查询他人勋章墙，但若查询自己的勋章墙，携带 `SESSDATA` 可能获得更完整的数据（如未公开的勋章？）。
3. **`wearing_status` 标识当前用户是否佩戴该勋章**（前提是查询自己数据时有效，查询他人时只表示对方是否佩戴）。
4. **颜色字段**：十进制颜色值（如 `12478086`）转换为十六进制为 `#BE6A86`，V2 字段直接提供了 RGBA 格式字符串，便于前端展示。
5. **亲密度相关**：`intimacy` 为当前亲密度，`next_intimacy` 为下一级所需亲密度，`today_feed` 为今日已增加量，`day_limit` 为每日上限。
6. **`guard_level`**：0 表示非大航海用户，1/2/3 分别对应总督/提督/舰长（具体需验证）。
7. **`live_status`**：0 表示未开播，1 表示正在直播，2 表示轮播或结束？实际以文档更新为准。


# 2. 佩戴粉丝勋章

## 接口描述

为当前登录用户佩戴指定的粉丝勋章。

> 该接口位于直播域名 `api.live.bilibili.com`，用于控制勋章墙的佩戴状态。

---

## 接口地址

```
POST https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/wear
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名     | 类型 | 内容       | 必要性 | 备注                               |
| ---------- | ---- | ---------- | ------ | ---------------------------------- |
| medal_id   | num  | 勋章 ID    | 必要   | 从勋章墙接口获取的 `medal_id`      |
| target_id  | num  | 目标 UID   | 必要   | 固定传 `0`，表示对当前登录用户操作 |
| csrf_token | str  | CSRF Token | 必要   | 位于 Cookie 中的 `bili_jct` 值     |
| csrf       | str  | CSRF Token | 必要   | 同 `csrf_token`，重复传递          |
| visit_id   | str  | 访问标识   | 非必要 | 可能用于会话追踪，从页面获取       |

**示例请求体：**

```
medal_id=6375&target_id=0&csrf_token=1eaefa721216ddee6444fcbedace61b2&csrf=1eaefa721216ddee6444fcbedace61b2&visit_id=2t65pfx40kc0
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注        |
| ------- | ---- | -------- | ----------- |
| code    | num  | 状态码   | 0 表示成功  |
| message | str  | 状态信息 | `"OK"`      |
| ttl     | num  | 1        |             |
| data    | obj  | 数据本体 | 空对象 `{}` |

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
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段说明                  |

---

## 调用示例（curl）

```bash
curl 'https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/wear' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://live.bilibili.com/' \
  -H 'Origin: https://live.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'medal_id=6375' \
  --data-urlencode 'target_id=0' \
  --data-urlencode 'csrf_token=xxx' \
  --data-urlencode 'csrf=xxx' \
  --data-urlencode 'visit_id=xxx'
```

---

## 注意事项

1. **`medal_id` 来源**：从勋章墙接口 `MedalWall` 返回的 `medal_id` 字段获取，不是 `target_id`。
2. **`csrf` 双重传递**：接口同时接收 `csrf_token` 和 `csrf` 两个参数，值均为 Cookie 中的 `bili_jct`。
3. **`target_id=0`**：固定传 `0`，表示对当前登录用户进行佩戴/取消操作。
4. **`visit_id`**：为可选参数，可能来自页面浏览上下文，部分场景下不传也可能成功。
5. **操作互斥**：佩戴新勋章会自动取消当前佩戴的勋章，无需先调用取消接口。
6. **响应 `data` 为空**：操作成功时返回空对象，无额外数据。


# 3. 取消佩戴粉丝勋章

## 接口描述

取消当前登录用户佩戴的粉丝勋章。

> 该接口位于直播域名 `api.live.bilibili.com`，用于控制勋章墙的佩戴状态。

---

## 接口地址

```
POST https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/take_off
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`

---

## 请求参数（表单数据）

| 参数名     | 类型 | 内容       | 必要性 | 备注                               |
| ---------- | ---- | ---------- | ------ | ---------------------------------- |
| medal_id   | num  | 勋章 ID    | 必要   | 从勋章墙接口获取的 `medal_id`      |
| target_id  | num  | 目标 UID   | 必要   | 固定传 `0`，表示对当前登录用户操作 |
| csrf_token | str  | CSRF Token | 必要   | 位于 Cookie 中的 `bili_jct` 值     |
| csrf       | str  | CSRF Token | 必要   | 同 `csrf_token`，重复传递          |
| visit_id   | str  | 访问标识   | 非必要 | 可能用于会话追踪，从页面获取       |

**示例请求体：**

```
medal_id=6375&target_id=0&csrf_token=1eaefa721216ddee6444fcbedace61b2&csrf=1eaefa721216ddee6444fcbedace61b2&visit_id=2t65pfx40kc0
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注        |
| ------- | ---- | -------- | ----------- |
| code    | num  | 状态码   | 0 表示成功  |
| message | str  | 状态信息 | `"OK"`      |
| ttl     | num  | 1        |             |
| data    | obj  | 数据本体 | 空对象 `{}` |

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
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段说明                  |

---

## 调用示例（curl）

```bash
curl 'https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/take_off' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://live.bilibili.com/' \
  -H 'Origin: https://live.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'medal_id=6375' \
  --data-urlencode 'target_id=0' \
  --data-urlencode 'csrf_token=xxx' \
  --data-urlencode 'csrf=xxx' \
  --data-urlencode 'visit_id=xxx'
```

---

## 注意事项

1. **`medal_id` 来源**：从勋章墙接口 `MedalWall` 返回的 `medal_id` 字段获取。
2. **`csrf` 双重传递**：接口同时接收 `csrf_token` 和 `csrf` 两个参数，值均为 Cookie 中的 `bili_jct`。
3. **`target_id=0`**：固定传 `0`，表示对当前登录用户进行操作。
4. **无需事先查询佩戴状态**：直接调用取消即可，如果当前未佩戴该勋章，接口可能返回成功或特定错误码。


## 相关接口汇总

| 功能       | 接口路径                                   | 请求方式 | 关键参数           |
| ---------- | ------------------------------------------ | -------- | ------------------ |
| 勋章墙查询 | `/xlive/web-ucenter/user/MedalWall`        | GET      | `target_id`        |
| 佩戴勋章   | `/xlive/app-ucenter/v1/fansMedal/wear`     | POST     | `medal_id`、`csrf` |
| 取消佩戴   | `/xlive/app-ucenter/v1/fansMedal/take_off` | POST     | `medal_id`、`csrf` |
