# 用户合集列表

## 接口描述

获取指定用户创建的所有视频合集（Season）和直播回放合集（Series）列表。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于用户空间合集页面展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/polymer/web-space/seasons_series_list
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容       | 必要性   | 备注             |
| ------------ | ---- | ---------- | -------- | ---------------- |
| mid          | num  | 用户 UID   | **必要** | 要查询的用户 ID  |
| page_num     | num  | 页码       | 非必要   | 默认 1           |
| page_size    | num  | 每页数量   | 非必要   | 默认 20          |
| web_location | str  | 来源标识   | 非必要   | 固定传 `0.0`     |
| w_rid        | str  | WBI 签名   | **必要** | 见 WBI 签名算法  |
| wts          | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳 |

**示例请求 URL：**

```
https://api.bilibili.com/x/polymer/web-space/seasons_series_list?mid=1447574&page_size=20&page_num=1&web_location=0.0&w_rid=xxx&wts=xxx
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

| 字段        | 类型 | 内容         | 备注 |
| ----------- | ---- | ------------ | ---- |
| items_lists | obj  | 合集列表数据 |      |

### `items_lists` 对象

| 字段         | 类型  | 内容             | 备注                         |
| ------------ | ----- | ---------------- | ---------------------------- |
| page         | obj   | 分页信息         |                              |
| seasons_list | array | 视频合集列表     | UP主创建的视频合集（Season） |
| series_list  | array | 直播回放合集列表 | 直播回放合集（Series）       |

### `page` 对象

| 字段      | 类型 | 内容     | 备注 |
| --------- | ---- | -------- | ---- |
| page_num  | num  | 当前页码 |      |
| page_size | num  | 每页条数 |      |
| total     | num  | 总记录数 |      |

### `seasons_list` 数组元素（视频合集）

| 字段        | 类型  | 内容                | 备注                      |
| ----------- | ----- | ------------------- | ------------------------- |
| meta        | obj   | 合集元数据          |                           |
| archives    | array | 合集内的视频列表    | 最近发布的视频（最多6个） |
| recent_aids | array | 合集内视频 AID 列表 |                           |

#### `meta` 对象（视频合集）

| 字段        | 类型 | 内容             | 备注              |
| ----------- | ---- | ---------------- | ----------------- |
| season_id   | num  | 合集 ID          | 全局唯一          |
| mid         | num  | UP 主 UID        |                   |
| title       | str  | 合集标题         |                   |
| name        | str  | 合集名称（别名） | 与 `title` 相同   |
| cover       | str  | 封面图地址       |                   |
| description | str  | 合集描述         |                   |
| category    | num  | 分类             | 0：普通           |
| total       | num  | 合集内视频总数   |                   |
| ptime       | num  | 最后更新时间戳   | Unix 时间戳（秒） |

#### `archives` 数组元素（视频信息）

| 字段              | 类型 | 内容           | 备注              |
| ----------------- | ---- | -------------- | ----------------- |
| aid               | num  | 视频 AV ID     |                   |
| bvid              | str  | 视频 BV ID     |                   |
| title             | str  | 视频标题       |                   |
| pic               | str  | 封面图地址     |                   |
| duration          | num  | 视频时长（秒） |                   |
| pubdate           | num  | 发布时间戳     | Unix 时间戳（秒） |
| ctime             | num  | 创建时间戳     | Unix 时间戳（秒） |
| state             | num  | 视频状态       | 0：正常           |
| ugc_pay           | num  | 是否 UGC 付费  | 0：否             |
| interactive_video | bool | 是否互动视频   |                   |
| enable_vt         | bool | 是否启用 VT    |                   |
| vt_display        | str  | VT 显示信息    |                   |
| playback_position | num  | 播放进度（秒） | 对当前登录用户    |
| stat              | obj  | 统计数据       |                   |

##### `stat` 对象

| 字段    | 类型 | 内容     | 备注 |
| ------- | ---- | -------- | ---- |
| view    | num  | 播放量   |      |
| danmaku | num  | 弹幕数   |      |
| vt      | num  | 视频类型 |      |

### `series_list` 数组元素（直播回放合集）

| 字段        | 类型  | 内容                | 备注                                                         |
| ----------- | ----- | ------------------- | ------------------------------------------------------------ |
| meta        | obj   | 合集元数据          | 结构与 `seasons_list.meta` 类似，包含 `series_id`、`total` 等 |
| archives    | array | 合集内的视频列表    |                                                              |
| recent_aids | array | 合集内视频 AID 列表 |                                                              |

#### `meta` 对象（直播回放合集）

| 字段           | 类型 | 内容           | 备注                  |
| -------------- | ---- | -------------- | --------------------- |
| series_id      | num  | 系列 ID        | 全局唯一              |
| mid            | num  | UP 主 UID      |                       |
| name           | str  | 合集名称       | 如 `"直播回放"`       |
| cover          | str  | 封面图地址     |                       |
| description    | str  | 合集描述       |                       |
| category       | num  | 分类           | 2：直播回放           |
| creator        | str  | 创建者         | `"auto"` 表示自动生成 |
| total          | num  | 合集内视频总数 |                       |
| state          | num  | 状态           | 2：正常               |
| ctime          | num  | 创建时间戳     |                       |
| mtime          | num  | 最后修改时间戳 |                       |
| last_update_ts | num  | 最后更新时间戳 |                       |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "items_lists": {
            "page": {
                "page_num": 1,
                "page_size": 20,
                "total": 12
            },
            "seasons_list": [
                {
                    "archives": [
                        {
                            "aid": 116890202542351,
                            "bvid": "BV1ucMH6hEtE",
                            "title": "【洛少爷翻唱】关于我今天成才的秘方...",
                            "duration": 211,
                            "stat": {
                                "view": 81844,
                                "danmaku": 240
                            }
                        }
                    ],
                    "meta": {
                        "season_id": 2421087,
                        "mid": 1447574,
                        "title": "洛少爷·翻唱精选集",
                        "cover": "https://archive.biliimg.com/bfs/archive/xxx.jpg",
                        "total": 210
                    },
                    "recent_aids": [
                        116890202542351,
                        114260709479094
                    ]
                }
            ],
            "series_list": [
                {
                    "archives": [
                        {
                            "aid": 115678518445999,
                            "bvid": "BV1ofmABxEQG",
                            "title": "【直播回放】一个普通的直播 2025年12月07日19点场"
                        }
                    ],
                    "meta": {
                        "series_id": 3222903,
                        "mid": 1447574,
                        "name": "直播回放",
                        "total": 126
                    },
                    "recent_aids": [
                        115678518445999,
                        115622163842463
                    ]
                }
            ]
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
| -400   | WBI 签名缺失或错误          |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/polymer/web-space/seasons_series_list?mid=1447574&page_size=20&page_num=1&web_location=0.0&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **两种合集类型**：
   - `seasons_list`：UP主手动创建的视频合集（如“翻唱精选集”）
   - `series_list`：直播回放自动生成的合集
3. **`archives` 列表**：每个合集只返回最近发布的 6 个视频，完整列表需通过其他接口获取。
4. **`category` 字段**：`0` 表示普通视频合集，`2` 表示直播回放合集。
5. **分页**：`page_size` 最大可能为 20，超过可能被截断。


### 📂 用户空间模块文件清单（更新）

| 文件                                 | 内容                 |
| ------------------------------------ | -------------------- |
| `bili-space-user-info-api.md`        | 用户空间主页信息     |
| `bili-space-myinfo-api.md`           | 我的空间信息（V2）   |
| `bili-space-upstat-api.md`           | 空间统计数据         |
| `bili-space-navnum-api.md`           | 空间导航计数         |
| `bili-space-archive-api.md`          | 投稿列表             |
| `bili-space-bangumi-api.md`          | 追番列表             |
| `bili-space-cinema-list-api.md`      | 追剧列表             |
| `bili-space-top-api.md`              | 置顶视频             |
| `bili-space-coin-video-api.md`       | 投币视频列表         |
| `bili-space-dynamic-feed-api.md`     | 空间动态列表         |
| `bili-space-setting-api.md`          | 空间隐私设置         |
| **`bili-space-seasons-list-api.md`** | **合集列表（新增）** |
