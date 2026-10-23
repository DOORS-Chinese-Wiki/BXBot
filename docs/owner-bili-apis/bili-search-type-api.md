# 综合搜索

## 接口描述

根据关键词搜索 B站 内容，支持按类型筛选（用户、视频、番剧等）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于搜索结果页面展示。**该接口需要 WBI 签名。**


## 接口地址

```
GET https://api.bilibili.com/x/web-interface/wbi/search/type
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：✅ 需要


## 请求参数（URL Query）

| 参数名            | 类型 | 内容             | 必要性   | 备注                                                         |
| ----------------- | ---- | ---------------- | -------- | ------------------------------------------------------------ |
| `search_type`     | str  | 搜索类型         | **必要** | `bili_user`：用户，`video`：视频，`bangumi`：番剧，`live`：直播，`article`：专栏 |
| `keyword`         | str  | 搜索关键词       | **必要** | URL 编码，如 `%E6%B4%9B%E5%B0%91%E7%88%B7`                   |
| `page`            | num  | 页码             | 非必要   | 默认 1                                                       |
| `page_size`       | num  | 每页数量         | 非必要   | 默认 36                                                      |
| `category_id`     | str  | 分类 ID          | 非必要   | 默认为空                                                     |
| `order`           | str  | 排序方式         | 非必要   | `totalrank`：综合排序，`pubdate`：最新发布，`click`：最多播放 |
| `duration`        | num  | 视频时长         | 非必要   | `0`：全部，`1`：10 分钟以下，`2`：10-30 分钟，`3`：30-60 分钟，`4`：60 分钟以上 |
| `pubtime_begin_s` | num  | 发布时间（起始） | 非必要   | Unix 时间戳（秒）                                            |
| `pubtime_end_s`   | num  | 发布时间（结束） | 非必要   | Unix 时间戳（秒）                                            |
| `highlight`       | num  | 是否高亮         | 非必要   | `1`：高亮匹配词                                              |
| `single_column`   | num  | 单列模式         | 非必要   | `0`：双列，`1`：单列                                         |
| `platform`        | str  | 平台标识         | 非必要   | `pc`                                                         |
| `web_location`    | str  | 来源标识         | 非必要   | `1430654`                                                    |
| `w_rid`           | str  | WBI 签名         | **必要** | 见 WBI 签名算法                                              |
| `wts`             | num  | WBI 时间戳       | **必要** | 秒级 Unix 时间戳                                             |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `message` | str  | 状态信息 | `"OK"`     |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段              | 类型  | 内容           | 备注       |
| ----------------- | ----- | -------------- | ---------- |
| `seid`            | str   | 搜索会话 ID    |            |
| `page`            | num   | 当前页码       |            |
| `pagesize`        | num   | 每页数量       |            |
| `numResults`      | num   | 总结果数       |            |
| `numPages`        | num   | 总页数         |            |
| `suggest_keyword` | str   | 建议关键词     | 通常为空   |
| `rqt_type`        | str   | 请求类型       | `"search"` |
| `exp_list`        | obj   | 实验配置列表   |            |
| `egg_hit`         | num   | 彩蛋命中       | `0`：否    |
| `result`          | array | 搜索结果列表   |            |
| `show_column`     | num   | 是否显示专栏   |            |
| `in_black_key`    | num   | 是否命中黑名单 |            |
| `in_white_key`    | num   | 是否命中白名单 |            |

### `exp_list` 对象

实验 ID 列表，每个 key 为实验名，值为 `true`/`false`。如 `"100010": true`。

### `result` 数组元素（`search_type=bili_user`）

| 字段               | 类型  | 内容           | 备注                        |
| ------------------ | ----- | -------------- | --------------------------- |
| `type`             | str   | 条目类型       | `"bili_user"`               |
| `mid`              | num   | 用户 UID       |                             |
| `uname`            | str   | 用户昵称       |                             |
| `usign`            | str   | 用户签名       |                             |
| `fans`             | num   | 粉丝数         |                             |
| `videos`           | num   | 投稿数         |                             |
| `upic`             | str   | 头像地址       | 相对路径                    |
| `face_nft`         | num   | 是否 NFT 头像  | `0`：否，`1`：是            |
| `face_nft_type`    | num   | NFT 头像类型   |                             |
| `verify_info`      | str   | 认证信息       |                             |
| `level`            | num   | 用户等级       | 1-6                         |
| `gender`           | num   | 性别           | `1`：男，`2`：女，`3`：保密 |
| `is_upuser`        | num   | 是否 UP 主     | `1`：是                     |
| `is_live`          | num   | 是否直播中     | `0`：否，`1`：是            |
| `room_id`          | num   | 直播间 ID      | 0 表示无                    |
| `res`              | array | 相关视频列表   | 该用户的代表作品            |
| `official_verify`  | obj   | 官方认证信息   |                             |
| `hit_columns`      | array | 命中的搜索字段 | 如 `["uname"]`              |
| `is_senior_member` | num   | 是否资深会员   |                             |

### `official_verify` 对象

| 字段   | 类型 | 内容     | 备注                          |
| ------ | ---- | -------- | ----------------------------- |
| `type` | num  | 认证类型 | `0`：UP 主认证，`127`：无认证 |
| `desc` | str  | 认证描述 |                               |

### `res` 数组元素（代表作品）

| 字段              | 类型 | 内容         | 备注              |
| ----------------- | ---- | ------------ | ----------------- |
| `aid`             | num  | 视频 AV ID   |                   |
| `bvid`            | str  | 视频 BV ID   |                   |
| `title`           | str  | 视频标题     |                   |
| `pubdate`         | num  | 发布时间戳   | Unix 时间戳（秒） |
| `arcurl`          | str  | 视频链接     |                   |
| `pic`             | str  | 封面图地址   | 相对路径          |
| `play`            | str  | 播放量       |                   |
| `dm`              | num  | 弹幕数       |                   |
| `coin`            | num  | 投币数       |                   |
| `fav`             | num  | 收藏数       |                   |
| `desc`            | str  | 视频简介     |                   |
| `duration`        | str  | 视频时长     | 格式 `"MM:SS"`    |
| `is_pay`          | num  | 是否付费     | `0`：否           |
| `is_union_video`  | num  | 是否联合投稿 | `0`：否           |
| `is_charge_video` | num  | 是否充电专属 | `0`：否           |


## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "seid": "6820065602913587205",
        "page": 1,
        "pagesize": 36,
        "numResults": 794,
        "numPages": 23,
        "suggest_keyword": "",
        "rqt_type": "search",
        "result": [
            {
                "type": "bili_user",
                "mid": 1447574,
                "uname": "洛少爷",
                "usign": "原创音乐人，全平台ID：洛少爷",
                "fans": 1553334,
                "videos": 326,
                "upic": "//i1.hdslb.com/bfs/face/xxx.jpg",
                "face_nft": 0,
                "level": 6,
                "gender": 1,
                "is_upuser": 1,
                "is_live": 0,
                "room_id": 936475,
                "res": [
                    {
                        "aid": 117083056774827,
                        "bvid": "BV1Ubgj69Ehr",
                        "title": "我和你飞到蓝蓝的天边~",
                        "pubdate": 1786546053,
                        "play": "87243",
                        "dm": 993,
                        "coin": 2418,
                        "fav": 5616,
                        "duration": "0:17"
                    }
                ],
                "official_verify": {
                    "type": 0,
                    "desc": "bilibili 知名音乐UP主"
                },
                "hit_columns": ["uname"]
            },
            {
                "type": "bili_user",
                "mid": 3546388166085549,
                "uname": "洛少爷的耳坠",
                "usign": "“如果地球没有上线 我依旧会爱你 不会改变”—《地球上线》",
                "fans": 322,
                "videos": 1,
                "level": 2,
                "gender": 3,
                "is_upuser": 1,
                "is_live": 0,
                "room_id": 0,
                "official_verify": {
                    "type": 127,
                    "desc": ""
                },
                "hit_columns": ["uname"]
            }
        ],
        "show_column": 0,
        "in_black_key": 0,
        "in_white_key": 0
    }
}
```


## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | WBI 签名缺失或错误          |
| -403   | 风控拦截                    |
| -404   | 搜索无结果                  |


## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=bili_user&keyword=%E6%B4%9B%E5%B0%91%E7%88%B7&page=1&page_size=36&highlight=1&platform=pc&web_location=1430654&w_rid=xxx&wts=xxx' \
  -X GET \
  -H 'Referer: https://search.bilibili.com/' \
  -H 'Origin: https://search.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **需要 WBI 签名**：该接口必须携带 WBI 签名。
2. **`search_type` 枚举值**：`bili_user`（用户）、`video`（视频）、`bangumi`（番剧）、`live`（直播）、`article`（专栏）。
3. **`keyword` 必须 URL 编码**：中文字符需转码为百分号编码。
4. **`res` 数组**：仅返回最多 3 个代表作品，非完整投稿列表。
5. **分页**：`page_size` 默认为 36，最大可能为 50。
6. **`official_verify.type`**：`0` 表示 UP 主认证，`127` 表示无认证。


## 相关接口

| 功能     | 接口路径                   | 说明                      |
| -------- | -------------------------- | ------------------------- |
| 搜索建议 | `/x/web-interface/suggest` | 搜索框联想词，需 WBI 签名 |
