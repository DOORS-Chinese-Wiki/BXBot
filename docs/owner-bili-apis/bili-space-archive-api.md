# 用户空间视频投稿列表 API

## 接口列表

### 1. 获取用户视频投稿列表

---

# 1. 获取用户视频投稿列表

## 接口描述

获取指定用户的所有视频投稿列表，支持分页、分区筛选、排序等。**该接口需要 WBI 签名**。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间展示用户的视频投稿。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/wbi/arc/search
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名           | 类型 | 内容                   | 必要性           | 备注                                 |
| ---------------- | ---- | ---------------------- | ---------------- | ------------------------------------ |
| mid              | num  | 目标用户 UID           | **必要**         | 要查询的用户 ID                      |
| pn               | num  | 页码                   | 非必要           | 默认 1                               |
| ps               | num  | 每页数量               | 非必要           | 默认 30，最大 50？                   |
| tid              | num  | 分区 ID                | 非必要           | 0 表示全部，具体分区代码参考原项目   |
| order            | str  | 排序方式               | 非必要           | `pubdate`：发布时间，`click`：播放量 |
| keyword          | str  | 关键词                 | 非必要           | 搜索标题关键词                       |
| platform         | str  | 平台标识               | 非必要           | 固定传 `web`                         |
| web_location     | str  | 来源标识               | 非必要           | 固定传 `0.0`                         |
| order_avoided    | bool | 是否跳过已看           | 非必要           | 默认 `true`                          |
| special_type     | str  | 特殊类型               | 非必要           | 默认为空                             |
| index            | num  | 索引                   | 非必要           | 默认为 0                             |
| dm_img_list      | str  | 风控参数（鼠标轨迹）   | **必要（风控）** | JSON 数组字符串                      |
| dm_img_str       | str  | 风控参数（GPU 信息）   | **必要（风控）** | Base64 编码                          |
| dm_cover_img_str | str  | 风控参数（渲染器信息） | **必要（风控）** | Base64 编码                          |
| dm_img_inter     | str  | 风控参数（交互信息）   | **必要（风控）** | JSON 字符串                          |
| w_rid            | str  | WBI 签名               | **必要**         | 见 WBI 签名算法                      |
| wts              | num  | WBI 时间戳             | **必要**         | 秒级 Unix 时间戳                     |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/wbi/arc/search?mid=123456789&pn=1&ps=40&order=pubdate&platform=web&w_rid=xxx&wts=xxx
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

| 字段            | 类型 | 内容             | 备注             |
| --------------- | ---- | ---------------- | ---------------- |
| list            | obj  | 列表数据         |                  |
| page            | obj  | 分页信息         |                  |
| episodic_button | obj  | 播放全部按钮信息 |                  |
| is_risk         | bool | 是否风控         | `false` 表示正常 |
| gaia_res_type   | num  | Gaia 资源类型    |                  |
| gaia_data       | null | Gaia 数据        | 通常为 null      |

### `list` 对象

| 字段  | 类型  | 内容     | 备注                           |
| ----- | ----- | -------- | ------------------------------ |
| vlist | array | 视频列表 | 每个元素为一条视频信息         |
| tlist | obj   | 分区统计 | key 为 `tid`，value 为分区信息 |

### `list.tlist` 对象

| 字段  | 类型 | 内容         | 备注                       |
| ----- | ---- | ------------ | -------------------------- |
| {tid} | obj  | 分区统计信息 | key 为分区代码（如 `160`） |

#### `tlist.{tid}` 对象

| 字段  | 类型 | 内容           | 备注                  |
| ----- | ---- | -------------- | --------------------- |
| tid   | num  | 分区 ID        |                       |
| count | num  | 该分区视频数量 |                       |
| name  | str  | 分区名称       | 如 `"生活"`、`"科技"` |

### `list.vlist` 数组元素

| 字段               | 类型 | 内容             | 备注                           |
| ------------------ | ---- | ---------------- | ------------------------------ |
| aid                | num  | 视频 AV ID       | 旧版视频 ID                    |
| bvid               | str  | 视频 BV ID       | 新版视频 ID，推荐使用          |
| title              | str  | 视频标题         |                                |
| description        | str  | 视频简介         |                                |
| pic                | str  | 封面图地址       | http 协议                      |
| author             | str  | UP 主名称        |                                |
| mid                | num  | UP 主 UID        |                                |
| typeid             | num  | 分区 ID          |                                |
| copyright          | str  | 版权类型         | `"1"`：原创，`"2"`：转载       |
| play               | num  | 播放量           |                                |
| comment            | num  | 评论数           |                                |
| video_review       | num  | 弹幕数           |                                |
| review             | num  | 审核状态         | 通常为 0                       |
| created            | num  | 发布时间戳       | Unix 时间戳（秒）              |
| length             | str  | 视频时长         | 格式 `"MM:SS"` 或 `"HH:MM:SS"` |
| subtitle           | str  | 字幕信息         | 通常为空                       |
| hide_click         | bool | 是否隐藏点击     |                                |
| is_pay             | num  | 是否付费视频     | 0：否                          |
| is_union_video     | num  | 是否联合视频     | 0：否                          |
| is_steins_gate     | num  | 是否互动视频     | 0：否                          |
| is_live_playback   | num  | 是否直播回放     | 0：否                          |
| is_lesson_video    | num  | 是否课程视频     | 0：否                          |
| is_lesson_finished | num  | 课程是否完结     | 0：否                          |
| lesson_update_info | str  | 课程更新信息     | 通常为空                       |
| jump_url           | str  | 跳转链接         | 通常为空                       |
| meta               | null | 元数据           | 通常为 null                    |
| is_avoided         | num  | 是否被回避       |                                |
| season_id          | num  | 合集/剧集 ID     | 0 表示无                       |
| attribute          | num  | 视频属性位掩码   | 见下方说明                     |
| is_charging_arc    | bool | 是否充电专属视频 |                                |
| elec_arc_type      | num  | 充电类型         |                                |
| elec_arc_badge     | str  | 充电徽章         |                                |
| vt                 | num  | 视频类型         |                                |
| enable_vt          | num  | 是否启用 VT      |                                |
| vt_display         | str  | VT 显示信息      |                                |
| playback_position  | num  | 播放进度（秒）   | 针对当前用户                   |
| is_self_view       | bool | 是否自己观看过   | `true` 表示已看过              |
| view_self_type     | num  | 观看类型         |                                |

#### `attribute` 位掩码说明

| 值      | 含义                     |
| ------- | ------------------------ |
| 16512   | 普通视频（常见）         |
| 8405120 | 特殊状态视频（如老视频） |

> 具体位含义待补充。

### `page` 对象

| 字段  | 类型 | 内容     | 备注 |
| ----- | ---- | -------- | ---- |
| pn    | num  | 当前页码 |      |
| ps    | num  | 每页数量 |      |
| count | num  | 总记录数 |      |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "list": {
            "slist": [],
            "tlist": {
                "160": {
                    "tid": 160,
                    "count": 3,
                    "name": "生活"
                },
                "188": {
                    "tid": 188,
                    "count": 2,
                    "name": "科技"
                }
            },
            "vlist": [
                {
                    "comment": 8,
                    "typeid": 230,
                    "play": 661,
                    "pic": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
                    "subtitle": "",
                    "description": "视频简介内容",
                    "copyright": "1",
                    "title": "视频标题",
                    "review": 0,
                    "author": "UP主名称",
                    "mid": 123456789,
                    "created": 1778855016,
                    "length": "08:08",
                    "video_review": 0,
                    "aid": 116579002029229,
                    "bvid": "BV1rR5i6GEHP",
                    "hide_click": false,
                    "is_pay": 0,
                    "is_union_video": 0,
                    "is_steins_gate": 0,
                    "is_live_playback": 0,
                    "is_lesson_video": 0,
                    "is_lesson_finished": 0,
                    "attribute": 16512,
                    "is_charging_arc": false,
                    "elec_arc_type": 0,
                    "is_self_view": false
                }
            ]
        },
        "page": {
            "pn": 1,
            "ps": 40,
            "count": 5
        },
        "is_risk": false
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | 请求错误/WBI 签名缺失或错误 |
| -403   | CSRF 验证失败或风控拦截     |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123456789&pn=1&ps=40&order=pubdate&platform=web&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误或带 `v_voucher` 的响应。具体算法参考原项目的 `wbi.md` 文档。
2. **`mid` 为必要参数**：必须指定目标用户的 UID。
3. **风控参数**：`dm_img_list`、`dm_img_str`、`dm_cover_img_str`、`dm_img_inter` 为设备指纹/行为采集参数，用于反爬风控。缺失可能导致 `-400` 或 `-403`。
   - `dm_img_list`：鼠标轨迹坐标数组（JSON 字符串）
   - `dm_img_str`：GPU/WebGL 信息（Base64）
   - `dm_cover_img_str`：渲染器驱动信息（Base64）
   - `dm_img_inter`：交互元素信息（JSON 字符串）
4. **`order_avoided`**：当设为 `true` 时，会跳过用户已看过的视频（仅对登录用户生效）。
5. **分页**：`ps` 最大可能为 50，超过可能会被截断或报错。
6. **`attribute` 字段**：位掩码值需进一步解析，目前已知 `16512` 为普通视频。
7. **`playback_position` 和 `is_self_view`**：仅当登录用户查询自己时有效，用于记录播放进度和观看状态。


## 相关接口汇总

| 功能             | 接口路径                    | 请求方式 | 签名 |
| ---------------- | --------------------------- | -------- | ---- |
| 用户视频投稿列表 | `/x/space/wbi/arc/search`   | GET      | WBI  |
| WBI 签名获取     | `/x/web-interface/nav`      | GET      | 无   |
| 用户基本信息     | `/x/space/wbi/acc/info`     | GET      | WBI  |
| 用户关系状态     | `/x/space/wbi/acc/relation` | GET      | WBI  |
