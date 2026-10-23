# 评论列表

## 接口描述

获取指定对象的评论区主列表，支持视频评论（`type=1`）和图文动态评论（`type=12`），包含评论内容、用户信息、子回复、置顶评论等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于视频/图文动态评论区展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/v2/reply/wbi/main
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名         | 类型 | 内容        | 必要性   | 备注                                                       |
| -------------- | ---- | ----------- | -------- | ---------------------------------------------------------- |
| oid            | num  | 对象 ID     | **必要** | 视频的 `aid` 或图文动态的 `opus_id`                        |
| type           | num  | 评论类型    | **必要** | `1`：视频评论，`12`：图文动态评论                          |
| mode           | num  | 排序模式    | 非必要   | `3`：热门评论，`2`：按时间                                 |
| pagination_str | str  | 翻页游标    | 非必要   | 首次请求传 `{"offset":""}`，后续使用响应中的 `next_offset` |
| plat           | num  | 平台标识    | 非必要   | `1`：Web                                                   |
| seek_rpid      | str  | 定位评论 ID | 非必要   | 用于跳转到指定评论                                         |
| web_location   | str  | 来源标识    | 非必要   | 固定传 `1315875` 或类似值                                  |
| w_rid          | str  | WBI 签名    | **必要** | 见 WBI 签名算法                                            |
| wts            | num  | WBI 时间戳  | **必要** | 秒级 Unix 时间戳                                           |

**示例请求 URL（视频评论）：**

```
https://api.bilibili.com/x/v2/reply/wbi/main?oid=116429382819235&type=1&mode=3&pagination_str={"offset":""}&plat=1&seek_rpid=&web_location=1315875&w_rid=xxx&wts=xxx
```

**示例请求 URL（图文动态评论）：**

```
https://api.bilibili.com/x/v2/reply/wbi/main?oid=21848272&type=12&mode=3&pagination_str={"offset":""}&plat=1&seek_rpid=&web_location=1315875&w_rid=xxx&wts=xxx
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

| 字段        | 类型  | 内容           | 备注                 |
| ----------- | ----- | -------------- | -------------------- |
| cursor      | obj   | 翻页游标信息   |                      |
| replies     | array | 评论列表       |                      |
| top         | obj   | 置顶评论       | 包含 `upper`、`vote` |
| top_replies | array | 置顶评论列表   |                      |
| effects     | obj   | 特效信息       |                      |
| assist      | num   | 辅助信息       |                      |
| blacklist   | num   | 黑名单状态     |                      |
| vote        | num   | 投票状态       |                      |
| config      | obj   | 评论区配置     |                      |
| upper       | obj   | UP 主信息      |                      |
| control     | obj   | 评论区控制配置 |                      |
| note        | num   | 笔记标识       |                      |

### `cursor` 对象

| 字段             | 类型  | 内容           | 备注               |
| ---------------- | ----- | -------------- | ------------------ |
| is_begin         | bool  | 是否是第一页   |                    |
| prev             | num   | 上一页游标     |                    |
| next             | num   | 下一页游标     |                    |
| is_end           | bool  | 是否最后一页   |                    |
| pagination_reply | obj   | 分页回复信息   | 包含 `next_offset` |
| session_id       | str   | 会话 ID        |                    |
| mode             | num   | 当前排序模式   |                    |
| mode_text        | str   | 模式名称       |                    |
| all_count        | num   | 总评论数       |                    |
| support_mode     | array | 支持的排序模式 |                    |
| name             | str   | 模式名称       |                    |

### `replies` 数组元素

| 字段          | 类型  | 内容                 | 备注                      |
| ------------- | ----- | -------------------- | ------------------------- |
| rpid          | num   | 评论 ID              | 全局唯一                  |
| rpid_str      | str   | 评论 ID（字符串）    |                           |
| oid           | num   | 对象 ID              |                           |
| type          | num   | 评论类型             | `1`：视频，`12`：图文动态 |
| mid           | num   | 评论者 UID           |                           |
| root          | num   | 根评论 ID            | 0 表示主评论              |
| parent        | num   | 父评论 ID            | 0 表示主评论              |
| dialog        | num   | 对话 ID              |                           |
| count         | num   | 子回复总数           |                           |
| rcount        | num   | 子回复总数（含折叠） |                           |
| state         | num   | 评论状态             |                           |
| fansgrade     | num   | 粉丝等级             |                           |
| attr          | num   | 属性位               |                           |
| ctime         | num   | 发布时间戳           | Unix 时间戳（秒）         |
| like          | num   | 点赞数               |                           |
| action        | num   | 用户操作状态         | 0：无操作，1：已点赞      |
| member        | obj   | 评论者信息           |                           |
| content       | obj   | 评论内容             |                           |
| replies       | array | 子回复列表           |                           |
| up_action     | obj   | UP 主操作状态        |                           |
| invisible     | bool  | 是否不可见           |                           |
| card_label    | array | 卡片标签             | 如 `"UP主觉得很赞"`       |
| reply_control | obj   | 回复控制信息         |                           |
| folder        | obj   | 折叠状态             |                           |
| track_info    | str   | 追踪信息             |                           |

### `member` 对象

| 字段            | 类型 | 内容         | 备注 |
| --------------- | ---- | ------------ | ---- |
| mid             | str  | 用户 UID     |      |
| uname           | str  | 用户昵称     |      |
| handle          | str  | 用户 handle  |      |
| sex             | str  | 性别         |      |
| sign            | str  | 用户签名     |      |
| avatar          | str  | 头像地址     |      |
| rank            | str  | 等级         |      |
| level_info      | obj  | 等级信息     |      |
| pendant         | obj  | 挂件信息     |      |
| nameplate       | obj  | 头像框信息   |      |
| official_verify | obj  | 官方认证信息 |      |
| vip             | obj  | 大会员信息   |      |
| user_sailing    | obj  | 用户装扮信息 |      |
| user_sailing_v2 | obj  | 用户装扮 V2  |      |
| is_contractor   | bool | 是否契约者   |      |
| avatar_item     | obj  | 头像组件     |      |

### `content` 对象

| 字段          | 类型  | 内容            | 备注           |
| ------------- | ----- | --------------- | -------------- |
| message       | str   | 评论内容        | 包含表情文本   |
| members       | array | @提及的用户列表 |                |
| emote         | obj   | 表情信息        | key 为表情文本 |
| jump_url      | obj   | 跳转链接        |                |
| max_line      | num   | 最大行数        |                |
| pictures      | array | 图片列表        | 评论中的图片   |
| picture_scale | num   | 图片缩放比例    |                |

---

## 翻页说明

该接口使用 **游标分页**（`pagination_str`）：

1. **首次请求**：`pagination_str={"offset":""}`
2. **后续请求**：使用响应中 `cursor.pagination_reply.next_offset` 构造新的 `pagination_str`
3. **最后一页**：`cursor.is_end` 为 `true`

---

## 响应示例

### 视频评论（`type=1`）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "cursor": {
            "is_begin": true,
            "is_end": false,
            "all_count": 52,
            "mode": 3,
            "name": "热门评论",
            "pagination_reply": {
                "next_offset": "CAESEDE4MjY2Mjk3MTU2OTQzNjYiAggB"
            }
        },
        "replies": [
            {
                "rpid": 299423339856,
                "oid": 116429382819235,
                "type": 1,
                "mid": 3546618192202347,
                "ctime": 1776572362,
                "like": 19,
                "member": {
                    "mid": "3546618192202347",
                    "uname": "洛琏琴",
                    "avatar": "https://i0.hdslb.com/bfs/face/xxx.jpg"
                },
                "content": {
                    "message": "小蛋糕就应该老老实实呆在蛋糕店啊喂[洛少爷之南瓜糖果_眩晕]"
                }
            }
        ],
        "top": {
            "upper": {
                "rpid": 296737174289,
                "ctime": 1776595198,
                "like": 33
            }
        }
    }
}
```

### 图文动态评论（`type=12`）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "cursor": {
            "is_begin": true,
            "is_end": false,
            "all_count": 222,
            "mode": 3,
            "name": "热门评论",
            "pagination_reply": {
                "next_offset": "CAESEDE4MjY2MzI2OTQxMDQ0OTUiAggB"
            }
        },
        "replies": [
            {
                "rpid": 152460266528,
                "oid": 21848272,
                "type": 12,
                "mid": 1139640768,
                "ctime": 1676462556,
                "like": 178,
                "member": {
                    "mid": "1139640768",
                    "uname": "账号已注销",
                    "avatar": "https://i0.hdslb.com/bfs/face/member/noface.jpg"
                },
                "content": {
                    "message": "爷哥想起账号密码了[doge]"
                }
            }
        ],
        "top": {
            "upper": null
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

### 视频评论

```bash
curl 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=116429382819235&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://www.bilibili.com/video/BVxxx' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

### 图文动态评论

```bash
curl 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=21848272&type=12&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://www.bilibili.com/opus/xxx' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`type` 类型区分**：
   - `1`：视频评论
   - `12`：图文动态评论
3. **`oid` 来源**：
   - 视频：`aid`，可从视频信息接口 `/x/web-interface/view` 获取
   - 图文动态：`opus_id`，可从图文动态列表接口获取
4. **`mode` 排序**：
   - `3`：热门评论（默认）
   - `2`：按时间排序
5. **`pagination_str` 格式**：JSON 字符串，包含 `offset` 字段
6. **`card_label`**：表示该评论的特殊标签，如 `"UP主觉得很赞"`
7. **`up_action`**：表示 UP 主对该评论的操作状态（点赞、回复等）
8. **`top` 和 `top_replies`**：分别返回置顶评论对象和置顶评论列表
