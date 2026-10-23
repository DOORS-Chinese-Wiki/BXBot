# UP主协管员（骑士团）列表

## 接口描述

获取当前登录用户授权的协管员（骑士团成员）列表，包含协管员基本信息、权限分配、任命时间等。

> 该接口位于创作中心域名 `member.bilibili.com`，用于UP主管理协管员。

---

## 接口地址

```
GET https://member.bilibili.com/x/web/assist
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数

无请求参数。仅需携带有效的 Cookie（`SESSDATA`）。

**示例请求 URL：**

```
https://member.bilibili.com/x/web/assist
```

---

## 响应结构

### 根对象

| 字段    | 类型  | 内容       | 备注       |
| ------- | ----- | ---------- | ---------- |
| code    | num   | 状态码     | 0 表示成功 |
| message | str   | 状态信息   | `"0"`      |
| ttl     | num   | 1          |            |
| data    | array | 协管员列表 |            |

### `data` 数组元素

| 字段          | 类型 | 内容           | 备注              |
| ------------- | ---- | -------------- | ----------------- |
| assist_mid    | num  | 协管员 UID     |                   |
| assist_name   | str  | 协管员昵称     |                   |
| assist_avatar | str  | 协管员头像地址 |                   |
| banned        | num  | 是否被禁用     | 0：否             |
| rights        | obj  | 权限信息       |                   |
| ctime         | num  | 任命时间戳     | Unix 时间戳（秒） |
| mtime         | num  | 最后修改时间戳 | Unix 时间戳（秒） |
| total         | obj  | 操作统计信息   |                   |

### `rights` 对象

| 字段 | 类型 | 内容     | 备注      |
| ---- | ---- | -------- | --------- |
| main | num  | 主站权限 | 1：有权限 |
| live | num  | 直播权限 | 0：无权限 |

### `total` 对象

| 字段   | 类型 | 内容         | 备注           |
| ------ | ---- | ------------ | -------------- |
| amtmap | obj  | 操作统计映射 | key 为操作类型 |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": [
        {
            "assist_mid": 3546813281864337,
            "banned": 0,
            "assist_avatar": "https://i0.hdslb.com/bfs/face/xxx.jpg",
            "assist_name": "洛灵熙xr",
            "rights": {
                "main": 1,
                "live": 0
            },
            "ctime": 1770542167,
            "mtime": 1780206039,
            "total": {}
        },
        {
            "assist_mid": 3707015195003287,
            "banned": 0,
            "assist_avatar": "https://i1.hdslb.com/bfs/face/xxx.jpg",
            "assist_name": "YunLv-L",
            "rights": {
                "main": 1,
                "live": 0
            },
            "ctime": 1782429304,
            "mtime": 1782429304,
            "total": {
                "amtmap": {
                    "1": {
                        "amtrmap": {
                            "1": 1
                        }
                    }
                }
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
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://member.bilibili.com/x/web/assist' \
  -H 'Referer: https://member.bilibili.com/' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限 UP 主**：该接口只能查询当前登录用户（需为 UP 主）的协管员列表。
3. **`rights.main`**：`1` 表示有主站管理权限（弹幕/评论管理），`0` 表示无权限。
4. **`total.amtmap`**：记录了协管员的操作统计，结构较复杂，通常用于展示操作日志。
