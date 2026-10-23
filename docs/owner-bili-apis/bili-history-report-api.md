# 历史记录上报（观看进度上报）

## 接口描述

上报用户观看视频的进度，用于记录观看历史和播放进度。该接口在用户观看视频时会定期或退出时调用。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于记录观看历史和播放进度。

---

## 接口地址

```
POST https://api.bilibili.com/x/v2/history/report
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名 | 类型 | 内容       | 必要性   | 备注                           |
| ------ | ---- | ---------- | -------- | ------------------------------ |
| aid    | num  | 视频 AV ID | **必要** |                                |
| type   | num  | 上报类型   | **必要** | 固定传 `5`，可能表示视频观看   |
| dt     | num  | 设备类型   | 非必要   | 固定传 `2`，可能表示 Web 端    |
| csrf   | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

**示例请求体：**

```
aid=21848272&type=5&dt=2&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |

**响应示例：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1
}
```

---

## 错误码

| 状态码 | 含义                                     |
| ------ | ---------------------------------------- |
| 0      | 操作成功                                 |
| -101   | 未登录（Cookie 无效或过期）              |
| -403   | CSRF 验证失败（`bili_jct` 不匹配或过期） |
| 其他   | 参见 `message` 字段                      |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/v2/history/report' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'aid=21848272' \
  --data-urlencode 'type=5' \
  --data-urlencode 'dt=2' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
3. **上报时机**：通常在视频播放过程中定期上报，或在用户退出视频页面时上报。
4. **与历史记录列表的关系**：该接口上报的数据会出现在历史记录列表（`/x/web-interface/history/cursor`）中。
