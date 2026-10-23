# 获取我的空间信息（V2）

## 接口描述

获取当前登录用户的个人空间信息（V2版本），包含用户资料、等级经验、硬币余额、关注/粉丝数等。该接口为 `/x/space/v2/myinfo`，专门用于获取当前用户自己的空间信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间“我的信息”页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/v2/myinfo
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性 | 备注                       |
| ------------ | ---- | -------- | ------ | -------------------------- |
| web_location | str  | 来源标识 | 非必要 | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/v2/myinfo?web_location=333.1387
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

| 字段      | 类型 | 内容         | 备注     |
| --------- | ---- | ------------ | -------- |
| profile   | obj  | 用户资料信息 |          |
| level_exp | obj  | 等级经验信息 |          |
| coins     | num  | 硬币余额     | 单位：个 |
| following | num  | 关注数       |          |
| follower  | num  | 粉丝数       |          |

### `profile` 对象

| 字段             | 类型 | 内容             | 备注                     |
| ---------------- | ---- | ---------------- | ------------------------ |
| mid              | num  | 用户 UID         |                          |
| name             | str  | 用户昵称         |                          |
| sex              | str  | 性别             | `"男"`、`"女"`、`"保密"` |
| face             | str  | 头像地址         |                          |
| sign             | str  | 用户签名         |                          |
| rank             | num  | 旧版等级         |                          |
| level            | num  | 用户等级         | 1-6                      |
| jointime         | num  | 注册时间戳       | 0 表示未公开             |
| moral            | num  | 节操值           |                          |
| silence          | num  | 是否被禁言       | 0：否                    |
| email_status     | num  | 邮箱验证状态     | 1：已验证                |
| tel_status       | num  | 手机验证状态     | 1：已验证                |
| identification   | num  | 实名认证状态     | 0：未认证，1：已认证     |
| vip              | obj  | 大会员信息       |                          |
| pendant          | obj  | 挂件信息         |                          |
| nameplate        | obj  | 头像框信息       |                          |
| official         | obj  | 官方认证信息     |                          |
| birthday         | num  | 生日时间戳       |                          |
| is_tourist       | num  | 是否游客账号     |                          |
| is_fake_account  | num  | 是否虚假账号     |                          |
| is_deleted       | num  | 是否已删除       |                          |
| in_reg_audit     | num  | 是否在注册审核中 |                          |
| is_rip_user      | bool | 是否 RIP 用户    |                          |
| profession       | obj  | 职业信息         |                          |
| face_nft         | num  | 是否 NFT 头像    | 0：否                    |
| is_senior_member | num  | 是否资深会员     | 0：否                    |
| honours          | obj  | 荣誉信息         |                          |
| digital_id       | str  | 数字 ID          |                          |
| digital_type     | num  | 数字类型         | -2：无                   |
| attestation      | obj  | 认证信息         |                          |
| expert_info      | obj  | 专家信息         |                          |
| name_render      | null | 昵称渲染         | 通常为 null              |
| country_code     | str  | 国家代码         | 如 `"86"`                |
| handle           | str  | 用户 handle      |                          |

### `level_exp` 对象

| 字段          | 类型 | 内容             | 备注 |
| ------------- | ---- | ---------------- | ---- |
| current_level | num  | 当前等级         |      |
| current_min   | num  | 当前等级最低经验 |      |
| current_exp   | num  | 当前经验值       |      |
| next_exp      | num  | 下一级所需经验值 |      |
| level_up      | num  | 升级时间戳       |      |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "profile": {
            "mid": 3690995472402999,
            "name": "YunLv_L",
            "sex": "男",
            "face": "https://i0.hdslb.com/bfs/face/xxx.jpg",
            "sign": "「换位思考是一种能力，有的人就是不会」",
            "level": 3,
            "moral": 70,
            "email_status": 1,
            "tel_status": 1,
            "identification": 0,
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
                "image": "https://i2.hdslb.com/bfs/face/xxx.png"
            },
            "birthday": 1321545600,
            "country_code": "86"
        },
        "level_exp": {
            "current_level": 3,
            "current_min": 1500,
            "current_exp": 4171,
            "next_exp": 4500,
            "level_up": 1772035850
        },
        "coins": 131.5,
        "following": 69,
        "follower": 38
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
curl 'https://api.bilibili.com/x/space/v2/myinfo?web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限当前用户**：该接口只能获取当前登录用户自己的信息，不能用于查询他人。
3. **与 `acc/info` 的区别**：
   - `/x/space/wbi/acc/info`：需要 `mid` 参数，可查询他人，需要 WBI 签名
   - `/x/space/v2/myinfo`：不需要 `mid`，只能查自己，不需要 WBI 签名
4. **`identification` 字段**：0 表示未实名认证，1 表示已实名认证。
5. **`level_exp`**：提供等级经验进度，可用于判断距离下一级还需多少经验。
6. **V2 版本**：该接口为 V2 版本，比旧版 `/x/space/myinfo` 字段更完整。


## 相关接口

| 功能                   | 接口路径                  | 签名 | 适用场景               |
| ---------------------- | ------------------------- | ---- | ---------------------- |
| 获取我的空间信息（V2） | `/x/space/v2/myinfo`      | 无   | 当前用户自己的空间信息 |
| 获取用户空间信息       | `/x/space/wbi/acc/info`   | WBI  | 查询任意用户（含自己） |
| 获取导航栏信息         | `/x/web-interface/nav`    | 无   | 全局导航栏             |
| 账号安全中心信息       | `/x/safecenter/user/info` | 无   | 安全中心页面           |


### 📌 这个接口和 `bili-space-user-info-api.md` 的区别是：

- `myinfo`：V2，无签名，只查自己
- `acc/info`：WBI 签名，可查任何人
