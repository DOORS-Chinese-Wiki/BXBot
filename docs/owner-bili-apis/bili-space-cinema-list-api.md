# 获取用户追剧列表（电影/影视）

## 接口描述

获取指定用户的追剧列表（电影、影视内容），包含观看进度、追剧状态等信息。

> 该接口与追番列表共用接口路径，仅通过 `type` 参数区分内容类型。该接口需要 WBI 签名。

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

| 参数名        | 类型 | 内容       | 必要性   | 备注                                |
| ------------- | ---- | ---------- | -------- | ----------------------------------- |
| vmid          | num  | 用户 UID   | **必要** |                                     |
| type          | num  | 内容类型   | **必要** | `2`：电影/影视                      |
| pn            | num  | 页码       | 非必要   | 默认 1                              |
| ps            | num  | 每页数量   | 非必要   | 默认 15，最大 24？                  |
| platform      | str  | 平台标识   | 非必要   | `web`                               |
| follow_status | num  | 追剧状态   | 非必要   | `0`：全部，`1`：追剧中，`2`：已看完 |
| web_location  | str  | 来源标识   | 非必要   | `0.0`                               |
| w_rid         | str  | WBI 签名   | **必要** | 见 WBI 签名算法                     |
| wts           | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳                    |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/bangumi/follow/list?vmid=3690995472402999&type=2&pn=1&ps=24&platform=web&follow_status=0&web_location=0.0&w_rid=xxx&wts=xxx
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

| 字段  | 类型  | 内容     | 备注                    |
| ----- | ----- | -------- | ----------------------- |
| list  | array | 追剧列表 | 每个元素为一部电影/影视 |
| pn    | num   | 当前页码 |                         |
| ps    | num   | 每页数量 |                         |
| total | num   | 追剧总数 |                         |

### `list` 数组元素

| 字段             | 类型  | 内容         | 备注                          |
| ---------------- | ----- | ------------ | ----------------------------- |
| season_id        | num   | 剧集 ID      |                               |
| media_id         | num   | 媒体 ID      |                               |
| season_type      | num   | 类型         | `2`：电影                     |
| season_type_name | str   | 类型名称     | `"电影"`                      |
| title            | str   | 电影名称     |                               |
| cover            | str   | 封面图地址   |                               |
| total_count      | num   | 总集数       | 电影通常为 1                  |
| is_finish        | num   | 是否完结     | 1：已完结                     |
| is_started       | num   | 是否上映     | 1：已上映                     |
| is_play          | num   | 是否可播放   | 1：可播放                     |
| badge            | str   | 角标文案     | 如 `"大会员"`                 |
| badge_type       | num   | 角标类型     |                               |
| stat             | obj   | 统计数据     |                               |
| rating           | obj   | 评分信息     |                               |
| new_ep           | obj   | 最新剧集信息 |                               |
| follow_status    | num   | 追剧状态     | 1：已追，2：追剧中，3：已看完 |
| progress         | str   | 观看进度     | 如 `"已看完"`                 |
| both_follow      | bool  | 是否同时关注 |                               |
| url              | str   | 播放链接     |                               |
| styles           | array | 标签列表     | 如 `["剧情","犯罪"]`          |
| evaluate         | str   | 简介         |                               |
| summary          | str   | 详细简介     |                               |
| publish          | obj   | 上映信息     |                               |
| first_ep_info    | obj   | 正片信息     |                               |
| formal_ep_count  | num   | 正片数量     | 通常为 1                      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "list": [
            {
                "season_id": 45456,
                "season_type": 2,
                "season_type_name": "电影",
                "title": "孤注一掷",
                "cover": "https://i0.hdslb.com/bfs/bangumi/image/xxx.png",
                "stat": {
                    "follow": 673703,
                    "view": 31842323,
                    "likes": 308681
                },
                "rating": {
                    "score": 9,
                    "count": 3712
                },
                "follow_status": 2,
                "progress": "已看完",
                "both_follow": true,
                "styles": ["剧情", "犯罪"]
            }
        ],
        "pn": 1,
        "ps": 24,
        "total": 3
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
curl 'https://api.bilibili.com/x/space/bangumi/follow/list?vmid=3690995472402999&type=2&pn=1&ps=24&platform=web&follow_status=0&web_location=0.0&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`type=2`**：固定值，表示电影/影视内容。
3. **`follow_status`**：
   - `0`：全部
   - `1`：追剧中
   - `2`：已看完
4. **电影与番剧的区别**：
   - `total_count` 通常为 1（正片）
   - `new_ep.index_show` 显示上映日期而非集数
   - `duration` 为正片总时长（毫秒）
5. **与追番列表的关系**：共用接口路径 `/x/space/bangumi/follow/list`，通过 `type` 参数区分（`1`：番剧，`2`：电影）。
6. **`series` 字段**：部分电影可能为空对象，没有系列信息。


### 📂 追番/追剧模块文件清单

| 文件                            | 内容                 |
| ------------------------------- | -------------------- |
| `bili-space-bangumi-api.md`     | 追番列表（`type=1`） |
| `bili-space-cinema-list-api.md` | 追剧列表（`type=2`） |
