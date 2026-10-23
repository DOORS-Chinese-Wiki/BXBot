# B币钱包 API

## 接口列表

### 1. B币充值记录查询
### 2. B币消费记录查询

---

# 1. B币充值记录查询

## 接口描述

查询当前用户的 B 币充值记录，包含充值到账明细，支持按时间范围分页查询。

> 该接口位于支付域名 `pay.bilibili.com`，用于 B 币钱包的充值记录展示（B币购买记录）。

---

## 接口地址

```
POST https://pay.bilibili.com/paywallet/wallet/listForUserRecharges
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（JSON Body）

| 参数名      | 类型 | 内容         | 必要性 | 备注                              |
| ----------- | ---- | ------------ | ------ | --------------------------------- |
| currentPage | num  | 当前页码     | 必要   | 从 1 开始                         |
| pageSize    | num  | 每页条数     | 必要   | 通常为 10、20、50                 |
| beginTime   | str  | 查询开始时间 | 必要   | 格式 `YYYY-MM-DD HH:mm:ss`        |
| endTime     | str  | 查询结束时间 | 必要   | 格式 `YYYY-MM-DD HH:mm:ss`        |
| timestamp   | num  | 当前时间戳   | 必要   | 毫秒级                            |
| traceId     | num  | 请求追踪 ID  | 必要   | 毫秒级时间戳，与 `timestamp` 相同 |
| version     | str  | 接口版本     | 必要   | 固定为 `"1.0"`                    |

**示例请求体：**

```json
{
    "currentPage": 1,
    "pageSize": 10,
    "beginTime": "2026-01-01 00:00:00",
    "endTime": "2026-07-11 23:59:59",
    "timestamp": 1783747102000,
    "traceId": 1783747102000,
    "version": "1.0"
}
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容         | 备注             |
| ------- | ---- | ------------ | ---------------- |
| code    | num  | 状态码       | 0 表示成功       |
| errno   | num  | 错误编号     | 0 表示无错误     |
| msg     | str  | 英文状态信息 | `"SUCCESS"`      |
| showMsg | str  | 中文提示信息 | 如 `"交易成功"`  |
| data    | obj  | 数据本体     |                  |
| success | bool | 是否成功     | `true` / `false` |

### `data` 对象

| 字段   | 类型  | 内容         | 备注               |
| ------ | ----- | ------------ | ------------------ |
| page   | obj   | 分页信息     |                    |
| result | array | 充值记录列表 | 每条记录为一个对象 |

### `page` 对象

| 字段        | 类型 | 内容     |
| ----------- | ---- | -------- |
| currentPage | num  | 当前页码 |
| pageSize    | num  | 每页条数 |
| totalCount  | num  | 总记录数 |
| totalPage   | num  | 总页数   |

### `result` 数组元素

| 字段          | 类型 | 内容                 | 备注                                              |
| ------------- | ---- | -------------------- | ------------------------------------------------- |
| rechargeTime  | num  | 充值时间戳           | 毫秒级 Unix 时间戳                                |
| wxId          | str  | 交易流水号           | 全局唯一标识                                      |
| payAmount     | num  | 支付金额（元）       | 单位：人民币元，保留两位小数                      |
| payAmountDesc | str  | 支付金额格式化字符串 | 如 `"¥8.00"`，用于前端展示                        |
| bp            | num  | 到账 B 币数量        | 1 B币 = 1 元                                      |
| channelName   | str  | 支付渠道名称         | `"微信"`、`"待支付"`、`"支付宝"`、`"苹果IAP"` 等  |
| status        | num  | 交易状态码           | 见下方状态枚举表                                  |
| refundStatus  | num  | 退款状态码           | 0：无退款                                         |
| refundBp      | num  | 退款金额（B币）      | 单位：B币                                         |
| platformType  | num  | 平台类型             | 0 表示 B 站平台                                   |
| remark        | str  | 交易备注             | 如 `"用户xxx购买8.00B币"`、`"包月充电PC充值面板"` |

---

## 交易状态码（`status`）

| 状态码 | 含义            | 备注                   |
| ------ | --------------- | ---------------------- |
| 0      | 未支付 / 待支付 | 订单已创建但未完成支付 |
| 4      | 支付成功        | 充值已完成，B币已到账  |

> **说明**：充值记录中的 `status=4` 表示充值成功；`status=0` 表示未支付订单（如发起充值后未完成付款）。

---

## 错误码

| 状态码 | 含义                             |
| ------ | -------------------------------- |
| 0      | 请求成功                         |
| -101   | 未登录（Cookie 无效或过期）      |
| 其他   | 参见 `showMsg` 或 `msg` 字段说明 |

---

## 调用示例（curl）

```bash
curl 'https://pay.bilibili.com/paywallet/wallet/listForUserRecharges' \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://pay.bilibili.com/pay-v2-web/bcoin_record' \
  -H 'Origin: https://pay.bilibili.com' \
  -b 'SESSDATA=xxx' \
  --data-raw '{
    "currentPage": 1,
    "pageSize": 10,
    "beginTime": "2026-01-01 00:00:00",
    "endTime": "2026-07-11 23:59:59",
    "timestamp": 1783747102000,
    "traceId": 1783747102000,
    "version": "1.0"
  }'
```

---

## 响应示例

```json
{
    "code": 0,
    "errno": 0,
    "msg": "SUCCESS",
    "showMsg": "交易成功",
    "data": {
        "page": {
            "currentPage": 1,
            "pageSize": 10,
            "totalCount": 7,
            "totalPage": 1
        },
        "result": [
            {
                "rechargeTime": 1781316881000,
                "wxId": "1317819266174689651",
                "payAmount": 8.00,
                "payAmountDesc": "¥8.00",
                "bp": 8.00,
                "channelName": "微信",
                "status": 4,
                "refundStatus": 0,
                "refundBp": 0,
                "platformType": 0,
                "remark": "用户3690995472402999购买8.00B币"
            },
            {
                "rechargeTime": 1774092726000,
                "wxId": "1227273417640796596",
                "payAmount": 68.00,
                "payAmountDesc": "¥68.00",
                "bp": 68.00,
                "channelName": "待支付",
                "status": 0,
                "refundStatus": 0,
                "refundBp": 0,
                "platformType": 0,
                "remark": "用户3690995472402999购买68.00B币"
            }
        ]
    },
    "success": true
}
```

---

## 注意事项

1. **时间范围**：查询跨度建议不超过 30 天，实际以客户端限制为准。
2. **认证**：必须携带有效的 `SESSDATA` Cookie，否则返回 `-101` 未登录。
3. **Referer 与 Origin**：请求需携带 `Referer: https://pay.bilibili.com/pay-v2-web/bcoin_record` 和 `Origin: https://pay.bilibili.com`，否则可能因跨域策略被拒绝。
4. **timestamp 与 traceId**：取当前毫秒级时间戳，两者值保持一致即可。
5. **分页**：当 `totalCount` 为 0 时，表示当前时间范围内无充值记录。
6. **金额单位**：`payAmount` 为人民币元，`bp` 为 B 币数量，两者数值相等（1 B币 = 1 元）。
7. **待支付记录**：`status=0` 且 `channelName="待支付"` 的订单表示用户发起了充值但未完成支付，不会实际到账。
8. **接口区分**：
   - `/wallet/listForUserRecharges`：充值记录（B币购买）
   - `/wallet/listForUserPays`：消费记录（B币支出）

---

# 2. B币消费记录查询

## 接口描述

查询当前用户的 B 币消费/交易记录，包含 B 币消费明细，支持按时间范围分页查询。

> 该接口位于支付域名 `pay.bilibili.com`，用于 B 币钱包的消费明细展示。

---

## 接口地址

```
POST https://pay.bilibili.com/paywallet/wallet/listForUserPays
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（JSON Body）

| 参数名      | 类型 | 内容         | 必要性 | 备注                              |
| ----------- | ---- | ------------ | ------ | --------------------------------- |
| currentPage | num  | 当前页码     | 必要   | 从 1 开始                         |
| pageSize    | num  | 每页条数     | 必要   | 通常为 10、20、50                 |
| beginTime   | str  | 查询开始时间 | 必要   | 格式 `YYYY-MM-DD HH:mm:ss`        |
| endTime     | str  | 查询结束时间 | 必要   | 格式 `YYYY-MM-DD HH:mm:ss`        |
| timestamp   | num  | 当前时间戳   | 必要   | 毫秒级                            |
| traceId     | num  | 请求追踪 ID  | 必要   | 毫秒级时间戳，与 `timestamp` 相同 |
| version     | str  | 接口版本     | 必要   | 固定为 `"1.0"`                    |

**示例请求体：**

```json
{
    "currentPage": 1,
    "pageSize": 10,
    "beginTime": "2026-07-05 00:00:00",
    "endTime": "2026-07-11 23:59:59",
    "timestamp": 1783746864000,
    "traceId": 1783746864000,
    "version": "1.0"
}
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容         | 备注             |
| ------- | ---- | ------------ | ---------------- |
| code    | num  | 状态码       | 0 表示成功       |
| errno   | num  | 错误编号     | 0 表示无错误     |
| msg     | str  | 英文状态信息 | `"SUCCESS"`      |
| showMsg | str  | 中文提示信息 | 如 `"交易成功"`  |
| data    | obj  | 数据本体     |                  |
| success | bool | 是否成功     | `true` / `false` |

### `data` 对象

| 字段   | 类型  | 内容         | 备注               |
| ------ | ----- | ------------ | ------------------ |
| page   | obj   | 分页信息     |                    |
| result | array | 交易记录列表 | 每条记录为一个对象 |

### `page` 对象

| 字段        | 类型 | 内容     |
| ----------- | ---- | -------- |
| currentPage | num  | 当前页码 |
| pageSize    | num  | 每页条数 |
| totalCount  | num  | 总记录数 |
| totalPage   | num  | 总页数   |

### `result` 数组元素

| 字段         | 类型 | 内容              | 备注                                   |
| ------------ | ---- | ----------------- | -------------------------------------- |
| wxId         | str  | 交易流水号        | 全局唯一标识                           |
| orderId      | str  | 订单号            | 通常与 `wxId` 相同                     |
| status       | num  | 交易状态码        | 见下方状态枚举表                       |
| refundStatus | num  | 退款状态码        | 0：无退款                              |
| refundBp     | num  | 退款金额（B币）   | 单位：B币                              |
| remark       | str  | 交易备注          | 商品名称等                             |
| payAmount    | num  | 支付金额（B币）   | 单位：B币，保留两位小数                |
| totalBp      | num  | 总交易金额（B币） | 单位：B币                              |
| bp           | num  | 实际扣除B币数     | 单位：B币，与 `totalBp` 相同           |
| coupon       | num  | 优惠券抵扣金额    | 单位：B币                              |
| platformType | num  | 平台类型          | 0 表示 B 站平台                        |
| payTime      | num  | 支付时间戳        | 毫秒级 Unix 时间戳                     |
| channelName  | str  | 支付渠道/业务名称 | 如 `"收藏集"`、`"大会员"`、`"B币充值"` |
| channelLogo  | str  | 渠道 Logo 地址    | 通常为空                               |
| channelUrl   | str  | 渠道跳转链接      | 通常为 `null`                          |

---

## 交易状态码（`status`）

| 状态码 | 含义     | 备注     |
| ------ | -------- | -------- |
| 4      | 支付成功 | 交易完成 |

> **说明**：根据实际抓包数据，`status=4` 表示支付成功。其他状态码（如 0、1、2、3、5 等）待补充，可能对应：待支付、处理中、支付失败、已退款等。

---

## 错误码

| 状态码 | 含义                             |
| ------ | -------------------------------- |
| 0      | 请求成功                         |
| -101   | 未登录（Cookie 无效或过期）      |
| 其他   | 参见 `showMsg` 或 `msg` 字段说明 |

---

## 调用示例（curl）

```bash
curl 'https://pay.bilibili.com/paywallet/wallet/listForUserPays' \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://pay.bilibili.com/pay-v2-web/bcoin_record' \
  -H 'Origin: https://pay.bilibili.com' \
  -b 'SESSDATA=xxx' \
  --data-raw '{
    "currentPage": 1,
    "pageSize": 10,
    "beginTime": "2026-07-05 00:00:00",
    "endTime": "2026-07-11 23:59:59",
    "timestamp": 1783746864000,
    "traceId": 1783746864000,
    "version": "1.0"
  }'
```

---

## 响应示例

```json
{
    "code": 0,
    "errno": 0,
    "msg": "SUCCESS",
    "showMsg": "交易成功",
    "data": {
        "page": {
            "currentPage": 1,
            "pageSize": 10,
            "totalCount": 2,
            "totalPage": 1
        },
        "result": [
            {
                "wxId": "1317793994484355900",
                "orderId": "1317793994484355900",
                "status": 4,
                "refundStatus": 0,
                "refundBp": 0,
                "remark": "洛少爷收藏集",
                "payAmount": 9.90,
                "totalBp": 9.90,
                "bp": 9.90,
                "coupon": 0,
                "platformType": 0,
                "payTime": 1781316920000,
                "channelName": "收藏集",
                "channelLogo": "",
                "channelUrl": null
            },
            {
                "wxId": "1227278657509315717",
                "orderId": "1227278657509315717",
                "status": 4,
                "refundStatus": 0,
                "refundBp": 0,
                "remark": "洛少爷收藏集",
                "payAmount": 4.90,
                "totalBp": 4.90,
                "bp": 4.90,
                "coupon": 0,
                "platformType": 0,
                "payTime": 1771417268000,
                "channelName": "收藏集",
                "channelLogo": "",
                "channelUrl": null
            }
        ]
    },
    "success": true
}
```

---

## 注意事项

1. **时间范围**：查询跨度通常建议不超过 30 天，实际以客户端限制为准。
2. **认证**：必须携带有效的 `SESSDATA` Cookie，否则返回 `-101` 未登录。
3. **Referer 与 Origin**：请求需携带 `Referer: https://pay.bilibili.com/pay-v2-web/bcoin_record` 和 `Origin: https://pay.bilibili.com`，否则可能因跨域策略被拒绝。
4. **timestamp 与 traceId**：取当前毫秒级时间戳，两者值保持一致即可。
5. **分页**：当 `totalCount` 为 0 时，表示当前时间范围内无交易记录。
6. **金额单位**：所有金额字段（`payAmount`、`totalBp`、`bp`、`coupon`、`refundBp`）单位均为 **B币**（1 B币 = 1 元），保留两位小数。
7. **接口区分**：
   - `/wallet/listForUserRecharges`：充值记录（B币购买）
   - `/wallet/listForUserPays`：消费记录（B币支出）
