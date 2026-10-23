# 获取番剧剧集列表

## 接口描述

获取指定番剧（`season_id`）的所有剧集列表，包含正片、PV、预告等不同章节的内容，以及每集的播放统计、OP/ED 时间点等信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于番剧播放页面展示所有剧集。

---

## 接口地址

```
GET https://api.bilibili.com/pgc/view/web/ep/list
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名    | 类型 | 内容    | 必要性   | 备注                                       |
| --------- | ---- | ------- | -------- | ------------------------------------------ |
| season_id | num  | 剧集 ID | **必要** | 番剧的唯一标识，可从追番列表或番剧页面获取 |

**示例请求 URL：**

```
https://api.bilibili.com/pgc/view/web/ep/list?season_id=76110
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注        |
| ------- | ---- | -------- | ----------- |
| code    | num  | 状态码   | 0 表示成功  |
| message | str  | 状态信息 | `"success"` |
| result  | obj  | 数据本体 |             |

### `result` 对象

| 字段          | 类型  | 内容         | 备注                      |
| ------------- | ----- | ------------ | ------------------------- |
| episodes      | array | 正片剧集列表 | 按顺序排列，每集一个对象  |
| section       | array | 章节列表     | 包含 PV、预告等非正片内容 |
| play_strategy | obj   | 播放策略配置 | 控制播放逻辑              |

### `episodes` 数组元素

| 字段           | 类型 | 内容             | 备注                           |
| -------------- | ---- | ---------------- | ------------------------------ |
| id             | num  | 剧集 ID          | 同 `ep_id`                     |
| ep_id          | num  | 剧集 ID          |                                |
| aid            | num  | 视频 AV ID       |                                |
| bvid           | str  | 视频 BV ID       |                                |
| cid            | num  | 视频 CID         |                                |
| title          | str  | 集数编号         | 如 `"1"`、`"2"`                |
| long_title     | str  | 完整标题         | 如 `"其一 厕所里的花子"`       |
| show_title     | str  | 展示标题         | 如 `"第1话 其一 厕所里的花子"` |
| cover          | str  | 剧集封面图地址   |                                |
| duration       | num  | 视频时长（毫秒） |                                |
| pub_time       | num  | 发布时间戳       | Unix 时间戳（秒）              |
| status         | num  | 状态             | `13`：已完结                   |
| badge          | str  | 角标文案         | 如 `"会员"`                    |
| badge_type     | num  | 角标类型         |                                |
| badge_info     | obj  | 角标详细信息     | 包含 `text`、`bg_color`        |
| link           | str  | 播放链接         |                                |
| share_url      | str  | 分享链接         |                                |
| share_copy     | str  | 分享文案         |                                |
| short_link     | str  | 短链接           |                                |
| dimension      | obj  | 视频尺寸         | `width`、`height`、`rotate`    |
| rights         | obj  | 权限信息         |                                |
| skip           | obj  | OP/ED 时间点     |                                |
| stat           | obj  | 统计数据         |                                |
| stat_for_unity | obj  | 统一统计格式     | 包含 `vt`、`danmaku` 等        |
| subtitle       | str  | 副标题           | 如 `"已观看5398.4万次"`        |

### `skip` 对象

| 字段 | 类型 | 内容      | 备注                 |
| ---- | ---- | --------- | -------------------- |
| op   | obj  | OP 时间点 | `start`、`end`（秒） |
| ed   | obj  | ED 时间点 | `start`、`end`（秒） |

### `stat` 对象

| 字段     | 类型 | 内容   | 备注 |
| -------- | ---- | ------ | ---- |
| play     | num  | 播放量 |      |
| danmakus | num  | 弹幕数 |      |
| reply    | num  | 评论数 |      |
| likes    | num  | 点赞数 |      |
| coin     | num  | 投币数 |      |

### `section` 数组元素

| 字段     | 类型  | 内容               | 备注                           |
| -------- | ----- | ------------------ | ------------------------------ |
| id       | num   | 章节 ID            |                                |
| title    | str   | 章节标题           | 如 `"PV"`、`"预告"`            |
| type     | num   | 章节类型           | `1`：PV/预告，`0`：正片        |
| episodes | array | 该章节下的剧集列表 | 结构与 `episodes` 数组元素相同 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "success",
    "result": {
        "episodes": [
            {
                "id": 1414782,
                "ep_id": 1414782,
                "aid": 113876159038682,
                "bvid": "BV1sqfBYuEn7",
                "cid": 28789312431,
                "title": "1",
                "long_title": "其一 厕所里的花子",
                "show_title": "第1话 其一 厕所里的花子",
                "cover": "http://i0.hdslb.com/bfs/archive/xxx.png",
                "duration": 1425966,
                "pub_time": 1737887400,
                "status": 13,
                "badge": "会员",
                "stat": {
                    "play": 9228664,
                    "danmakus": 32053,
                    "likes": 107076,
                    "coin": 34390
                },
                "skip": {
                    "op": { "start": 125, "end": 215 },
                    "ed": { "start": 1331, "end": 1420 }
                },
                "link": "https://www.bilibili.com/bangumi/play/ep1414782"
            }
        ],
        "section": [
            {
                "id": 136627,
                "title": "PV",
                "type": 1,
                "episodes": [
                    {
                        "id": 1366148,
                        "title": "PV1",
                        "stat": { "play": 1400608 }
                    }
                ]
            }
        ],
        "play_strategy": {
            "strategies": [
                "common_section-formal_first_ep",
                "formal-finish-next_season"
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
| -400   | 请求参数错误                |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/pgc/view/web/ep/list?season_id=76110' \
  -H 'Referer: https://www.bilibili.com/bangumi/play/ss76110' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`season_id` 来源**：可从追番列表接口（`/x/space/bangumi/follow/list`）的 `season_id` 字段获取，或从番剧页面 URL `ss{season_id}` 提取。
3. **正片与章节分离**：
   - `episodes`：按顺序排列的正片剧集
   - `section`：PV、预告、花絮等其他内容
4. **`skip` 字段**：提供 OP 和 ED 的起止时间（秒），可用于自动跳过片头片尾。
5. **播放统计**：`stat` 字段包含播放量、弹幕数、点赞数等，其中 `play` 和 `danmakus` 可用于热度展示。
6. **`badge` 字段**：标识是否需要大会员才能观看（如 `"会员"`）。


### 📂 番剧模块文件清单

| 文件                            | 内容                 |
| ------------------------------- | -------------------- |
| `bili-space-bangumi-api.md`     | 追番列表（`type=1`） |
| `bili-space-cinema-list-api.md` | 追剧列表（`type=2`） |
| `bili-bangumi-ep-list-api.md`   | 番剧剧集列表         |
