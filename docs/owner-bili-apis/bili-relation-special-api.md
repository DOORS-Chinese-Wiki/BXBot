# 特别关注列表

## 接口描述

获取当前登录用户的特别关注分组（`tagid=-10`）中的用户列表，包含用户基本信息、关注状态等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于展示特别关注分组下的关注用户。

---

## 接口地址

```
GET https://api.bilibili.com/x/relation/tag
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注                 |
| ------------ | ---- | -------- | -------- | -------------------- |
| tagid        | num  | 分组 ID  | **必要** | 特别关注固定为 `-10` |
| mid          | num  | 用户 UID | **必要** | 当前登录用户的 UID   |
| pn           | num  | 页码     | 非必要   | 默认 1               |
| ps           | num  | 每页数量 | 非必要   | 默认 20，最大 50     |
| web_location | str  | 来源标识 | 非必要   | 固定传 `0.0`         |

**示例请求 URL：**

```
https://api.bilibili.com/x/relation/tag?tagid=-10&pn=1&ps=24&mid=3690995472402999&web_location=0.0
```

---

## 响应结构

### 根对象

| 字段    | 类型  | 内容     | 备注                   |
| ------- | ----- | -------- | ---------------------- |
| code    | num   | 状态码   | 0 表示成功             |
| message | str   | 状态信息 | `"0"`                  |
| ttl     | num   | 1        |                        |
| data    | array | 用户列表 | 每个元素为一个用户对象 |

### `data` 数组元素

| 字段            | 类型       | 内容          | 备注                          |
| --------------- | ---------- | ------------- | ----------------------------- |
| mid             | num        | 用户 UID      |                               |
| uname           | str        | 用户昵称      |                               |
| face            | str        | 头像地址      |                               |
| sign            | str        | 用户签名      |                               |
| face_nft        | num        | 是否 NFT 头像 | 0：否                         |
| handle          | str        | 用户 handle   |                               |
| attribute       | num        | 关系属性      | 0：未关注，2：已关注，6：互粉 |
| tag             | null/array | 分组标签      | 通常为 null                   |
| special         | num        | 特别关注标识  | 0：否                         |
| contract_info   | obj        | 契约计划信息  |                               |
| official_verify | obj        | 官方认证信息  |                               |
| vip             | obj        | 大会员信息    |                               |
| name_render     | obj        | 昵称渲染信息  |                               |
| live            | obj        | 直播状态信息  |                               |
| nft_icon        | str        | NFT 图标      |                               |
| rec_reason      | str        | 推荐理由      |                               |
| track_id        | str        | 追踪 ID       |                               |
| follow_time     | str        | 关注时间      |                               |

### `official_verify` 对象

| 字段 | 类型 | 内容     | 备注                             |
| ---- | ---- | -------- | -------------------------------- |
| type | num  | 认证类型 | -1：无，0：个人认证，1：机构认证 |
| desc | str  | 认证描述 |                                  |

### `vip` 对象

| 字段                 | 类型 | 内容         | 备注                                |
| -------------------- | ---- | ------------ | ----------------------------------- |
| vipType              | num  | 会员类型     | 0：无，1：月度大会员，2：年度大会员 |
| vipDueDate           | num  | 到期时间戳   | 毫秒级                              |
| dueRemark            | str  | 到期备注     |                                     |
| accessStatus         | num  | 访问状态     |                                     |
| vipStatus            | num  | 大会员状态   | 0：无效，1：有效                    |
| vipStatusWarn        | str  | 状态警告     |                                     |
| themeType            | num  | 主题类型     |                                     |
| label                | obj  | 标签信息     |                                     |
| avatar_subscript     | num  | 头像角标     |                                     |
| nickname_color       | str  | 昵称颜色     |                                     |
| avatar_subscript_url | str  | 头像角标地址 |                                     |

### `live` 对象

| 字段        | 类型 | 内容           | 备注                 |
| ----------- | ---- | -------------- | -------------------- |
| live_status | num  | 直播状态       | 0：未直播，1：直播中 |
| jump_url    | str  | 直播间跳转链接 |                      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": [
        {
            "mid": 3707015195003287,
            "uname": "YunLv-L",
            "face": "https://i1.hdslb.com/bfs/face/xxx.jpg",
            "sign": "",
            "official_verify": {
                "type": -1,
                "desc": ""
            },
            "vip": {
                "vipType": 1,
                "vipDueDate": 1785168000000,
                "vipStatus": 1,
                "nickname_color": "#FB7299"
            },
            "live": {
                "live_status": 0,
                "jump_url": ""
            }
        },
        {
            "mid": 1447574,
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
        }
    ]
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
curl 'https://api.bilibili.com/x/relation/tag?tagid=-10&pn=1&ps=24&mid=3690995472402999&web_location=0.0' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`tagid=-10`**：固定值，表示特别关注分组。
3. **`mid` 参数**：必须为当前登录用户的 UID，否则无法获取正确数据。
4. **分页**：`ps` 最大可能为 50，建议使用 20 或 24。
5. **返回数据与关注列表类似**：该接口返回的用户对象结构与 `/x/relation/followings` 一致。
6. **特别关注分组 ID**：`-10` 为系统保留值，用于标识特别关注。
