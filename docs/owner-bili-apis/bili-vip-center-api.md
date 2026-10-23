# 大会员中心 API

## 接口列表

### 1. 大会员中心信息
### 2. 大会员签到
### 3. 大会员权益列表

---

# 1. 大会员中心信息

## 接口描述

获取当前登录用户的大会员中心综合信息，包含用户账户信息、大会员状态、积分余额、福利活动、榜单入口等。

> 该接口是大会员中心首页的聚合接口，一次性返回大会员模块所需的大部分展示数据。

---

## 接口地址

```
GET https://api.bilibili.com/x/vip/web/vip_center/info
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名    | 类型 | 内容       | 必要性             | 备注                                |
| --------- | ---- | ---------- | ------------------ | ----------------------------------- |
| module_id | num  | 模块 ID    | 必要               | 固定传 `700001`，标识大会员中心模块 |
| platform  | str  | 平台标识   | 非必要             | 固定传 `pc`                         |
| buvid     | str  | 设备标识   | 非必要（风控要求） | 从 Cookie 中取 `buvid3` 的值        |
| build     | num  | 构建版本号 | 非必要             | 固定传 `0`                          |

**示例请求 URL：**

```
https://api.bilibili.com/x/vip/web/vip_center/info?module_id=700001&platform=pc&buvid=xxx&build=0
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

| 字段             | 类型  | 内容                     | 备注     |
| ---------------- | ----- | ------------------------ | -------- |
| top_banner       | obj   | 顶部横幅信息             |          |
| user             | obj   | 用户信息（含大会员状态） | **核心** |
| welfare_activity | obj   | 福利活动信息             |          |
| taps             | array | 榜单 Tab 列表            |          |
| face             | obj   | 头像组件信息             |          |

---

### `top_banner` 对象

| 字段    | 类型  | 内容     | 备注         |
| ------- | ----- | -------- | ------------ |
| banners | array | 横幅列表 | 多个横幅轮播 |

#### `banners` 数组元素

| 字段          | 类型 | 内容          | 备注             |
| ------------- | ---- | ------------- | ---------------- |
| cover         | str  | 封面图地址    | 大图             |
| small_cover   | str  | 小封面图地址  | 小图             |
| title         | str  | 标题          |                  |
| logo          | str  | Logo 图片地址 |                  |
| link          | str  | 跳转链接      |                  |
| season_status | num  | 剧集状态      |                  |
| season_id     | num  | 剧集 ID       |                  |
| play_title    | str  | 播放标题      |                  |
| user_status   | num  | 用户状态      |                  |
| season_type   | num  | 剧集类型      |                  |
| source        | str  | 来源          | `"ads"` 表示广告 |
| track_params  | obj  | 埋点参数      |                  |

---

### `user` 对象（核心）

| 字段                | 类型 | 内容                     | 备注         |
| ------------------- | ---- | ------------------------ | ------------ |
| account             | obj  | 账户基本信息             |              |
| vip_info            | obj  | 大会员详细信息           | **最重要**   |
| tv_vip_info         | obj  | 超级大会员信息           | 含电视端权益 |
| overdue_explain     | obj  | 过期提示文案             |              |
| wallet              | obj  | 钱包信息（积分、卡券等） |              |
| open_entrance       | obj  | 入口按钮文案             |              |
| vip_surplus_seconds | num  | 大会员剩余秒数           |              |
| tv_surplus_seconds  | num  | 超级大会员剩余秒数       |              |
| is_auto_renew       | bool | 是否自动续费             |              |
| is_tv_auto_renew    | bool | 超级大会员是否自动续费   |              |
| vip_keep_time       | num  | 大会员保留时间           |              |
| is_sign_surplus     | bool | 是否签到盈余             |              |
| notice              | obj  | 通知信息                 |              |

#### `user.account` 对象

| 字段             | 类型 | 内容             | 备注        |
| ---------------- | ---- | ---------------- | ----------- |
| mid              | num  | 用户 UID         |             |
| name             | str  | 用户昵称         |             |
| sex              | str  | 性别             |             |
| face             | str  | 头像地址         |             |
| sign             | str  | 签名             |             |
| rank             | num  | 等级             |             |
| birthday         | num  | 生日时间戳       |             |
| is_fake_account  | num  | 是否虚假账号     |             |
| is_deleted       | num  | 是否已删除       |             |
| in_reg_audit     | num  | 是否在注册审核中 |             |
| is_senior_member | num  | 是否资深会员     |             |
| name_render      | null | 昵称渲染         | 通常为 null |
| handle           | str  | 用户 handle      |             |

#### `user.vip_info` 对象（核心）

| 字段                    | 类型 | 内容             | 备注                            |
| ----------------------- | ---- | ---------------- | ------------------------------- |
| mid                     | num  | 用户 UID         |                                 |
| name                    | str  | 用户昵称         |                                 |
| vip_type                | num  | 大会员类型       | 0：无，1：大会员，2：超级大会员 |
| vip_status              | num  | 大会员状态       | 1：有效，0：无效                |
| vip_due_date            | num  | 大会员到期时间戳 | 毫秒级                          |
| vip_pay_type            | num  | 支付类型         | 1：月付，2：年付？              |
| theme_type              | num  | 主题类型         |                                 |
| label                   | obj  | 大会员标签信息   |                                 |
| avatar_subscript        | num  | 头像角标标识     |                                 |
| avatar_subscript_url    | str  | 头像角标图片地址 |                                 |
| nickname_color          | str  | 昵称颜色         | 如 `"#FB7299"`                  |
| is_new_user             | bool | 是否新用户       |                                 |
| tip_material            | obj  | 提示素材         |                                 |
| vip_is_annual           | bool | 是否年度大会员   |                                 |
| vip_is_month            | bool | 是否月度大会员   |                                 |
| is_auto_renew           | bool | 是否自动续费     |                                 |
| vip_is_valid            | bool | 大会员是否有效   |                                 |
| vip_is_overdue          | bool | 大会员是否已过期 |                                 |
| vip_keep_time           | num  | 大会员保留时间   |                                 |
| vip_expire_days         | num  | 距离过期天数     | 如 `27` 表示还有 27 天到期      |
| is_tv_vip               | bool | 是否超级大会员   |                                 |
| tv_vip_status           | num  | 超级大会员状态   |                                 |
| vip_membership_is_vip   | bool | 是否会员购大会员 |                                 |
| super_membership_is_vip | bool | 是否超级大会员   |                                 |

##### `vip_info.label` 对象

| 字段                      | 类型 | 内容                 | 备注          |
| ------------------------- | ---- | -------------------- | ------------- |
| text                      | str  | 标签文字             | 如 `"大会员"` |
| label_theme               | str  | 标签主题             | `"vip"`       |
| text_color                | str  | 文字颜色             |               |
| bg_style                  | num  | 背景样式             |               |
| bg_color                  | str  | 背景颜色             |               |
| border_color              | str  | 边框颜色             |               |
| use_img_label             | bool | 是否使用图片标签     |               |
| img_label_uri_hans        | str  | 简体图片标签地址     |               |
| img_label_uri_hant        | str  | 繁体图片标签地址     |               |
| img_label_uri_hans_static | str  | 简体静态图片标签地址 |               |
| img_label_uri_hant_static | str  | 繁体静态图片标签地址 |               |
| label_id                  | num  | 标签 ID              |               |
| label_goto                | obj  | 跳转链接             | 移动端/PC     |
| img_label_uri_i18n        | str  | 国际化图片标签       |               |
| img_label_uri_i18n_static | str  | 国际化静态图片标签   |               |
| label_type                | num  | 标签类型             |               |

#### `user.wallet` 对象

| 字段         | 类型 | 内容         | 备注         |
| ------------ | ---- | ------------ | ------------ |
| big_point    | obj  | 大会员积分   | **核心字段** |
| card_package | obj  | 卡券包       |              |
| buy_record   | obj  | 购买记录     |              |
| auto_renew   | obj  | 自动续费记录 |              |

##### `wallet.big_point` 对象

| 字段  | 类型 | 内容               | 备注     |
| ----- | ---- | ------------------ | -------- |
| count | num  | 当前积分余额       | 如 `933` |
| link  | str  | 积分详情页跳转链接 |          |

##### `wallet.card_package` / `buy_record` / `auto_renew` 对象

| 字段  | 类型 | 内容     | 备注 |
| ----- | ---- | -------- | ---- |
| count | num  | 数量     |      |
| link  | str  | 跳转链接 |      |

#### `user.open_entrance` 对象

| 字段            | 类型 | 内容             | 备注 |
| --------------- | ---- | ---------------- | ---- |
| vip_button_tip  | str  | VIP 按钮提示文案 |      |
| corner_marker   | str  | 角标文案         |      |
| gift_button_tip | str  | 赠送按钮文案     |      |

#### `user.notice` 对象

| 字段           | 类型 | 内容       | 备注 |
| -------------- | ---- | ---------- | ---- |
| reason_text    | str  | 原因文案   |      |
| notice_text    | str  | 通知文案   |      |
| tv_text        | str  | 电视端文案 |      |
| type           | num  | 通知类型   |      |
| can_close      | bool | 是否可关闭 |      |
| new_user_title | str  | 新用户标题 |      |

---

### `welfare_activity` 对象

| 字段     | 类型  | 内容         | 备注 |
| -------- | ----- | ------------ | ---- |
| welfares | array | 福利活动列表 |      |

#### `welfares` 数组元素

| 字段  | 类型 | 内容         | 备注 |
| ----- | ---- | ------------ | ---- |
| index | num  | 排序索引     |      |
| img   | str  | 活动图片地址 |      |
| link  | str  | 活动跳转链接 |      |

---

### `taps` 数组元素

| 字段       | 类型 | 内容                    | 备注                                                |
| ---------- | ---- | ----------------------- | --------------------------------------------------- |
| oid        | str  | 配置参数（JSON 字符串） | 如 `"{season_type:0,style_id:0,day:3,rank_type:5}"` |
| rank_id    | num  | 榜单 ID                 |                                                     |
| rank_title | str  | 榜单标题                | 如 `"会员"`、`"番剧"`、`"电影"`                     |
| type       | num  | 类型                    | 部分条目可能没有此字段                              |

---

### `face` 对象

| 字段            | 类型 | 内容               | 备注         |
| --------------- | ---- | ------------------ | ------------ |
| container_size  | obj  | 容器尺寸           |              |
| fallback_layers | obj  | 头像图层配置       | 用于前端渲染 |
| mid             | str  | 用户 UID（字符串） |              |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "top_banner": {
            "banners": [
                {
                    "cover": "http://i0.hdslb.com/bfs/vip/xxx.png",
                    "small_cover": "http://i0.hdslb.com/bfs/vip/xxx.png",
                    "title": "联合会员买一送一",
                    "link": "https://www.bilibili.com/blackboard/xxx.html"
                }
            ]
        },
        "user": {
            "account": {
                "mid": 123456789,
                "name": "示例用户",
                "face": "https://i0.hdslb.com/bfs/face/xxx.jpg"
            },
            "vip_info": {
                "vip_type": 1,
                "vip_status": 1,
                "vip_due_date": 1786032000000,
                "vip_expire_days": 27,
                "vip_is_valid": true,
                "vip_is_overdue": false,
                "is_auto_renew": true
            },
            "wallet": {
                "big_point": {
                    "count": 933,
                    "link": "https://big.bilibili.com/mobile/bigPoint?navhide=1&closable=1"
                }
            }
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
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/vip/web/vip_center/info?module_id=700001&platform=pc&buvid=xxx&build=0' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **聚合接口**：该接口一次性返回大会员中心的大部分数据，包含账户信息、会员状态、积分、福利活动、榜单入口等。
2. **`module_id=700001`**：固定值，表示大会员中心模块，不可更改。
3. **`vip_status` 含义**：
   - `1`：大会员有效
   - `0`：无效/已过期
4. **`vip_type` 含义**：
   - `0`：非大会员
   - `1`：大会员
   - `2`：超级大会员（含电视端权益）
5. **`vip_pay_type` 含义**：
   - `1`：月度支付
   - `2`：年度支付（待验证）
6. **积分余额**：位于 `user.wallet.big_point.count`。
7. **距离过期天数**：`vip_expire_days` 字段直接返回剩余天数，无需自行计算。
8. **自动续费**：`is_auto_renew` 为 `true` 表示已开启自动续费。
9. **`face` 对象**：为头像组件的前端渲染配置，普通调用者可忽略。
10. **`tv_vip_info` 字段**：即超级大会员（含电视端权益）信息，当 `type=0`、`status=0` 时表示未开通。


# 2. 大会员签到

## 接口描述

执行大会员每日签到操作，签到可获得会员积分等奖励。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于大会员每日签到打卡。

---

## 接口地址

```
POST https://api.bilibili.com/x/vip/experience/add
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`（实际请求体为空，参数在 URL 中）

---

## 请求参数（URL Query）

| 参数名 | 类型 | 内容       | 必要性           | 备注                           |
| ------ | ---- | ---------- | ---------------- | ------------------------------ |
| mid    | num  | 用户 UID   | 必要             | 当前登录用户的 UID             |
| buvid  | str  | 设备标识   | 必要（风控要求） | 从 Cookie 中取 `buvid3` 的值   |
| csrf   | str  | CSRF Token | 必要             | 位于 Cookie 中的 `bili_jct` 值 |

> **注意**：该接口虽然是 POST 方法，但**请求体为空**，所有参数均通过 URL Query 传递。

**示例请求 URL：**

```
https://api.bilibili.com/x/vip/experience/add?mid=123456789&buvid=xxx&csrf=xxx
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

| 字段     | 类型 | 内容                   | 备注                                        |
| -------- | ---- | ---------------------- | ------------------------------------------- |
| type     | num  | 签到类型               | 0：普通签到？                               |
| is_grant | bool | 是否成功签到并获得奖励 | `true`：签到成功，`false`：签到失败或已签到 |

**响应示例（签到成功）：**

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "type": 0,
        "is_grant": true
    }
}
```

**响应示例（已签到）：**

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "type": 0,
        "is_grant": false
    }
}
```

---

## 错误码

| 状态码 | 含义                                        |
| ------ | ------------------------------------------- |
| 0      | 请求成功（`is_grant` 指示是否实际签到成功） |
| -101   | 未登录（Cookie 无效或过期）                 |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期）    |
| 其他   | 参见 `message` 字段                         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/vip/experience/add?mid=123456789&buvid=xxx&csrf=xxx' \
  -X POST \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx'
```

---

## 注意事项

1. **请求体为空**：该接口虽然是 POST，但所有参数都在 URL 中，`Content-Length: 0`。
2. **`is_grant` 判断签到结果**：
   - `true`：签到成功，已获得积分奖励
   - `false`：签到失败，可能原因包括：今日已签到、非大会员用户、账号异常等
3. **`code=0` 不等于签到成功**：需要同时检查 `data.is_grant` 是否为 `true`。
4. **认证**：必须携带有效的 `SESSDATA` 和 `bili_jct` Cookie。


# 3. 大会员权益列表

## 接口描述

获取当前登录用户的大会员权益列表，包含各项权益的领取状态、剩余时间等信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于大会员中心展示可领取/已领取的权益。

---

## 接口地址

```
GET https://api.bilibili.com/x/vip/privilege/my
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名   | 类型 | 内容     | 必要性             | 备注                         |
| -------- | ---- | -------- | ------------------ | ---------------------------- |
| mid      | num  | 用户 UID | 必要               | 当前登录用户的 UID           |
| platform | str  | 平台标识 | 非必要             | 固定传 `Windows`             |
| buvid    | str  | 设备标识 | 非必要（风控要求） | 从 Cookie 中取 `buvid3` 的值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/vip/privilege/my?mid=123456789&platform=Windows&buvid=xxx
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

| 字段              | 类型  | 内容               | 备注                            |
| ----------------- | ----- | ------------------ | ------------------------------- |
| list              | array | 权益列表           | 每个元素为一项权益              |
| is_short_vip      | bool  | 是否短期大会员     |                                 |
| is_freight_open   | bool  | 是否开启免邮       |                                 |
| level             | num   | 会员等级           |                                 |
| cur_exp           | num   | 当前经验值         |                                 |
| next_exp          | num   | 下一级所需经验值   |                                 |
| is_vip            | bool  | 是否大会员         |                                 |
| is_senior_member  | num   | 是否资深会员       |                                 |
| format060102      | num   | 格式化的日期       | 如 `260626` 可能表示 2026-06-26 |
| is_overdue_vip    | bool  | 大会员是否已过期   |                                 |
| vip_status        | num   | 大会员状态         | 1：有效                         |
| vip_type          | num   | 大会员类型         | 1：大会员                       |
| keeptime_end      | num   | 权益保留结束时间戳 |                                 |
| vip_due_date      | num   | 大会员到期时间戳   |                                 |
| vip_is_annual     | bool  | 是否年度大会员     |                                 |
| vip_is_month      | bool  | 是否月度大会员     |                                 |
| vip_is_new_user   | bool  | 是否新用户         |                                 |
| bind_phone        | str   | 绑定手机号（脱敏） | 如 `"180****4235"`              |
| taobao_account    | null  | 淘宝账号绑定       | 通常为 null                     |
| is_tv_vip         | bool  | 是否超级大会员     |                                 |
| keeptime_start    | num   | 权益保留开始时间戳 |                                 |
| comic_show_coupon | obj   | 漫展优惠券汇总信息 |                                 |

---

### `list` 数组元素

| 字段              | 类型     | 内容             | 备注                              |
| ----------------- | -------- | ---------------- | --------------------------------- |
| type              | num      | 权益类型 ID      | 见下方权益类型表                  |
| state             | num      | 权益状态         | 0：未领取，1：已领取/待领取？     |
| expire_time       | num      | 过期时间戳       | 0 表示无过期限制                  |
| vip_type          | num      | 需要的会员类型   | 0：非会员，1：大会员              |
| next_receive_days | num      | 距离可领取的天数 | -1 表示不可领取                   |
| period_end_unix   | num      | 周期结束时间戳   |                                   |
| is_count          | bool     | 是否计入统计     |                                   |
| name              | str      | 权益名称         | 通常为空                          |
| coupon_code       | str      | 优惠券码         | 通常为空                          |
| app_describe      | str      | APP 端描述       | 通常为空                          |
| recive_state      | num      | 领取状态         | 0：不可领取，1：可领取，2：已领取 |
| salary_type       | num      | 发放类型         | 0：周期性发放，1：一次性发放？    |
| exp_params        | obj/null | 实验参数         |                                   |
| extra_params      | obj/null | 额外参数         |                                   |

---

### 权益类型（`type`）枚举

| 值      | 含义（推测）                         | 备注                                       |
| ------- | ------------------------------------ | ------------------------------------------ |
| 1       | B币券（5元）                         | 每月可领                                   |
| 2       | 会员购优惠券                         |                                            |
| 3       | 游戏礼包                             |                                            |
| 4       | 漫画券                               |                                            |
| 5       | 阅读券                               |                                            |
| 6       | 装扮券                               |                                            |
| 7       | 直播礼物                             |                                            |
| 8       | 游戏加速                             | 已领取（`state=1`）                        |
| 9       | 其他权益                             |                                            |
| 14      | 会员购优惠券                         | 带实验参数                                 |
| 18      | 权益（一次性）                       | `salary_type=1`                            |
| 19      | 权益（一次性）                       | 可领取（`is_allowe_receive=true`）         |
| 20      | 权益（不可领取）                     | `is_allowe_receive=false`                  |
| 21      | 权益（不展示）                       | `is_show=false`                            |
| 22      | 游戏加速                             | 已领取                                     |
| 24      | 权益（周期）                         |                                            |
| 25      | 权益（周期）                         |                                            |
| 26      | 漫展-大会员专属票务优惠券 立减2元    | `extra_params.comic_show_coupon_prop_info` |
| 27      | 漫展-大会员专属票务优惠券 满120减5元 | `extra_params.comic_show_coupon_prop_info` |
| 28      | 权益                                 | 已领取                                     |
| 129-131 | 非会员不可领取权益                   | `vip_type=0`，`recive_state=0`             |
| 200     | 非会员不可领取权益                   | `vip_type=0`，`recive_state=0`             |

---

### `extra_params` 对象（部分权益包含）

| 字段                        | 类型 | 内容                   | 备注                 |
| --------------------------- | ---- | ---------------------- | -------------------- |
| is_allowe_receive           | str  | 是否允许领取           | `"true"` / `"false"` |
| is_show                     | str  | 是否展示               | `"true"` / `"false"` |
| last_salary_time            | str  | 上次发放时间           | Unix 时间戳字符串    |
| now                         | str  | 当前时间               | Unix 时间戳字符串    |
| comic_show_coupon_prop_info | str  | 漫展优惠券 JSON 字符串 | 包含券详情           |

#### `comic_show_coupon_prop_info` 解析

| 字段         | 类型 | 内容             |
| ------------ | ---- | ---------------- |
| prop_id      | num  | 道具 ID          |
| prop_name    | str  | 道具名称         |
| start_time   | str  | 开始时间         |
| end_time     | str  | 结束时间         |
| prop_type    | str  | `"ASSET_COUPON"` |
| leftStock    | num  | 剩余库存         |
| totalStock   | num  | 总库存           |
| person_limit | num  | 每人限领数量     |
| prop_param   | obj  | 优惠券参数       |

---

### `comic_show_coupon` 对象

| 字段            | 类型  | 内容           | 备注 |
| --------------- | ----- | -------------- | ---- |
| hide            | bool  | 是否隐藏       |      |
| state           | num   | 状态           |      |
| count           | num   | 优惠券种类数量 |      |
| title           | str   | 标题           |      |
| sub_title       | str   | 副标题         |      |
| coupons         | array | 优惠券列表     |      |
| promotion_rules | array | 优惠规则列表   |      |
| hide_v2         | bool  | V2 是否隐藏    |      |
| expire_tip      | str   | 过期提示       |      |
| expire_time     | num   | 过期时间戳     |      |

#### `coupons` 数组元素

| 字段              | 类型 | 内容                 |
| ----------------- | ---- | -------------------- |
| amount            | num  | 优惠金额（单位：分） |
| payment_threshold | str  | 使用门槛             |
| title             | str  | 标题                 |
| sub_title         | str  | 副标题               |

---

## 响应示例（脱敏）

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "list": [
            {
                "type": 1,
                "state": 0,
                "expire_time": 0,
                "vip_type": 1,
                "next_receive_days": 17,
                "period_end_unix": 1785168000,
                "is_count": true,
                "recive_state": 1,
                "salary_type": 0,
                "exp_params": {
                    "exp_group_tag": "",
                    "hit_value": 0
                },
                "extra_params": null
            },
            {
                "type": 8,
                "state": 1,
                "expire_time": 1783785600,
                "vip_type": 1,
                "next_receive_days": 1,
                "period_end_unix": 1783785600,
                "is_count": true,
                "recive_state": 2,
                "salary_type": 1,
                "extra_params": null
            }
        ],
        "is_vip": true,
        "vip_status": 1,
        "vip_type": 1,
        "vip_due_date": 1785168000,
        "level": 2,
        "cur_exp": 295,
        "next_exp": 1500,
        "comic_show_coupon": {
            "hide": false,
            "state": 0,
            "count": 2,
            "title": "大会员专属票务优惠券",
            "sub_title": "立减2元 | 满120减5",
            "coupons": [
                {
                    "amount": 200,
                    "payment_threshold": "立减",
                    "title": "大会员专享票务优惠券",
                    "sub_title": "领取后15天内可用"
                },
                {
                    "amount": 500,
                    "payment_threshold": "满120可用",
                    "title": "大会员专享票务优惠券",
                    "sub_title": "领取后15天内可用"
                }
            ],
            "promotion_rules": [
                "立减2元",
                "满120减5"
            ],
            "hide_v2": false,
            "expire_tip": "",
            "expire_time": 0
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
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/vip/privilege/my?mid=123456789&platform=Windows&buvid=xxx' \
  -H 'Referer: https://account.bilibili.com/' \
  -H 'Origin: https://account.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **权益状态判断**：`recive_state` 比 `state` 更直观：
   - `0`：不可领取
   - `1`：可领取
   - `2`：已领取
2. **`next_receive_days`**：表示距离下次可领取的天数，`-1` 表示该权益当前不可领取。
3. **`salary_type`**：
   - `0`：周期性发放（如每月 B 币券）
   - `1`：一次性发放（如首充奖励）
4. **漫展优惠券**：在 `extra_params.comic_show_coupon_prop_info` 中存放 JSON 字符串，需自行解析。
5. **响应中的 `vip_due_date`**：大会员到期时间戳（毫秒级），与 `keeptime_end` 通常相同。
6. **非大会员权益**：`type=200` 和 `129-131` 的 `vip_type=0`，非大会员用户不可领取。


## 相关接口汇总

| 功能           | 接口路径                     | 请求方式 | 关键参数           |
| -------------- | ---------------------------- | -------- | ------------------ |
| 大会员中心信息 | `/x/vip/web/vip_center/info` | GET      | `module_id=700001` |
| 大会员签到     | `/x/vip/experience/add`      | POST     | `mid`、`csrf`      |
| 大会员权益列表 | `/x/vip/privilege/my`        | GET      | `mid`              |
