# 用户空间动态列表

## 接口描述

获取指定用户个人空间发布的所有动态（图文、视频、转发等），支持翻页和多种内容类型。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于用户空间动态页面展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：✅ 需要

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容                 | 必要性     | 备注                                          |
| --------------- | ---- | -------------------- | ---------- | --------------------------------------------- |
| host_mid        | num  | 目标用户 UID         | **必要**   | 要查询的用户 ID                               |
| offset          | str  | 翻页偏移量           | 非必要     | 首次请求传空字符串，后续使用响应中的 `offset` |
| timezone_offset | num  | 时区偏移             | 非必要     | 如 `-480`（东八区）                           |
| platform        | str  | 平台标识             | 非必要     | `web`                                         |
| features        | str  | 功能开关             | 非必要     | 逗号分隔，如 `itemOpusStyle,listOnlyfans,...` |
| web_location    | str  | 来源标识             | 非必要     | `0.0`                                         |
| dm_img_list     | str  | 风控参数（鼠标轨迹） | ⚠️ 风控要求 | JSON 数组字符串                               |

**示例请求 URL：**

```
https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid=3690995472402999&offset=&timezone_offset=-480&platform=web&features=itemOpusStyle,listOnlyfans&web_location=0.0&w_rid=xxx&wts=xxx
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

| 字段            | 类型  | 内容           | 备注               |
| --------------- | ----- | -------------- | ------------------ |
| items           | array | 动态列表       | 每个元素为一条动态 |
| update_num      | str   | 更新数量       |                    |
| update_baseline | str   | 下次请求基线   | 翻页时使用         |
| offset          | str   | 下次请求偏移量 | 翻页时使用         |
| has_more        | bool  | 是否有更多数据 | `true`：有下一页   |
| total           | str   | 总数           |                    |

### `items` 数组元素

| 字段    | 类型     | 内容              | 备注                                                         |
| ------- | -------- | ----------------- | ------------------------------------------------------------ |
| id_str  | str      | 动态 ID（字符串） | 全局唯一                                                     |
| type    | str      | 动态类型          | `DYNAMIC_TYPE_DRAW`：图文，`DYNAMIC_TYPE_AV`：视频投稿，`DYNAMIC_TYPE_FORWARD`：转发，`DYNAMIC_TYPE_COMMON_SQUARE`：装扮分享等 |
| visible | bool     | 是否可见          |                                                              |
| basic   | obj      | 基本信息          | 包含 `rid_str`、`comment_type`、`comment_id_str`、`jump_url` 等 |
| modules | obj      | 模块信息          | 核心内容载体                                                 |
| orig    | null/obj | 原始动态          | 转发动态时包含原始动态                                       |

### `modules` 对象

| 字段               | 类型 | 内容     | 备注                                                      |
| ------------------ | ---- | -------- | --------------------------------------------------------- |
| module_author      | obj  | 作者信息 | 含 `mid`、`name`、`face`、`vip`、`pendant`、`pub_time` 等 |
| module_more        | obj  | 更多操作 | 置顶、删除等                                              |
| module_dynamic     | obj  | 动态内容 | 核心内容                                                  |
| module_stat        | obj  | 统计数据 | 转发、评论、点赞数                                        |
| module_tag         | null | 标签     | 通常为 null                                               |
| module_extend      | null | 扩展信息 | 通常为 null                                               |
| module_interaction | null | 交互信息 | 通常为 null                                               |
| module_share_info  | null | 分享信息 | 通常为 null                                               |
| module_fold        | null | 折叠状态 | 通常为 null                                               |

### `module_author` 对象

| 字段            | 类型 | 内容          | 备注              |
| --------------- | ---- | ------------- | ----------------- |
| mid             | num  | 用户 UID      |                   |
| name            | str  | 用户昵称      |                   |
| face            | str  | 头像地址      |                   |
| face_nft        | bool | 是否 NFT 头像 |                   |
| pub_ts          | str  | 发布时间戳    | Unix 时间戳（秒） |
| pub_time        | str  | 发布时间描述  | 如 `"06月14日"`   |
| pub_action      | str  | 发布动作描述  | 如 `"投稿了视频"` |
| vip             | obj  | 大会员信息    |                   |
| pendant         | obj  | 挂件信息      |                   |
| official_verify | obj  | 官方认证信息  |                   |
| decoration_card | obj  | 装扮卡片信息  |                   |
| avatar          | obj  | 头像组件      | 前端渲染用        |

### `module_dynamic` 对象

| 字段  | 类型     | 内容     | 备注                         |
| ----- | -------- | -------- | ---------------------------- |
| topic | null/obj | 话题信息 | 含 `id`、`name`、`jump_url`  |
| desc  | null/obj | 文字描述 | 含 `text`、`rich_text_nodes` |
| major | obj      | 主要内容 | 根据动态类型不同结构不同     |

### `module_stat` 对象

| 字段     | 类型 | 内容     | 备注              |
| -------- | ---- | -------- | ----------------- |
| forward  | obj  | 转发统计 | `status`、`count` |
| comment  | obj  | 评论统计 | `status`、`count` |
| like     | obj  | 点赞统计 | `status`、`count` |
| coin     | null | 投币统计 | 通常为 null       |
| favorite | null | 收藏统计 | 通常为 null       |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "0",
    "data": {
        "update_num": "0",
        "update_baseline": "",
        "offset": "1195600757840150547",
        "has_more": true,
        "total": "0",
        "items": [
            {
                "id_str": "1213628393486024710",
                "type": "DYNAMIC_TYPE_DRAW",
                "visible": true,
                "modules": {
                    "module_author": {
                        "mid": 3690995472402999,
                        "name": "YunLv_L",
                        "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
                        "pub_time": "06月14日",
                        "vip": {
                            "type": 1,
                            "status": 1,
                            "nickname_color": "#FB7299"
                        }
                    },
                    "module_dynamic": {
                        "major": {
                            "type": "MAJOR_TYPE_OPUS",
                            "opus": {
                                "title": "RikkaHub-Armv7a 最新版",
                                "summary": {
                                    "text": "终于把32位的最新版RikkaHub编译出来了！..."
                                },
                                "pics": [
                                    {
                                        "url": "http://i0.hdslb.com/bfs/new_dyn/xxx.png",
                                        "width": 1920,
                                        "height": 1020
                                    }
                                ]
                            }
                        }
                    },
                    "module_stat": {
                        "comment": { "count": 2 },
                        "like": { "count": 3 }
                    }
                }
            },
            {
                "id_str": "1202662212364140551",
                "type": "DYNAMIC_TYPE_AV",
                "modules": {
                    "module_author": {
                        "pub_action": "投稿了视频"
                    },
                    "module_dynamic": {
                        "major": {
                            "type": "MAJOR_TYPE_ARCHIVE",
                            "archive": {
                                "bvid": "BV1rR5i6GEHP",
                                "aid": "116579002029229",
                                "title": "[开源项目]KernelBase",
                                "cover": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
                                "duration_text": "08:08",
                                "stat": { "play": "661" }
                            }
                        }
                    }
                }
            }
        ]
    }
}
```

---

## 动态类型说明（`type`）

| 类型                         | 含义          | `major.type`                  |
| ---------------------------- | ------------- | ----------------------------- |
| `DYNAMIC_TYPE_DRAW`          | 图文动态      | `MAJOR_TYPE_OPUS`             |
| `DYNAMIC_TYPE_AV`            | 视频投稿      | `MAJOR_TYPE_ARCHIVE`          |
| `DYNAMIC_TYPE_FORWARD`       | 转发动态      | 无 `major`，`orig` 中有原动态 |
| `DYNAMIC_TYPE_COMMON_SQUARE` | 装扮/通用分享 | `MAJOR_TYPE_COMMON`           |

---

## 翻页说明

使用 **基线游标分页**：

1. **首次请求**：`offset=`（空字符串）
2. **后续请求**：使用响应中 `offset` 作为下一次请求的 `offset` 参数
3. **最后一页**：`has_more` 为 `false`

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 请求成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -400   | WBI 签名缺失或错误          |
| -403   | 风控拦截                    |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid=3690995472402999&offset=&timezone_offset=-480&platform=web&features=itemOpusStyle,listOnlyfans&web_location=0.0&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`features` 参数**：控制前端功能开关，建议直接从浏览器抓包复制完整值。
3. **`offset` 翻页**：使用游标方式，不是传统的页码分页。
4. **动态类型丰富**：包含图文、视频、转发、装扮等多种内容类型，解析时需根据 `type` 判断。


### 📂 空间动态模块文件清单

| 文件                             | 内容                               |
| -------------------------------- | ---------------------------------- |
| `bili-space-dynamic-feed-api.md` | 用户空间动态列表（图文/视频/转发） |
| `bili-article-list-api.md`       | 图文动态列表（仅 `type=article`）  |
