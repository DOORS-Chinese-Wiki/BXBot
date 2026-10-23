# UP主协管员添加

## 接口描述

添加指定用户为协管员（骑士团成员），并分配权限。

> 该接口位于创作中心域名 `member.bilibili.com`，用于UP主添加协管员。

---

## 接口地址

```
POST https://member.bilibili.com/x/web/assist/add
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded; charset=UTF-8`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名     | 类型 | 内容       | 必要性   | 备注                                            |
| ---------- | ---- | ---------- | -------- | ----------------------------------------------- |
| assist_mid | num  | 协管员 UID | **必要** | 要添加的用户 ID                                 |
| main       | num  | 主站权限   | 非必要   | `1`：授予主站管理权限（弹幕/评论），`0`：不授予 |
| live       | num  | 直播权限   | 非必要   | `1`：授予直播管理权限，`0`：不授予              |
| csrf       | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值                  |

**示例请求体：**

```
assist_mid=3546913664142201&main=1&live=0&csrf=1eaefa721216ddee6444fcbedace61b2
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "0",
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
curl 'https://member.bilibili.com/x/web/assist/add' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Referer: https://member.bilibili.com/platform/fans/assist' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'assist_mid=3546913664142201' \
  --data-urlencode 'main=1' \
  --data-urlencode 'live=0' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
3. **权限说明**：
   - `main=1`：协管员可管理主站弹幕和评论
   - `live=1`：协管员可管理直播（如直播间禁言等）
4. **仅限 UP 主**：该接口只能由 UP 主本人操作。
5. **与移除接口的区别**：
   - `/add`：添加协管员
   - `/del`：移除协管员（待抓取）
