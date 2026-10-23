# 获取用户空间主页信息

## 接口描述

获取指定用户的个人空间主页信息，包含用户基本信息、大会员状态、粉丝勋章、挂件、头像框、硬币余额、关注状态、顶部背景图等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间页面展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/space/wbi/acc/info
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名           | 类型 | 内容       | 必要性   | 备注                      |
| ---------------- | ---- | ---------- | -------- | ------------------------- |
| mid              | num  | 用户 UID   | **必要** | 目标用户的 UID            |
| token            | str  | 令牌       | 非必要   | 通常为空                  |
| platform         | str  | 平台标识   | 非必要   | `web`                     |
| web_location     | str  | 来源标识   | 非必要   | 固定传 `1550101` 或类似值 |
| dm_img_list      | str  | 风控参数   | 非必要   | 鼠标轨迹数据              |
| dm_img_str       | str  | 风控参数   | 非必要   | Base64 编码               |
| dm_cover_img_str | str  | 风控参数   | 非必要   | Base64 编码               |
| dm_img_inter     | str  | 风控参数   | 非必要   | JSON 字符串               |
| w_rid            | str  | WBI 签名   | **必要** | 见 WBI 签名算法           |
| wts              | num  | WBI 时间戳 | **必要** | 秒级 Unix 时间戳          |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/wbi/acc/info?mid=3690995472402999&token=&platform=web&web_location=1550101&w_rid=xxx&wts=xxx
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

| 字段             | 类型     | 内容                                                         | 备注                     |
| ---------------- | -------- | ------------------------------------------------------------ | ------------------------ |
| mid              | num      | 用户 UID                                                     |                          |
| name             | str      | 用户昵称                                                     |                          |
| sex              | str      | 性别                                                         | `"男"`、`"女"`、`"保密"` |
| face             | str      | 头像地址                                                     |                          |
| face_nft         | num      | 是否 NFT 头像                                                | 0：否，1：是             |
| face_nft_type    | num      | NFT 头像类型                                                 | 0：无                    |
| sign             | str      | 用户签名                                                     |                          |
| rank             | num      | 用户等级（旧版）                                             |                          |
| level            | num      | 用户等级                                                     | 1-6                      |
| jointime         | num      | 注册时间戳                                                   | 0 表示未公开             |
| moral            | num      | 节操值                                                       |                          |
| silence          | num      | 是否被禁言                                                   | 0：否                    |
| control          | num      | 是否被限制                                                   | 0：否                    |
| coins            | num      | 硬币余额                                                     | 单位：个，保留一位小数   |
| fans_badge       | bool     | 是否有粉丝勋章                                               |                          |
| fans_medal       | obj      | 粉丝勋章信息                                                 |                          |
| official         | obj      | 官方认证信息                                                 |                          |
| vip              | obj      | 大会员信息                                                   |                          |
| pendant          | obj      | 挂件信息                                                     |                          |
| nameplate        | obj      | **成就勋章信息**（个人空间展示的勋章，包含名称、图标、等级、获取条件） |                          |
| user_honour_info | obj      | 荣誉信息                                                     |                          |
| is_followed      | bool     | 当前用户是否关注了目标用户                                   |                          |
| top_photo        | str      | 顶部背景图地址                                               | 旧版字段                 |
| top_photo_v2     | obj      | 顶部背景图 V2                                                | 包含多尺寸               |
| birthday         | str      | 生日                                                         | 格式 `"MM-DD"`           |
| school           | obj      | 学校信息                                                     |                          |
| profession       | obj      | 职业信息                                                     |                          |
| live_room        | null/obj | 直播间信息                                                   | 未开播时为 null          |
| is_senior_member | num      | 是否资深会员                                                 | 0：否                    |
| is_risk          | bool     | 是否风控                                                     |                          |
| elec             | obj      | 充电信息                                                     |                          |
| contract         | obj      | 契约计划信息                                                 |                          |
| attestation      | obj      | 认证信息                                                     |                          |

### `vip` 对象

| 字段             | 类型 | 内容           | 备注                              |
| ---------------- | ---- | -------------- | --------------------------------- |
| type             | num  | 大会员类型     | 0：无，1：大会员，2：超级大会员？ |
| status           | num  | 大会员状态     | 1：有效，0：无效                  |
| due_date         | num  | 到期时间戳     | 毫秒级                            |
| vip_pay_type     | num  | 支付类型       | 1：月度，2：年度？                |
| label            | obj  | 大会员标签     |                                   |
| avatar_subscript | num  | 头像角标       |                                   |
| nickname_color   | str  | 昵称颜色       | 如 `"#FB7299"`                    |
| tv_vip_status    | num  | 超级大会员状态 |                                   |
| super_vip        | obj  | 超级大会员信息 |                                   |

### `fans_medal` 对象

| 字段   | 类型 | 内容         | 备注                                                        |
| ------ | ---- | ------------ | ----------------------------------------------------------- |
| show   | bool | 是否展示     |                                                             |
| wear   | bool | 是否佩戴     |                                                             |
| medal  | obj  | 勋章简略信息 | 包含 `level`、`medal_name`、`medal_color` 等                |
| detail | obj  | 勋章详细信息 | 包含 `medal_id`、`medal_color_level`、`medal_color_name` 等 |

### `pendant` 对象

| 字段   | 类型 | 内容         | 备注       |
| ------ | ---- | ------------ | ---------- |
| pid    | num  | 挂件 ID      |            |
| name   | str  | 挂件名称     |            |
| image  | str  | 挂件图片地址 |            |
| expire | num  | 过期时间戳   | 0 表示永久 |

### `nameplate` 对象

| 字段        | 类型 | 内容           | 备注 |
| ----------- | ---- | -------------- | ---- |
| nid         | num  | 头像框 ID      |      |
| name        | str  | 头像框名称     |      |
| image       | str  | 头像框图片地址 |      |
| image_small | str  | 头像框小图地址 |      |
| level       | str  | 等级描述       |      |
| condition   | str  | 获取条件       |      |

### `official` 对象

| 字段  | 类型 | 内容     | 备注                             |
| ----- | ---- | -------- | -------------------------------- |
| role  | num  | 认证角色 |                                  |
| title | str  | 认证标题 |                                  |
| desc  | str  | 认证描述 |                                  |
| type  | num  | 认证类型 | -1：无，0：个人认证，1：机构认证 |

### `top_photo_v2` 对象

| 字段       | 类型 | 内容           | 备注 |
| ---------- | ---- | -------------- | ---- |
| sid        | num  | 背景图 ID      |      |
| l_img      | str  | 大尺寸背景图   |      |
| l_200h_img | str  | 200px 高背景图 |      |

### `elec` 对象

| 字段      | 类型 | 内容         | 备注                             |
| --------- | ---- | ------------ | -------------------------------- |
| show_info | obj  | 充电展示信息 | 包含 `show`、`state`、`total` 等 |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "mid": 3690995472402999,
        "name": "YunLv_L",
        "sex": "男",
        "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
        "sign": "「换位思考是一种能力，有的人就是不会」",
        "level": 3,
        "coins": 131.5,
        "fans_medal": {
            "show": true,
            "wear": true,
            "medal": {
                "level": 16,
                "medal_name": "洛府"
            },
            "detail": {
                "medal_id": 6375,
                "medal_name": "洛府"
            }
        },
        "vip": {
            "type": 1,
            "status": 1,
            "due_date": 1786032000000,
            "nickname_color": "#FB7299"
        },
        "pendant": {
            "pid": 293,
            "name": "凹凸世界",
            "image": "https://i0.hdslb.com/bfs/face/xxx.png"
        },
        "nameplate": {
            "nid": 92,
            "name": "有爱大佬",
            "image": "https://i0.hdslb.com/bfs/face/xxx.png"
        },
        "is_followed": false,
        "top_photo_v2": {
            "l_img": "https://i1.hdslb.com/bfs/space/xxx.png"
        },
        "birthday": "11-18"
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
| -403   | 请求被风控拦截              |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/space/wbi/acc/info?mid=3690995472402999&token=&platform=web&web_location=1550101&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **风控参数**：`dm_img_list`、`dm_img_str`、`dm_cover_img_str`、`dm_img_inter` 为设备指纹/行为采集参数，用于反爬风控，缺失可能导致 `-403`。
3. **`coins` 字段**：返回当前用户的硬币余额（查询他人时可能不返回）。
4. **`is_followed`**：当前登录用户是否关注了目标用户（未登录时为 `false`）。
5. **原项目已有旧版接口**：原项目 `docs/user/info.md` 中的 `/x/space/acc/info` 已废弃，建议使用本接口（`/x/space/wbi/acc/info`）。
6. **与原项目旧版的区别**：
   - 新增 `fans_medal.detail` 详细字段
   - 新增 `pendant` 挂件信息
   - 新增 `nameplate` 头像框信息
   - 新增 `top_photo_v2` 多尺寸背景图
   - 新增 `coins` 硬币余额
   - 使用 WBI 签名鉴权


## 相关接口

| 功能             | 接口路径                       | 签名 |
| ---------------- | ------------------------------ | ---- |
| 用户空间主页信息 | `/x/space/wbi/acc/info`        | WBI  |
| 用户投稿列表     | `/x/space/wbi/arc/search`      | WBI  |
| 用户追番列表     | `/x/space/bangumi/follow/list` | WBI  |
| 用户置顶视频     | `/x/space/top/arc`             | 无   |
