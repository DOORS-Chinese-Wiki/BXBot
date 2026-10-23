# UP主评论精选列表

## 接口描述

获取当前登录用户（UP主）所有稿件中待精选的评论列表，支持按时间、状态、等级等条件筛选。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于创作中心/UP主后台的评论精选管理页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/v2/reply/up/selection/list
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名        | 类型 | 内容     | 必要性 | 备注                               |
| ------------- | ---- | -------- | ------ | ---------------------------------- |
| business      | str  | 业务类型 | 非必要 | `archive`：视频稿件                |
| oid           | str  | 对象 ID  | 非必要 | 指定稿件的 `aid`，为空表示所有稿件 |
| time_interval | num  | 时间区间 | 非必要 | `0`：全部时间                      |
| state         | num  | 精选状态 | 非必要 | `1`：待精选                        |
| level         | num  | 评论等级 | 非必要 | `0`：全部等级                      |
| sort          | str  | 排序方式 | 非必要 | `desc`：倒序（最新在前）           |
| pn            | num  | 页码     | 非必要 | 默认 1                             |
| ps            | num  | 每页数量 | 非必要 | 默认 10，最大 50                   |

**示例请求 URL：**

```
https://api.bilibili.com/x/v2/reply/up/selection/list?business=archive&oid=&time_interval=0&state=1&level=0&sort=desc&pn=1&ps=10
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

| 字段    | 类型       | 内容     | 备注              |
| ------- | ---------- | -------- | ----------------- |
| total   | num        | 总记录数 |                   |
| num     | num        | 当前页码 |                   |
| size    | num        | 每页条数 |                   |
| replies | array/null | 评论列表 | 无数据时为 `null` |

### `replies` 数组元素

与评论列表接口（`/x/v2/reply/wbi/main`）中的 `replies` 数组元素结构相同，包含：

| 字段          | 类型 | 内容           | 备注                                  |
| ------------- | ---- | -------------- | ------------------------------------- |
| rpid          | num  | 评论 ID        | 全局唯一                              |
| oid           | num  | 对象 ID        | 视频 AV ID                            |
| type          | num  | 评论类型       | `1`：视频评论                         |
| mid           | num  | 评论者 UID     |                                       |
| ctime         | num  | 发布时间戳     | Unix 时间戳（秒）                     |
| like          | num  | 点赞数         |                                       |
| member        | obj  | 评论者信息     | 含 `uname`、`avatar`、`level_info` 等 |
| content       | obj  | 评论内容       | 含 `message`、`emote` 等              |
| title         | str  | 视频标题       |                                       |
| cover_url     | str  | 视频封面图地址 |                                       |
| bvid          | str  | 视频 BV ID     |                                       |
| reply_control | obj  | 回复控制信息   | 含 `is_top`（是否置顶）等             |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "total": 0,
        "num": 1,
        "size": 10,
        "replies": null
    }
}
```

**有数据时：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "total": 5,
        "num": 1,
        "size": 10,
        "replies": [
            {
                "rpid": 301766511393,
                "oid": 116579002029229,
                "type": 1,
                "mid": 3546618192202347,
                "ctime": 1780713643,
                "like": 19,
                "member": {
                    "mid": "3546618192202347",
                    "uname": "洛琏琴",
                    "avatar": "https://i0.hdslb.com/bfs/face/xxx.jpg"
                },
                "content": {
                    "message": "小蛋糕就应该老老实实呆在蛋糕店啊喂"
                },
                "title": "[开源项目]KernelBase",
                "cover_url": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
                "bvid": "BV1rR5i6GEHP",
                "reply_control": {
                    "is_top": false
                }
            }
        ]
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
curl 'https://api.bilibili.com/x/v2/reply/up/selection/list?business=archive&oid=&time_interval=0&state=1&level=0&sort=desc&pn=1&ps=10' \
  -H 'Referer: https://member.bilibili.com/' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限 UP 主**：该接口只能查询当前登录用户（需为 UP 主）的待精选评论列表。
3. **`state=1`**：表示待精选状态，用于筛选。
4. **与 `bili-reply-up-list-api.md` 的区别**：
   - `bili-reply-up-list-api.md`：所有稿件的评论管理列表（含已发布、待审核等）
   - 本接口：专门筛选“待精选”状态的评论
