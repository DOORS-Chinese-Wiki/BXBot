# 关注列表

## 接口描述

获取指定用户的关注列表（该用户关注的 UP 主列表）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间关注列表页面展示。受对方隐私设置影响，若对方关闭关注列表展示，将返回 `53013`。


## 接口地址

```
GET https://api.bilibili.com/x/relation/followings
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要


## 请求参数（URL Query）

| 参数名         | 类型 | 内容         | 必要性   | 备注                                  |
| -------------- | ---- | ------------ | -------- | ------------------------------------- |
| `vmid`         | num  | 目标用户 UID | **必要** | 要查询关注列表的用户                  |
| `pn`           | num  | 页码         | 非必要   | 默认 1                                |
| `ps`           | num  | 每页数量     | 非必要   | 默认 20，最大 50；**网页版固定为 24** |
| `order`        | str  | 排序方向     | 非必要   | `desc`：倒序（默认），`asc`：正序     |
| `order_type`   | str  | 排序类型     | 非必要   | 见下方枚举值                          |
| `gaia_source`  | str  | 来源标识     | 非必要   | 如 `main_web`                         |
| `web_location` | str  | 来源标识     | 非必要   | 固定传 `333.1387`                     |

### `order_type` 枚举值

| 值          | 含义         | 说明                                                         |
| ----------- | ------------ | ------------------------------------------------------------ |
| （空）      | 默认排序     | 按关注时间倒序（`mtime` 降序），与 `order=desc` 配合         |
| `attention` | **最常访问** | 按用户访问频率排序，经常访问的 UP 主排在前面。**网页版「最常访问」Tab 使用的排序** |
| `pubtime`   | 按发布时间   | 按 UP 主最近发布时间排序                                     |


## 响应结构

### 根对象

| 字段      | 类型 | 内容     | 备注       |
| --------- | ---- | -------- | ---------- |
| `code`    | num  | 状态码   | 0 表示成功 |
| `message` | str  | 状态信息 | `"0"`      |
| `ttl`     | num  | 缓存时间 | 1          |
| `data`    | obj  | 数据本体 |            |

### `data` 对象

| 字段         | 类型  | 内容     | 备注                     |
| ------------ | ----- | -------- | ------------------------ |
| `list`       | array | 关注列表 | 每个元素为一个 UP 主信息 |
| `total`      | num   | 关注总数 |                          |
| `re_version` | num   | 版本标识 | 通常为 `0`               |

### `list` 数组元素

| 字段              | 类型  | 内容               | 备注                                    |
| ----------------- | ----- | ------------------ | --------------------------------------- |
| `mid`             | num   | UP 主 UID          |                                         |
| `attribute`       | num   | 关系属性           | `2`：已关注，`6`：互相关注              |
| `mtime`           | num   | 关注时间戳         | Unix 时间戳（秒）                       |
| `tag`             | array | 分组标签 ID 列表   | `-10` 表示特别关注；正数为自定义分组 ID |
| `special`         | num   | **是否特别关注**   | `0`：普通关注，`1`：特别关注            |
| `contract_info`   | obj   | 契约计划信息       | `{}` 或 `{"is_contract": true}`         |
| `uname`           | str   | UP 主昵称          |                                         |
| `face`            | str   | 头像 URL           |                                         |
| `sign`            | str   | 个人简介           |                                         |
| `face_nft`        | num   | 是否为 NFT 头像    | `0`：否                                 |
| `handle`          | str   | 用户 handle        | 通常为空                                |
| `official_verify` | obj   | 官方认证信息       |                                         |
| `vip`             | obj   | 大会员信息         |                                         |
| `name_render`     | obj   | 昵称渲染信息       | 通常为空对象                            |
| `nft_icon`        | str   | NFT 图标           | 通常为空                                |
| `rec_reason`      | str   | 推荐理由           | 通常为空                                |
| `track_id`        | str   | 追踪 ID            | 通常为空                                |
| `follow_time`     | str   | 关注时间（字符串） | 通常为空                                |

### `official_verify` 对象

| 字段   | 类型 | 内容     | 备注                                        |
| ------ | ---- | -------- | ------------------------------------------- |
| `type` | num  | 认证类型 | `-1`：无认证，`0`：UP 主认证，`1`：机构认证 |
| `desc` | str  | 认证描述 |                                             |

### `vip` 对象

| 字段               | 类型 | 内容       | 备注                                      |
| ------------------ | ---- | ---------- | ----------------------------------------- |
| `vipType`          | num  | 大会员类型 | `0`：无，`1`：月度大会员，`2`：年度大会员 |
| `vipDueDate`       | num  | 到期时间戳 | 毫秒                                      |
| `vipStatus`        | num  | 状态       | `0`：未激活/已过期，`1`：生效中           |
| `label`            | obj  | 标签信息   |                                           |
| `avatar_subscript` | num  | 头像角标   | `0`：无，`1`：有                          |
| `nickname_color`   | str  | 昵称颜色   | 大会员粉色 `#FB7299`                      |

### `contract_info` 对象

| 字段          | 类型 | 内容             | 备注                                                 |
| ------------- | ---- | ---------------- | ---------------------------------------------------- |
| `is_contract` | bool | 是否参与契约计划 | `true`：已参与（如老粉计划），`false`/不存在：未参与 |

> **说明**：`contract_info` 在网页端不直接展示，在 APP 端个人主页会显示相关标识（如“老粉计划”标签）。


## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": [
            {
                "mid": 1447574,
                "attribute": 2,
                "mtime": 1771576432,
                "tag": [-10, 353738545],
                "special": 1,
                "contract_info": {},
                "uname": "洛少爷",
                "face": "https://i2.hdslb.com/bfs/face/xxx.jpg",
                "sign": "原创音乐人，全平台ID：洛少爷",
                "official_verify": {
                    "type": 0,
                    "desc": "bilibili 知名音乐UP主"
                },
                "vip": {
                    "vipType": 2,
                    "vipDueDate": 1799424000000,
                    "vipStatus": 1,
                    "nickname_color": "#FB7299"
                }
            },
            {
                "mid": 3706925810191128,
                "attribute": 2,
                "mtime": 1773665876,
                "tag": [353739665, -10],
                "special": 1,
                "contract_info": {
                    "is_contract": true
                },
                "uname": "西西西酱_",
                "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
                "sign": "养成系吃播 现在关注以后就是老粉啦",
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
        "re_version": 0,
        "total": 74
    }
}
```


## 错误码

| 状态码 | 含义                                             |
| ------ | ------------------------------------------------ |
| 0      | 请求成功                                         |
| -101   | 未登录（Cookie 无效或过期）                      |
| -403   | 风控拦截                                         |
| 53013  | **用户隐私设置未公开**（对方关闭了关注列表展示） |


## 调用示例（curl）

### 默认排序（关注时间倒序）

```bash
curl 'https://api.bilibili.com/x/relation/followings?vmid=3690995472402999&pn=1&ps=24&order=desc&web_location=333.1387' \
  -X GET \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

### 最常访问排序

```bash
curl 'https://api.bilibili.com/x/relation/followings?vmid=3690995472402999&pn=1&ps=24&order=desc&order_type=attention&web_location=333.1387' \
  -X GET \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```


## 注意事项

1. **受隐私设置影响**：若目标用户的 `disable_following` 为 `1`（关闭关注列表展示），接口返回 `53013`。
2. **获取自身的关注列表无限制**：可翻页获取全部关注。
3. **获取他人的关注列表仅返回前 100 条**：即使分页也无法突破，这是服务端限制。
4. **网页版 `ps=24` 固定**：Web 端每页固定 24 条，无法通过参数修改。
5. **不需要 WBI 签名**：该接口不需要 WBI 签名。
6. **`attribute` 字段**：`2` 表示单向关注，`6` 表示互相关注。
7. **`tag` 与 `special` 的关系**：`tag` 数组包含 `-10` 时，`special` 为 `1`（特别关注）。建议以 `special` 字段为准。
8. **`special` 跨页统计**：`special` 字段只在当前页返回的数据中有效。要统计全部特别关注数量，需遍历所有页面或使用 `/x/relation/tag?tagid=-10` 接口。
9. **`contract_info.is_contract`**：`true` 表示该用户与你存在契约计划关系（如老粉计划），APP 端个人主页会显示对应标识。
10. **`order_type=attention`**：按最常访问排序，是网页版「最常访问」Tab 使用的排序方式。
11. **与共同关注的区别**：
    - `/followings`：返回当前用户关注的人（受隐私限制，查看他人仅 100 条）
    - `/same/followings`：返回双方共同关注的人（不受隐私限制，不受 100 条限制）


## 相关接口

| 功能         | 接口路径                      | 说明                                               |
| ------------ | ----------------------------- | -------------------------------------------------- |
| 粉丝列表     | `/x/relation/fans`            | 获取用户的粉丝列表                                 |
| 共同关注列表 | `/x/relation/same/followings` | 获取双方共同关注的 UP 主                           |
| 特别关注列表 | `/x/relation/tag?tagid=-10`   | 获取当前用户的特别关注列表（不分页，一次返回全部） |
| 关系统计     | `/x/relation/stat`            | 获取关注数、粉丝数                                 |
| 关系状态     | `/x/space/wbi/acc/relation`   | 判断是否关注、是否互粉                             |
| 空间隐私设置 | `/x/space/setting`            | 包含 `disable_following` 字段                      |


## `disable_following` 隐私说明

`/x/space/setting` 接口返回的 `privacy.disable_following` 字段控制关注列表的可见性：

| 值   | 含义                             |
| ---- | -------------------------------- |
| `0`  | 公开（任何人都可以查看关注列表） |
| `1`  | 隐藏（返回 `53013`）             |
