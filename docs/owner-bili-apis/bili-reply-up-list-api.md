# UP主评论管理列表

## 接口描述

获取当前登录用户（UP主）在所有稿件下的评论列表，包含自己发布的和粉丝的评论，支持排序和筛选。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于创作中心/UP主后台的评论管理页面展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/v2/reply/up/fulllist
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名             | 类型 | 内容         | 必要性 | 备注                        |
| ------------------ | ---- | ------------ | ------ | --------------------------- |
| order              | num  | 排序方式     | 非必要 | `1`：按时间倒序（最新在前） |
| filter             | num  | 筛选类型     | 非必要 | `-1`：全部                  |
| type               | num  | 评论类型     | 非必要 | `1`：视频评论               |
| bvid               | str  | 视频 BV ID   | 非必要 | 指定视频的评论              |
| pn                 | num  | 页码         | 非必要 | 默认 1                      |
| ps                 | num  | 每页数量     | 非必要 | 默认 10，最大 50            |
| charge_plus_filter | bool | 充电专属筛选 | 非必要 | `false`：不筛选             |

**示例请求 URL：**

```
https://api.bilibili.com/x/v2/reply/up/fulllist?order=1&filter=-1&type=1&bvid=&pn=1&ps=10&charge_plus_filter=false
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

| 字段             | 类型  | 内容         | 备注           |
| ---------------- | ----- | ------------ | -------------- |
| page             | obj   | 分页信息     |                |
| list             | array | 评论列表     |                |
| always_translate | bool  | 是否始终翻译 | 通常为 `false` |

### `page` 对象

| 字段  | 类型 | 内容     | 备注 |
| ----- | ---- | -------- | ---- |
| num   | num  | 当前页码 |      |
| size  | num  | 每页条数 |      |
| total | num  | 总记录数 |      |

### `list` 数组元素

| 字段          | 类型       | 内容                 | 备注                 |
| ------------- | ---------- | -------------------- | -------------------- |
| rpid          | num        | 评论 ID              | 全局唯一             |
| oid           | num        | 对象 ID              | 视频 AV ID           |
| type          | num        | 评论类型             | `1`：视频评论        |
| mid           | num        | 评论者 UID           |                      |
| root          | num        | 根评论 ID            | 0 表示主评论         |
| parent        | num        | 父评论 ID            | 0 表示主评论         |
| dialog        | num        | 对话 ID              |                      |
| count         | num        | 子回复总数           |                      |
| rcount        | num        | 子回复总数（含折叠） |                      |
| floor         | num        | 楼层号               |                      |
| state         | num        | 评论状态             |                      |
| fansgrade     | num        | 粉丝等级             |                      |
| attr          | num        | 属性位               |                      |
| ctime         | num        | 发布时间戳           | Unix 时间戳（秒）    |
| like          | num        | 点赞数               |                      |
| action        | num        | 用户操作状态         | 0：无操作，1：已点赞 |
| member        | obj        | 评论者信息           |                      |
| content       | obj        | 评论内容             |                      |
| replies       | null/array | 子回复列表           | 通常为 null          |
| assist        | num        | 辅助信息             |                      |
| up_action     | obj        | UP 主操作状态        |                      |
| invisible     | bool       | 是否不可见           |                      |
| folder        | obj        | 折叠状态             |                      |
| track_info    | str        | 追踪信息             |                      |
| title         | str        | 视频标题             |                      |
| cover_url     | str        | 视频封面图地址       |                      |
| bvid          | str        | 视频 BV ID           |                      |
| reply_control | obj        | 回复控制信息         |                      |
| parent_info   | null/obj   | 父评论信息           |                      |
| root_info     | null/obj   | 根评论信息           |                      |

### `reply_control` 对象

| 字段               | 类型 | 内容            | 备注 |
| ------------------ | ---- | --------------- | ---- |
| up_like            | bool | UP 主是否已点赞 |      |
| is_elec            | bool | 是否充电专属    |      |
| followed           | bool | 是否已关注      |      |
| is_garbage         | bool | 是否垃圾评论    |      |
| is_top             | bool | 是否置顶        |      |
| is_charge_plus     | bool | 是否充电专属    |      |
| extra              | null | 额外信息        |      |
| translation_switch | num  | 翻译开关        |      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "page": {
            "num": 1,
            "size": 10,
            "total": 30
        },
        "list": [
            {
                "rpid": 301766511393,
                "oid": 116579002029229,
                "type": 1,
                "mid": 3690995472402999,
                "ctime": 1780713643,
                "like": 0,
                "member": {
                    "mid": "3690995472402999",
                    "uname": "YunLv_L",
                    "avatar": "https://i0.hdslb.com/bfs/face/xxx.jpg"
                },
                "content": {
                    "message": "KernelBase v1.7.0 已更新！..."
                },
                "title": "[开源项目]KernelBase",
                "cover_url": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
                "bvid": "BV1rR5i6GEHP",
                "reply_control": {
                    "up_like": false,
                    "is_elec": false,
                    "followed": false,
                    "is_top": true
                }
            }
        ],
        "always_translate": false
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
curl 'https://api.bilibili.com/x/v2/reply/up/fulllist?order=1&filter=-1&type=1&bvid=&pn=1&ps=10&charge_plus_filter=false' \
  -H 'Referer: https://member.bilibili.com/' \
  -H 'Origin: https://member.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **仅限 UP 主**：该接口只能查询当前登录用户（需为 UP 主）的评论管理列表。
3. **与普通评论列表的区别**：
   - 普通评论列表：`/x/v2/reply/wbi/main`（需 `oid`，针对单个视频）
   - UP主评论管理：`/x/v2/reply/up/fulllist`（无需 `oid`，跨所有稿件）
4. **`reply_control.is_top`**：`true` 表示该评论已被置顶。
5. **`reply_control.up_like`**：`true` 表示 UP 主已点赞该评论。
