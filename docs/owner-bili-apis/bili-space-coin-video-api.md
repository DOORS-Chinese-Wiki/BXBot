# 获取用户投币视频列表

## 接口描述

获取指定用户投过币的视频列表（投币历史记录）。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间“我的投币”页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/coin/video
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注           |
| ------------ | ---- | -------- | -------- | -------------- |
| vmid         | num  | 用户 UID | **必要** | 目标用户的 UID |
| pn           | num  | 页码     | 非必要   | 默认 1         |
| ps           | num  | 每页数量 | 非必要   | 默认 ？        |
| web_location | str  | 来源标识 | 非必要   | `333.1387`     |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/coin/video?vmid=3690995472402999&web_location=333.1387
```

---

## 响应结构

### 根对象

| 字段    | 类型  | 内容         | 备注       |
| ------- | ----- | ------------ | ---------- |
| code    | num   | 状态码       | 0 表示成功 |
| message | str   | 状态信息     | `"OK"`     |
| ttl     | num   | 1            |            |
| data    | array | 投币视频列表 |            |

### `data` 数组元素（关键字段）

| 字段    | 类型 | 内容       | 备注                           |
| ------- | ---- | ---------- | ------------------------------ |
| aid     | num  | 视频 AV ID |                                |
| bvid    | str  | 视频 BV ID |                                |
| title   | str  | 视频标题   |                                |
| pic     | str  | 封面图地址 |                                |
| pubdate | num  | 发布时间戳 |                                |
| owner   | obj  | UP 主信息  | 包含 `mid`、`name`、`face`     |
| stat    | obj  | 统计数据   |                                |
| coins   | num  | 投币数量   | **该用户给这个视频投了多少币** |
| time    | num  | 投币时间戳 |                                |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": [
        {
            "aid": 113433592792165,
            "bvid": "BV1XkDgYQEUG",
            "title": "【Hi-Res】《远走高飞》金志文",
            "pic": "http://i1.hdslb.com/bfs/archive/xxx.jpg",
            "owner": {
                "mid": 3546683705133415,
                "name": "大猫一日同风起"
            },
            "stat": {
                "view": 38059,
                "like": 222
            },
            "coins": 1,
            "time": 1782472975
        }
    ]
}
```
