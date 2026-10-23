# 历史记录搜索

## 接口描述

根据关键词、时间范围、视频时长等条件，搜索当前登录用户的观看历史记录。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于在历史记录中搜索已观看过的内容。


## 接口地址

```
GET https://api.bilibili.com/x/web-interface/history/search
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名             | 类型 | 内容         | 必要性   | 备注                                                         |
| ------------------ | ---- | ------------ | -------- | ------------------------------------------------------------ |
| `pn`               | num  | 页码         | 非必要   | 默认 1                                                       |
| `keyword`          | str  | 搜索关键词   | **必要** | URL 编码，如 `%E6%B4%9B%E5%B0%91%E7%88%B7`                   |
| `business`         | str  | 内容类型     | 非必要   | `all`：全部（默认），`archive`：视频，`pgc`：番剧，`live`：直播，`article`：专栏 |
| `add_time_start`   | num  | 起始时间戳   | 非必要   | 0 表示不限                                                   |
| `add_time_end`     | num  | 结束时间戳   | 非必要   | 0 表示不限                                                   |
| `arc_max_duration` | num  | 最大视频时长 | 非必要   | 单位：秒，0 表示不限                                         |
| `arc_min_duration` | num  | 最小时长     | 非必要   | 单位：秒，0 表示不限                                         |
| `device_type`      | num  | 设备类型     | 非必要   | 0 表示不限                                                   |
| `web_location`     | str  | 来源标识     | 非必要   | `0.0`                                                        |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `message` | str  | 状态信息 | `"OK"`     |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段       | 类型  | 内容           | 备注                                        |
| ---------- | ----- | -------------- | ------------------------------------------- |
| `has_more` | bool  | 是否有更多数据 | `true`：有下一页                            |
| `page`     | obj   | 分页信息       |                                             |
| `list`     | array | 历史记录列表   | 结构同 `bili-history-api.md` 的 `list` 元素 |

### `page` 对象

| 字段    | 类型 | 内容     | 备注 |
| ------- | ---- | -------- | ---- |
| `pn`    | num  | 当前页码 |      |
| `total` | num  | 总记录数 |      |

### `list` 数组元素

| 字段          | 类型 | 内容             | 备注                                |
| ------------- | ---- | ---------------- | ----------------------------------- |
| `title`       | str  | 视频标题         |                                     |
| `cover`       | str  | 封面图地址       |                                     |
| `history`     | obj  | 历史记录详情     | 含 `oid`、`bvid`、`cid`、`business` |
| `author_name` | str  | UP 主名称        |                                     |
| `author_mid`  | num  | UP 主 UID        |                                     |
| `view_at`     | num  | 观看时间戳       | Unix 时间戳（秒）                   |
| `progress`    | num  | 播放进度（秒）   | `-1` 表示已看完或未记录             |
| `duration`    | num  | 视频总时长（秒） |                                     |
| `is_fav`      | num  | 是否已收藏       | `1`：已收藏                         |
| `tag_name`    | str  | 分区/标签名称    | 如 `"翻唱"`、`"原创音乐"`           |


## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "has_more": true,
        "page": {
            "pn": 1,
            "total": 48
        },
        "list": [
            {
                "title": "洛少爷7月29日直播录屏",
                "cover": "http://i1.hdslb.com/bfs/archive/xxx.jpg",
                "history": {
                    "oid": 117002593310397,
                    "bvid": "BV1F83268EXY",
                    "cid": 40407140731,
                    "business": "archive"
                },
                "author_name": "此刻又在想你",
                "author_mid": 3546961875568776,
                "view_at": 1785319402,
                "progress": -1,
                "duration": 3873,
                "is_fav": 0,
                "tag_name": "翻唱"
            }
        ]
    }
}
```


## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | 请求参数错误                |
| -403   | 风控拦截                    |


## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/web-interface/history/search?pn=1&keyword=%E6%B4%9B%E5%B0%91%E7%88%B7&business=all&web_location=0.0' \
  -X GET \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **需要登录态**：必须携带有效的 `SESSDATA` Cookie，否则返回 `-101`。
2. **关键词必须携带**：`keyword` 为空时接口可能返回空列表或异常。
3. **`business` 筛选**：`all` 为全部，`archive` 仅视频，`pgc` 仅番剧，`live` 仅直播，`article` 仅专栏。
4. **时间范围筛选**：`add_time_start` / `add_time_end` 为 Unix 时间戳（秒），0 表示不限。
5. **时长筛选**：仅对视频类型有效，单位秒。
6. **页码分页**：使用传统的 `pn` 页码分页，与历史记录列表接口的游标分页不同。
7. **搜索范围**：仅搜索当前用户的历史记录，非全站搜索。


## 相关接口

| 功能             | 接口路径                              | 说明                     |
| ---------------- | ------------------------------------- | ------------------------ |
| 历史记录列表     | `GET /x/web-interface/history/cursor` | 游标分页获取全部历史记录 |
| 删除单条历史记录 | `POST /x/v2/history/delete`           | 需 CSRF                  |
| 清空全部历史记录 | `POST /x/v2/history/clear`            | 需 CSRF                  |
| 视频信息         | `GET /x/web-interface/view`           | 通过 BV 号获取视频详情   |