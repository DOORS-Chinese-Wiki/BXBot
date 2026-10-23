好的，这是一个 **获取用户置顶视频** 的接口，虽然返回了“没有置顶视频”，但接口本身是有效的。

---

# 获取用户置顶视频

## 接口描述

获取指定用户个人空间置顶的视频信息。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于查询用户置顶视频。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/top/arc
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`

---

## 请求参数（URL Query）

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| vmid | num | 用户 UID | **必要** | 目标用户的 UID |
| web_location | str | 来源标识 | 非必要 | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/top/arc?vmid=3690995472402999&web_location=333.1387
```

---

## 响应结构

### 根对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| code | num | 状态码 | 0：成功，53016：没有置顶视频 |
| message | str | 状态信息 | `"没有置顶视频"` |
| ttl | num | 1 | |
| data | obj/null | 数据本体 | 成功时返回视频信息，无置顶时为 null |

### `data` 对象（有置顶视频时）

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| aid | num | 视频 AV ID | |
| bvid | str | 视频 BV ID | |
| title | str | 视频标题 | |
| pic | str | 封面图地址 | |
| owner | obj | UP 主信息 | |
| stat | obj | 统计数据 | 播放量、点赞、投币等 |
| pubdate | num | 发布时间戳 | Unix 时间戳（秒） |
| … | … | … | 与视频信息接口结构类似 |

**响应示例（无置顶）：**

```json
{
    "code": 53016,
    "message": "没有置顶视频",
    "ttl": 1,
    "data": null
}
```

**响应示例（有置顶）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "aid": 116579002029229,
        "bvid": "BV1rR5i6GEHP",
        "title": "【开源项目】KernelBase",
        "pic": "http://i0.hdslb.com/bfs/archive/xxx.jpg",
        "owner": {
            "mid": 3690995472402999,
            "name": "YunLv_L"
        },
        "stat": {
            "view": 661,
            "like": 13
        },
        "pubdate": 1778855016
    }
}
```

---

## 错误码

| 状态码 | 含义 |
| ------ | ---- |
| 0 | 请求成功（有置顶视频） |
| 53016 | 该用户没有置顶视频 |
| -101 | 未登录（Cookie 无效或过期） |
| 其他 | 参见 `message` 字段 |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/space/top/arc?vmid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **`code=53016` 是正常情况**：表示该用户没有置顶视频，不是错误。
2. **无需 WBI 签名**：该接口不需要 WBI 签名。
3. **`data` 字段**：有置顶视频时返回视频详细信息，无置顶时为 `null`。
4. **用途**：可用于获取用户个人空间的置顶视频，配合空间页面展示。