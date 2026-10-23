# 充电专属权益页面（权益引导页）

## 接口描述

获取 UP 主所有充电档位的专属权益内容聚合页，包含专属视频、直播回放、专属问答、专属动态、专属抽奖、专属表情包、粉丝勋章等。该接口同时返回当前用户对各权益的解锁状态（`locked` 字段）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示充电专属权益页面（权益引导页）。

---

## 接口地址

```
GET https://api.bilibili.com/x/upowerv2/gw/rights/guide
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
| build        | num  | 构建版本   | 非必要   | 固定传 `0`                     |
| device       | str  | 设备标识   | 非必要   | 通常为空                       |

**示例请求 URL：**

```
https://api.bilibili.com/x/upowerv2/gw/rights/guide?build=0&csrf=xxx&device=&t=1783816787431&up_mid=1447574&web_location=333.1196
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

| 字段           | 类型  | 内容             | 备注                 |
| -------------- | ----- | ---------------- | -------------------- |
| up             | obj   | UP 主信息        |                      |
| privilege_type | num   | 当前用户充电档位 | 如 10、20            |
| rights         | array | 各档位权益列表   | 按 `level_type` 分组 |

### `up` 对象

| 字段             | 类型  | 内容             | 备注                           |
| ---------------- | ----- | ---------------- | ------------------------------ |
| up_mid           | num   | UP 主 UID        |                                |
| name             | str   | UP 主昵称        |                                |
| face             | str   | UP 主头像地址    |                                |
| tabs             | array | 充电档位介绍     | 每个档位的名称、介绍、是否锁定 |
| rank             | obj   | 充电排行信息     |                                |
| upower_num_show  | num   | 是否显示充电人数 | 1：显示                        |
| upower_rank_show | num   | 是否显示充电排行 | 1：显示                        |

### `up.tabs` 数组元素

| 字段           | 类型 | 内容     | 备注                            |
| -------------- | ---- | -------- | ------------------------------- |
| privilege_name | str  | 权益名称 |                                 |
| privilege_type | num  | 权益类型 | 10/20 等，对应充电档位          |
| locked         | bool | 是否锁定 | `true`：未解锁，`false`：已解锁 |
| level_type     | num  | 档位类型 | 与 `privilege_type` 相同        |
| level_name     | str  | 档位名称 |                                 |
| level_intro    | str  | 档位介绍 |                                 |

### `up.rank` 对象

| 字段          | 类型  | 内容             | 备注    |
| ------------- | ----- | ---------------- | ------- |
| upower_num    | num   | 充电总人数       |         |
| preview_faces | array | 充电用户头像预览 | 前 3 名 |

### `rights` 数组元素

| 字段       | 类型  | 内容               | 备注      |
| ---------- | ----- | ------------------ | --------- |
| level_type | num   | 档位类型           | 如 10、20 |
| right_list | array | 该档位下的权益列表 |           |

### `right_list` 数组元素

| 字段       | 类型  | 内容         | 备注                                                         |
| ---------- | ----- | ------------ | ------------------------------------------------------------ |
| right_type | str   | 权益类型     | `archive`：视频，`live`：直播，`qa`：问答，`dynamic`：动态，`lottery`：抽奖，`emote`：表情包，`medal`：勋章 |
| num        | num   | 数量         |                                                              |
| num_str    | str   | 数量字符串   | 如 `"5"`、`"99+"`                                            |
| sort       | num   | 排序         |                                                              |
| locked     | bool  | 是否锁定     | `true`：未解锁（需要更高档位），`false`：已解锁              |
| list       | array | 具体内容列表 |                                                              |

### `right_list.list` 数组元素（按类型区分）

#### 1. 专属视频（`right_type: archive`）

| 字段          | 类型 | 内容           | 备注              |
| ------------- | ---- | -------------- | ----------------- |
| titles        | str  | 视频标题       |                   |
| pub_date      | num  | 发布时间戳     | Unix 时间戳（秒） |
| aid           | num  | 视频 AV ID     |                   |
| view          | num  | 播放量         |                   |
| danmaku       | num  | 弹幕数         |                   |
| pic           | str  | 封面图地址     |                   |
| duration      | num  | 视频时长（秒） |                   |
| short_link_v2 | str  | 短链接         |                   |
| badge_text    | str  | 角标文案       | 如 `"充电专属"`   |
| badge_icon    | str  | 角标图标       |                   |

#### 2. 直播回放（`right_type: live`）

| 字段          | 类型 | 内容     | 备注      |
| ------------- | ---- | -------- | --------- |
| on_live_state | num  | 直播状态 | 0：未直播 |
| live_infos    | obj  | 直播信息 |           |

##### `live_infos` 对象

| 字段           | 类型 | 内容       | 备注            |
| -------------- | ---- | ---------- | --------------- |
| cover          | str  | 封面图地址 |                 |
| title          | str  | 直播标题   |                 |
| audience_count | num  | 观看人数   |                 |
| start_time     | num  | 开始时间戳 |                 |
| end_time       | num  | 结束时间戳 |                 |
| room_id        | num  | 直播间 ID  |                 |
| subarea        | str  | 分区名称   | 如 `"单机游戏"` |
| live_date      | str  | 直播日期   | 如 `"1月18日"`  |

#### 3. 专属问答（`right_type: qa`）

| 字段          | 类型 | 内容         | 备注 |
| ------------- | ---- | ------------ | ---- |
| qa_id         | num  | 问答 ID      |      |
| user          | obj  | 提问用户信息 |      |
| question_time | num  | 提问时间戳   |      |
| question_text | str  | 问题内容     |      |
| qa_remain     | num  | 剩余问答数   |      |

#### 4. 专属动态（`right_type: dynamic`）

| 字段         | 类型  | 内容            | 备注        |
| ------------ | ----- | --------------- | ----------- |
| type         | num   | 动态类型        | 2：图文动态 |
| rid          | num   | 动态 ID         |             |
| ctime        | num   | 发布时间戳      |             |
| cover        | str   | 封面图地址      |             |
| title        | str   | 标题            |             |
| content      | str   | 内容            |             |
| pictures     | array | 图片列表        |             |
| jump_url     | str   | 跳转链接（APP） |             |
| jump_url_web | str   | 跳转链接（Web） |             |

#### 5. 专属抽奖（`right_type: lottery`）

| 字段         | 类型 | 内容            | 备注                          |
| ------------ | ---- | --------------- | ----------------------------- |
| ctime        | num  | 发布时间戳      |                               |
| content      | str  | 抽奖内容        | 如 `"一等奖*1份、二等奖*3份"` |
| jump_url     | str  | 跳转链接（APP） |                               |
| jump_url_web | str  | 跳转链接（Web） |                               |
| lottery_id   | num  | 抽奖 ID         |                               |

#### 6. 专属表情包（`right_type: emote`）

| 字段 | 类型 | 内容         | 备注          |
| ---- | ---- | ------------ | ------------- |
| id   | num  | 表情 ID      |               |
| name | str  | 表情名称     | 如 `"棒的嘞"` |
| icon | str  | 表情图标地址 |               |

#### 7. 粉丝勋章（`right_type: medal`）

| 字段      | 类型 | 内容     | 备注        |
| --------- | ---- | -------- | ----------- |
| level     | num  | 勋章等级 |             |
| fans_name | str  | 勋章名称 | 如 `"洛府"` |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "up": {
            "up_mid": 1447574,
            "name": "洛少爷",
            "face": "https://i2.hdslb.com/bfs/face/xxx.jpg",
            "tabs": [
                {
                    "privilege_name": "据说是专属视频",
                    "privilege_type": 20,
                    "locked": true,
                    "level_type": 20,
                    "level_name": "据说是专属视频",
                    "level_intro": "包含专属视频！不定期抽奖小福利！"
                },
                {
                    "privilege_name": "据说是粉丝勋章",
                    "privilege_type": 10,
                    "locked": false,
                    "level_type": 10,
                    "level_name": "据说是粉丝勋章",
                    "level_intro": "包含洛府粉丝勋章，充电表情包"
                }
            ],
            "rank": {
                "upower_num": 2289,
                "preview_faces": ["https://i1.hdslb.com/bfs/face/xxx.jpg"]
            },
            "upower_num_show": 1,
            "upower_rank_show": 1
        },
        "privilege_type": 10,
        "rights": [
            {
                "level_type": 20,
                "right_list": [
                    {
                        "right_type": "archive",
                        "num": 5,
                        "num_str": "5",
                        "sort": 2,
                        "locked": true,
                        "list": [
                            {
                                "titles": "【角色扮演小剧场】《星域条例》",
                                "aid": 114863397475253,
                                "view": 2453,
                                "pic": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
                                "duration": 134,
                                "badge_text": "充电专属"
                            }
                        ]
                    }
                ]
            },
            {
                "level_type": 10,
                "right_list": [
                    {
                        "right_type": "emote",
                        "num": 19,
                        "num_str": "19",
                        "sort": 9,
                        "locked": false,
                        "list": [
                            {
                                "id": 28652,
                                "name": "棒的嘞",
                                "icon": "https://i0.hdslb.com/bfs/garb/xxx.png"
                            }
                        ]
                    }
                ]
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
| -403   | CSRF 验证失败               |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/upowerv2/gw/rights/guide?build=0&csrf=xxx&device=&t=1783816787431&up_mid=1447574&web_location=333.1196' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和 URL 参数中的 `csrf`，两者值一致。
3. **`locked` 字段**：表示当前用户是否已解锁该权益。
   - `true`：未解锁（需要更高充电档位）
   - `false`：已解锁（当前充电档位足够）
4. **`rights` 按档位分组**：
   - `level_type: 20`：20 元档位权益
   - `level_type: 10`：10 元档位权益
5. **`privilege_type`**：当前用户的充电档位，决定哪些权益已解锁。
6. **`up.tabs` 与 `rights` 的对应关系**：`tabs` 是档位介绍文案，`rights` 是该档位下的实际内容列表。
7. **权益类型说明**：
   - `archive`：充电专属视频
   - `live`：直播回放
   - `qa`：专属问答
   - `dynamic`：专属动态
   - `lottery`：专属抽奖
   - `emote`：专属表情包
   - `medal`：粉丝勋章


### 📂 充电模块文件清单

| 文件                                 | 内容                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| `bili-electric-rights-guide-api.md`  | 充电专属权益页面（UP 主所有档位的权益聚合）                  |
| `bili-electric-charge-status-api.md` | 充电状态查询（用户对 UP 主的充电详情）                       |
| 原项目已有                           | `Bcoin.md`、`WeChat&Alipay.md`、`charge_msg.md`、`charge_list.md` |


### 📌 与 `bili-electric-charge-status-api.md` 的区别

| 维度     | `rights-guide`                       | `charge-status`            |
| -------- | ------------------------------------ | -------------------------- |
| 用途     | UP 主所有档位的专属权益展示          | 当前用户的充电状态查询     |
| 返回内容 | 专属视频、直播、问答、动态、表情包等 | 充电天数、剩余天数、排行榜 |
| 关注焦点 | UP 主视角                            | 用户视角                   |
