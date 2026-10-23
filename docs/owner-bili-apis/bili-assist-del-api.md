# UP主协管员移除

## 接口描述

将指定协管员（骑士团成员）从当前用户的协管员列表中移除，撤销其所有管理权限。

> 该接口位于创作中心域名 `member.bilibili.com`，用于UP主移除协管员。

---

## 接口地址

```
POST https://member.bilibili.com/x/web/assist/del
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/x-www-form-urlencoded; charset=UTF-8`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据）

| 参数名     | 类型 | 内容       | 必要性   | 备注                           |
| ---------- | ---- | ---------- | -------- | ------------------------------ |
| assist_mid | num  | 协管员 UID | **必要** | 要移除的协管员用户 ID          |
| csrf       | str  | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |

**示例请求体：**

```
assist_mid=3546913664142201&csrf=1eaefa721216ddee6444fcbedace61b2
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
curl 'https://member.bilibili.com/x/web/assist/del' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Referer: https://member.bilibili.com/platform/fans/assist' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-urlencode 'assist_mid=3546913664142201' \
  --data-urlencode 'csrf=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **CSRF 校验**：需携带 Cookie 中的 `bili_jct` 和表单中的 `csrf` 参数，两者值一致。
3. **仅限 UP 主**：该接口只能由 UP 主本人操作。
4. **不可逆操作**：移除协管员后，该用户将失去所有管理权限，需重新添加才能恢复。
5. **与添加接口的区别**：
   - `/add`：添加协管员（需同时传递 `main` 和 `live` 权限参数）
   - `/del`：移除协管员（仅需 `assist_mid` 和 `csrf`）
