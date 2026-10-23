好的，收到！这是 `/x/relation/fans` 粉丝列表的完整抓包数据 🎯

---

## 关键发现

| 对比项           | 关注列表 `/followings`  | 粉丝列表 `/fans`                   |
| ---------------- | ----------------------- | ---------------------------------- |
| 翻页方式         | `pn` + `ps`（页码分页） | `offset` + `ps`（游标分页）        |
| `total`          | 70                      | 1539748                            |
| `attribute` 含义 | 你的关注状态（2/6）     | 粉丝对你的关注状态（0 = 未关注你） |
| 是否需要 WBI     | ❌ 不需要                | ❌ 不需要                           |

---

# 粉丝列表

## 接口描述

获取指定用户的粉丝列表（关注了该用户的人）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间粉丝列表页面展示。**受对方隐私设置影响，若对方关闭粉丝列表展示，将返回 53013。**


## 接口地址

```
GET https://api.bilibili.com/x/relation/fans
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名         | 类型 | 内容         | 必要性   | 备注                                    |
| -------------- | ---- | ------------ | -------- | --------------------------------------- |
| `vmid`         | num  | 目标用户 UID | **必要** | 要查询粉丝列表的用户                    |
| `pn`           | num  | 页码         | 非必要   | 默认 1，与 `offset` 二选一              |
| `offset`       | str  | 游标偏移量   | 非必要   | 首次请求为空，后续使用响应中的 `offset` |
| `ps`           | num  | 每页数量     | 非必要   | 默认 20，最大 50                        |
| `gaia_source`  | str  | 来源标识     | 非必要   | 如 `main_web`                           |
| `web_location` | str  | 来源标识     | 非必要   | 固定传 `333.1387`                       |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `message` | str  | 状态信息 | `"0"`      |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段         | 类型  | 内容       | 备注                         |
| ------------ | ----- | ---------- | ---------------------------- |
| `list`       | array | 粉丝列表   | 每个元素为一个粉丝信息       |
| `total`      | num   | 粉丝总数   |                              |
| `offset`     | str   | 下一页游标 | 翻页时作为 `offset` 参数传入 |
| `re_version` | num   | 版本标识   | 通常为 `0`                   |

### `list` 数组元素

| 字段              | 类型       | 内容               | 备注                                          |
| ----------------- | ---------- | ------------------ | --------------------------------------------- |
| `mid`             | num        | 用户 UID           |                                               |
| `attribute`       | num        | 关系属性           | `0`：未关注你                                 |
| `mtime`           | num        | 关注时间戳         | Unix 时间戳（秒），即该用户关注目标用户的时间 |
| `tag`             | array/null | 分组标签           | 粉丝列表通常为 `null`                         |
| `special`         | num        | 是否特别关注       | `0`：否                                       |
| `contract_info`   | obj        | 契约计划信息       | 通常为空对象                                  |
| `uname`           | str        | 昵称               |                                               |
| `face`            | str        | 头像 URL           |                                               |
| `sign`            | str        | 个人简介           |                                               |
| `face_nft`        | num        | 是否为 NFT 头像    | `0`：否                                       |
| `handle`          | str        | 用户 handle        | 通常为空                                      |
| `official_verify` | obj        | 官方认证信息       |                                               |
| `vip`             | obj        | 大会员信息         |                                               |
| `name_render`     | obj        | 昵称渲染信息       | 通常为空对象                                  |
| `nft_icon`        | str        | NFT 图标           | 通常为空                                      |
| `rec_reason`      | str        | 推荐理由           | 通常为空                                      |
| `track_id`        | str        | 追踪 ID            | 通常为空                                      |
| `follow_time`     | str        | 关注时间（字符串） | 通常为空                                      |

### `official_verify` 对象

| 字段   | 类型 | 内容     | 备注                         |
| ------ | ---- | -------- | ---------------------------- |
| `type` | num  | 认证类型 | `-1`：无认证，`0`：UP 主认证 |
| `desc` | str  | 认证描述 |                              |

### `vip` 对象

| 字段               | 类型 | 内容       | 备注                                      |
| ------------------ | ---- | ---------- | ----------------------------------------- |
| `vipType`          | num  | 大会员类型 | `0`：无，`1`：月度大会员，`2`：年度大会员 |
| `vipDueDate`       | num  | 到期时间戳 | 毫秒                                      |
| `vipStatus`        | num  | 状态       | `0`：未激活/已过期，`1`：生效中           |
| `label`            | obj  | 标签信息   |                                           |
| `avatar_subscript` | num  | 头像角标   | `0`：无，`1`：有                          |
| `nickname_color`   | str  | 昵称颜色   | 大会员粉色 `#FB7299`                      |


## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": [
            {
                "mid": 1036149724,
                "attribute": 0,
                "mtime": 1784157271,
                "tag": null,
                "special": 0,
                "contract_info": {},
                "uname": "汐语兰歌",
                "face": "https://i1.hdslb.com/bfs/face/xxx.jpg",
                "sign": "",
                "face_nft": 0,
                "handle": "",
                "official_verify": {
                    "type": -1,
                    "desc": ""
                },
                "vip": {
                    "vipType": 0,
                    "vipDueDate": 0,
                    "vipStatus": 0,
                    "avatar_subscript": 0,
                    "nickname_color": ""
                },
                "name_render": {},
                "nft_icon": "",
                "rec_reason": "",
                "track_id": "",
                "follow_time": ""
            },
            {
                "mid": 3706972970945079,
                "attribute": 0,
                "mtime": 1784156903,
                "tag": null,
                "special": 0,
                "uname": "忒热了義",
                "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
                "sign": "",
                "official_verify": {
                    "type": -1,
                    "desc": ""
                },
                "vip": {
                    "vipType": 0,
                    "vipDueDate": 0,
                    "vipStatus": 0
                }
            }
        ],
        "offset": "1784134750:3690970130418205",
        "re_version": 0,
        "total": 1539748
    }
}
```


## 翻页说明

该接口使用 **游标分页**（与关注列表的页码分页不同）：

1. **首次请求**：不传 `offset` 或传空字符串
2. **后续请求**：使用响应中的 `offset` 值作为下一次请求的 `offset` 参数
3. **判断是否有下一页**：`list` 不为空且有 `offset` 返回


## 错误码

| 状态码 | 含义                                             |
| ------ | ------------------------------------------------ |
| 0      | 请求成功                                         |
| -101   | 未登录（Cookie 无效或过期）                      |
| -403   | 风控拦截                                         |
| 53013  | **用户隐私设置未公开**（对方关闭了粉丝列表展示） |


## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/relation/fans?vmid=1447574&ps=24&web_location=333.1387' \
  -X GET \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **受隐私设置影响**：若目标用户的 `disable_show_fans` 为 `1`（关闭粉丝列表展示），接口返回 `53013`。
2. **不需要 WBI 签名**：该接口目前不需要 WBI 签名。
3. **游标分页**：使用 `offset` 翻页，而非页码。
4. **`attribute` 含义不同**：在粉丝列表中，`attribute` 表示该粉丝与你的关系，`0` = 未关注你，`2` = 已关注你？**注意**：由于是粉丝列表，`attribute=0` 是常见的（粉丝不一定也关注你）。
5. **`mtime` 含义**：表示该粉丝关注目标用户的时间戳。
6. **与关注列表的区别**：
   - 关注列表：查询用户主动关注了谁
   - 粉丝列表：查询谁关注了该用户
   - 分页方式不同：页码 vs 游标


## 相关接口

| 功能         | 接口路径                      | 说明                          |
| ------------ | ----------------------------- | ----------------------------- |
| 关注列表     | `/x/relation/followings`      | 获取用户关注的人              |
| 共同关注列表 | `/x/relation/same/followings` | 获取双方共同关注的人          |
| 特别关注列表 | `/x/relation/tag?tagid=-10`   | 获取当前用户的特别关注列表    |
| 关系统计     | `/x/relation/stat`            | 获取关注数、粉丝数            |
| 关系状态     | `/x/space/wbi/acc/relation`   | 判断是否关注、是否互粉        |
| 空间隐私设置 | `/x/space/setting`            | 包含 `disable_show_fans` 字段 |


## `disable_show_fans` 隐私说明

`/x/space/setting` 接口返回的 `privacy.disable_show_fans` 字段控制粉丝列表的可见性：

| 值   | 含义                             |
| ---- | -------------------------------- |
| `0`  | 公开（任何人都可以查看粉丝列表） |
| `1`  | 隐藏（返回 `53013`）             |
