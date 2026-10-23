# 用户空间隐私设置

## 接口描述

获取指定用户的个人空间隐私设置，包含各模块的公开权限和页面模块排序。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于用户空间隐私设置页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/setting
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注                       |
| ------------ | ---- | -------- | -------- | -------------------------- |
| mid          | num  | 用户 UID | **必要** | 要查询的用户 ID            |
| web_location | str  | 来源标识 | 非必要   | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/setting?mid=3690995472402999&web_location=333.1387
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

| 字段            | 类型  | 内容              | 备注             |
| --------------- | ----- | ----------------- | ---------------- |
| privacy         | obj   | 隐私设置项        | 各字段含义见下方 |
| show_nft_switch | bool  | 是否显示 NFT 开关 |                  |
| index_order     | array | 空间模块排序列表  |                  |

### `privacy` 对象

| 字段                | 类型 | 内容                               | 备注                         |
| ------------------- | ---- | ---------------------------------- | ---------------------------- |
| bangumi             | num  | 公开追番追剧                       | 1：公开                      |
| bbq                 | num  | 公开最近玩过的游戏                 |                              |
| channel             | num  | 公开我的关注列表                   |                              |
| charge_video        | num  | 投稿视频列表中展现包月充电专属视频 |                              |
| close_space_medal   | num  | 关闭空间勋章展示                   | 0：未关闭（即公开），1：关闭 |
| coins_video         | num  | 公开最近投币的视频                 |                              |
| comic               | num  | 公开我的追漫（仅APP）              |                              |
| disable_following   | num  | 关闭关注列表展示                   | 1：关闭（即不公开）          |
| disable_show_fans   | num  | 关闭粉丝列表展示                   | 1：关闭（即不公开）          |
| disable_show_school | num  | 关闭学校信息展示                   | 1：关闭（即不公开）          |
| dress_up            | num  | 公开拥有的粉丝装扮（仅APP）        |                              |
| fav_video           | num  | 公开我的收藏                       |                              |
| groups              | num  | 公开我的个人标签                   |                              |
| lesson_video        | num  | 投稿视频列表中展现课堂视频         |                              |
| likes_video         | num  | 公开最近点赞的视频                 |                              |
| live_playback       | num  | 投稿视频列表中展现直播回放         |                              |
| only_show_wearing   | num  | 勋章墙仅显示佩戴中的勋章           | 0：显示全部，1：仅显示佩戴中 |
| played_game         | num  | 公开最近玩过的游戏                 |                              |
| tags                | num  | 公开我的个人标签                   |                              |
| user_info           | num  | 公开我的生日                       |                              |

> **数值说明**：`1` 表示公开/开启，`0` 表示不公开/关闭。部分字段的 `0`/`1` 含义相反（如 `disable_*` 系列），详见备注。

### `index_order` 数组元素

| 字段 | 类型 | 内容     | 备注                                |
| ---- | ---- | -------- | ----------------------------------- |
| id   | num  | 模块 ID  |                                     |
| name | str  | 模块名称 | 如 `"我的稿件"`、`"最近点赞的视频"` |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "privacy": {
            "bangumi": 1,
            "bbq": 1,
            "channel": 1,
            "charge_video": 1,
            "close_space_medal": 0,
            "coins_video": 0,
            "comic": 1,
            "disable_following": 1,
            "disable_show_fans": 1,
            "disable_show_school": 1,
            "dress_up": 1,
            "fav_video": 1,
            "groups": 1,
            "lesson_video": 1,
            "likes_video": 1,
            "live_playback": 1,
            "only_show_wearing": 0,
            "played_game": 0,
            "tags": 1,
            "user_info": 1
        },
        "show_nft_switch": false,
        "index_order": [
            {
                "id": 1,
                "name": "我的稿件"
            },
            {
                "id": 10,
                "name": "最近点赞的视频"
            },
            {
                "id": 5,
                "name": "最近投币的视频"
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
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/space/setting?mid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **查询他人设置**：`mid` 可指定任意用户，但返回的是该用户设置的公开选项。
3. **字段命名差异**：
   - 部分字段为正向控制（`1` = 公开），如 `fav_video`、`likes_video`
   - 部分字段为反向控制（`1` = 关闭/不公开），如 `disable_following`、`disable_show_fans`
4. **`only_show_wearing`**：控制勋章墙是否仅显示佩戴中的勋章，与 `close_space_medal` 配合使用。
5. **`index_order`**：控制用户空间主页各模块的显示顺序，可根据 `id` 和 `name` 调整。


### 📂 用户空间模块文件清单

| 文件                             | 内容               |
| -------------------------------- | ------------------ |
| `bili-space-user-info-api.md`    | 用户空间主页信息   |
| `bili-space-myinfo-api.md`       | 我的空间信息（V2） |
| `bili-space-upstat-api.md`       | 空间统计数据       |
| `bili-space-navnum-api.md`       | 空间导航计数       |
| `bili-space-archive-api.md`      | 投稿列表           |
| `bili-space-bangumi-api.md`      | 追番列表           |
| `bili-space-cinema-list-api.md`  | 追剧列表           |
| `bili-space-top-api.md`          | 置顶视频           |
| `bili-space-coin-video-api.md`   | 投币视频列表       |
| `bili-space-dynamic-feed-api.md` | 空间动态列表       |
| **`bili-space-setting-api.md`**  | **空间隐私设置**   |
