# 获取用户追番列表

## 接口描述

获取指定用户的追番列表（包含番剧、影视等），支持分页。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间展示追番列表。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/space/bangumi/follow/list
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容       | 必要性   | 备注                       |
| ------------ | ---- | ---------- | -------- | -------------------------- |
| vmid         | num  | 用户 UID   | **必要** | 目标用户的 UID             |
| type         | num  | 类型       | **必要** | `1`：番剧，`2`：影视？     |
| pn           | num  | 页码       | 非必要   | 默认 1                     |
| ps           | num  | 每页数量   | 非必要   | 默认 15                    |
| web_location | str  | 来源标识   | 非必要   | 固定传 `333.1387` 或类似值 |
| w_rid        | str  | WBI 签名   | **必要** | 见 WBI 签名算法            |
| wts          | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳           |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/bangumi/follow/list?vmid=3690995472402999&type=1&pn=1&ps=15&web_location=333.1387&w_rid=xxx&wts=xxx
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

| 字段  | 类型  | 内容     | 备注               |
| ----- | ----- | -------- | ------------------ |
| list  | array | 追番列表 | 每个元素为一部番剧 |
| pn    | num   | 当前页码 |                    |
| ps    | num   | 每页数量 |                    |
| total | num   | 追番总数 |                    |

### `list` 数组元素

| 字段             | 类型  | 内容         | 备注                                    |
| ---------------- | ----- | ------------ | --------------------------------------- |
| season_id        | num   | 剧集 ID      |                                         |
| media_id         | num   | 媒体 ID      |                                         |
| season_type      | num   | 类型         | `1`：番剧                               |
| season_type_name | str   | 类型名称     | `"番剧"`                                |
| title            | str   | 番剧名称     |                                         |
| cover            | str   | 封面图地址   |                                         |
| total_count      | num   | 总集数       |                                         |
| is_finish        | num   | 是否完结     | 1：已完结                               |
| is_started       | num   | 是否开播     | 1：已开播                               |
| is_play          | num   | 是否可播放   | 1：可播放                               |
| badge            | str   | 角标文案     | 如 `"大会员"`                           |
| badge_type       | num   | 角标类型     |                                         |
| stat             | obj   | 统计数据     |                                         |
| rating           | obj   | 评分信息     |                                         |
| new_ep           | obj   | 最新剧集信息 |                                         |
| follow_status    | num   | 追番状态     | 1：已追？2：追番中，3：已看完           |
| progress         | str   | 观看进度     | 如 `"看到第6话 0:42"`、`"已看完第12话"` |
| both_follow      | bool  | 是否同时关注 |                                         |
| url              | str   | 播放链接     |                                         |
| series           | obj   | 系列信息     |                                         |
| styles           | array | 标签列表     | 如 `["少女","奇幻","搞笑"]`             |
| evaluate         | str   | 简介         |                                         |

### `stat` 对象

| 字段     | 类型 | 内容     | 备注 |
| -------- | ---- | -------- | ---- |
| follow   | num  | 追番人数 |      |
| view     | num  | 播放量   |      |
| danmaku  | num  | 弹幕数   |      |
| reply    | num  | 评论数   |      |
| coin     | num  | 投币数   |      |
| likes    | num  | 点赞数   |      |
| favorite | num  | 收藏数   |      |

### `rating` 对象

| 字段  | 类型 | 内容     | 备注   |
| ----- | ---- | -------- | ------ |
| score | num  | 评分     | 如 9.8 |
| count | num  | 评分人数 |        |

### `new_ep` 对象

| 字段       | 类型 | 内容         | 备注          |
| ---------- | ---- | ------------ | ------------- |
| id         | num  | 剧集 ID      |               |
| index_show | str  | 集数显示     | 如 `"全24话"` |
| cover      | str  | 封面图地址   |               |
| title      | str  | 集数标题     |               |
| long_title | str  | 完整标题     |               |
| pub_time   | str  | 更新时间     |               |
| duration   | num  | 时长（毫秒） |               |

### `series` 对象

| 字段          | 类型 | 内容         | 备注 |
| ------------- | ---- | ------------ | ---- |
| series_id     | num  | 系列 ID      |      |
| title         | str  | 系列名称     |      |
| season_count  | num  | 系列包含季数 |      |
| new_season_id | num  | 最新季 ID    |      |
| series_ord    | num  | 当前季序号   |      |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "list": [
            {
                "season_id": 76110,
                "title": "地缚少年花子君 第二季",
                "cover": "https://i0.hdslb.com/bfs/bangumi/image/xxx.png",
                "stat": {
                    "follow": 4525271,
                    "view": 53983679
                },
                "rating": {
                    "score": 9.8,
                    "count": 3177
                },
                "follow_status": 2,
                "progress": "看到第6话 0:42",
                "both_follow": true
            }
        ],
        "pn": 1,
        "ps": 15,
        "total": 2
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
curl 'https://api.bilibili.com/x/space/bangumi/follow/list?vmid=3690995472402999&type=1&pn=1&ps=15&web_location=333.1387&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`type` 参数**：`1` 表示番剧，可能 `2` 表示影视（待验证）。
3. **`follow_status`**：
   - `1`：已追番（未观看？）
   - `2`：追番中（观看中）
   - `3`：已看完
4. **`progress` 字段**：显示用户观看进度，未观看时为空或 `null`。
5. **`both_follow`**：`true` 表示同时关注了该番剧的 UP 主（如官方账号）。

---

## 相关接口

| 功能     | 接口路径                       | 签名 |
| -------- | ------------------------------ | ---- |
| 追番列表 | `/x/space/bangumi/follow/list` | WBI  |

> **说明**：追番总数、追番中、已看完等统计数据，可通过 `/x/space/bangumi/follow/list` 接口返回的 `list` 数组和 `total` 字段自行计算得出。目前未发现独立的追番统计接口。
