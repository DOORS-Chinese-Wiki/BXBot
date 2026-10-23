# 充电状态查询

## 接口描述

查询当前用户对指定 UP 主的充电状态，包含已充电天数、剩余天数、充电排行榜等信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示用户对 UP 主的充电详情。

---

## 接口地址

```
GET https://api.bilibili.com/x/upower/charge/follow/info
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容       | 必要性   | 备注                           |
| ------------ | ---- | ---------- | -------- | ------------------------------ |
| up_mid       | num  | UP 主 UID  | **必要** | 要查询的 UP 主 ID              |
| csrf         | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |
| t            | num  | 时间戳     | 非必要   | 毫秒级时间戳                   |
| web_location | str  | 来源标识   | 非必要   | 固定传 `333.1196` 或类似值     |

**示例请求 URL：**

```
https://api.bilibili.com/x/upower/charge/follow/info?csrf=xxx&t=1783816787394&up_mid=1447574&web_location=333.1196
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

| 字段               | 类型 | 内容           | 备注         |
| ------------------ | ---- | -------------- | ------------ |
| days               | num  | 已充电天数     |              |
| remain_days        | num  | 剩余天数       |              |
| remain_less_1day   | num  | 是否不足 1 天  | 0：否，1：是 |
| up_card            | obj  | UP 主卡片信息  |              |
| user_card          | obj  | 用户卡片信息   |              |
| upower_rank        | obj  | 充电排行榜     |              |
| upower_icon        | str  | 充电图标       |              |
| upower_right_count | num  | 专属权益数量   |              |
| only_contain_medal | bool | 是否仅包含勋章 |              |
| privilege_type     | num  | 当前充电档位   |              |
| challenge_info     | obj  | 挑战任务信息   |              |

### `up_card` 对象

| 字段           | 类型 | 内容          | 备注 |
| -------------- | ---- | ------------- | ---- |
| mid            | num  | UP 主 UID     |      |
| nickname       | str  | UP 主昵称     |      |
| official_title | str  | 官方认证标题  |      |
| avatar         | str  | UP 主头像地址 |      |

### `user_card` 对象

| 字段     | 类型 | 内容         | 备注 |
| -------- | ---- | ------------ | ---- |
| avatar   | str  | 用户头像地址 |      |
| nickname | str  | 用户昵称     |      |

### `upower_rank` 对象

| 字段       | 类型  | 内容         | 备注         |
| ---------- | ----- | ------------ | ------------ |
| total      | num   | 充电总人数   |              |
| total_desc | str   | 充电人数描述 | 如 `"2000+"` |
| list       | array | 排行榜列表   | 前 6 名      |

### `upower_rank.list` 数组元素

| 字段     | 类型 | 内容         | 备注 |
| -------- | ---- | ------------ | ---- |
| rank     | num  | 排名         |      |
| mid      | num  | 用户 UID     |      |
| nickname | str  | 用户昵称     |      |
| avatar   | str  | 用户头像地址 |      |

### `challenge_info` 对象

| 字段           | 类型  | 内容         | 备注 |
| -------------- | ----- | ------------ | ---- |
| challenge_id   | str   | 挑战 ID      |      |
| description    | str   | 挑战描述     |      |
| challenge_type | num   | 挑战类型     |      |
| remaining_days | num   | 剩余天数     |      |
| end_time       | str   | 结束时间     |      |
| progress       | num   | 进度         |      |
| targets        | array | 目标列表     |      |
| state          | num   | 状态         |      |
| end_time_unix  | num   | 结束时间戳   |      |
| pub_dyn        | num   | 是否发布动态 |      |
| dyn_content    | str   | 动态内容     |      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "days": 190,
        "remain_days": 270,
        "remain_less_1day": 0,
        "up_card": {
            "mid": 1447574,
            "nickname": "洛少爷",
            "official_title": "bilibili 知名音乐UP主",
            "avatar": "https://i2.hdslb.com/bfs/face/xxx.jpg"
        },
        "user_card": {
            "avatar": "https://i0.hdslb.com/bfs/face/xxx.jpg",
            "nickname": "YunLv_L"
        },
        "upower_rank": {
            "total": 2289,
            "total_desc": "2000+",
            "list": [
                {
                    "rank": 1,
                    "mid": 1027691452,
                    "nickname": "Carlorrr",
                    "avatar": "https://i1.hdslb.com/bfs/face/xxx.jpg"
                }
            ]
        },
        "upower_icon": "",
        "upower_right_count": 3,
        "only_contain_medal": false,
        "privilege_type": 10,
        "challenge_info": {
            "challenge_id": "",
            "description": "",
            "challenge_type": 0,
            "remaining_days": 0,
            "end_time": "",
            "progress": 0,
            "targets": [],
            "state": 0,
            "end_time_unix": 0,
            "pub_dyn": 0,
            "dyn_content": ""
        }
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -403   | CSRF 验证失败               |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/upower/charge/follow/info?csrf=xxx&t=1783816787394&up_mid=1447574&web_location=333.1196' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和 URL 参数中的 `csrf`，两者值一致。
3. **`days` 与 `remain_days`**：两者之和为充电总周期天数。
4. **`privilege_type`**：表示当前用户的充电档位（如 10 表示 10 元档）。
5. **`upower_rank.list`**：仅返回前 6 名充电用户，用于前端展示排行榜预览。
6. **`challenge_info`**：可能用于充电挑战任务，目前大多数 UP 主未启用，字段为空。


### 📂 充电模块文件清单

| 文件                                 | 内容                                            |
| ------------------------------------ | ----------------------------------------------- |
| `bili-electric-up-api.md`            | 充电专属权益页面（UP 主所有档位的专属内容聚合） |
| `bili-electric-charge-status-api.md` | 充电状态查询（用户对 UP 主的充电详情）          |
