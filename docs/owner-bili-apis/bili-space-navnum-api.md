# 获取用户空间导航计数

## 接口描述

获取指定用户在个人空间各模块的内容数量统计，包含视频、番剧、收藏、相簿、图文动态等。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于个人空间页面展示各模块的数量徽标。

---

## 接口地址

```
GET https://api.bilibili.com/x/space/navnum
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容     | 必要性   | 备注                       |
| ------------ | ---- | -------- | -------- | -------------------------- |
| mid          | num  | 用户 UID | **必要** | 目标用户的 UID             |
| web_location | str  | 来源标识 | 非必要   | 固定传 `333.1387` 或类似值 |

**示例请求 URL：**

```
https://api.bilibili.com/x/space/navnum?mid=3690995472402999&web_location=333.1387
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

| 字段       | 类型 | 内容       | 备注 |
| ---------- | ---- | ---------- | ---- |
| video      | num  | 视频投稿数 |      |
| bangumi    | num  | 追番数     |      |
| cinema     | num  | 追影视数   |      |
| channel    | obj  | 频道数     |      |
| favourite  | obj  | 收藏夹数   |      |
| tag        | num  | 标签数     |      |
| article    | num  | 专栏文章数 |      |
| playlist   | num  | 视频列表数 |      |
| album      | num  | 相簿数     |      |
| audio      | num  | 音频数     |      |
| pugv       | num  | PUGV 数    |      |
| season_num | num  | 剧集数     |      |
| opus       | num  | 图文动态数 |      |

### `channel` 对象

| 字段   | 类型 | 内容       | 备注 |
| ------ | ---- | ---------- | ---- |
| master | num  | 主频道数   |      |
| guest  | num  | 客串频道数 |      |

### `favourite` 对象

| 字段   | 类型 | 内容         | 备注 |
| ------ | ---- | ------------ | ---- |
| master | num  | 主收藏夹数   |      |
| guest  | num  | 客串收藏夹数 |      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "video": 5,
        "bangumi": 2,
        "cinema": 3,
        "channel": {
            "master": 0,
            "guest": 0
        },
        "favourite": {
            "master": 11,
            "guest": 11
        },
        "tag": 0,
        "article": 0,
        "playlist": 0,
        "album": 30,
        "audio": 0,
        "pugv": 0,
        "season_num": 0,
        "opus": 30
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
curl 'https://api.bilibili.com/x/space/navnum?mid=3690995472402999&web_location=333.1387' \
  -H 'Referer: https://space.bilibili.com/' \
  -H 'Origin: https://space.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`album` 与 `opus` 的关系**：两者数值通常相同，`album` 为历史字段，`opus` 为图文动态的新字段。
3. **`favourite` 中的 `master` 和 `guest`**：`master` 为自己创建的收藏夹，`guest` 为他人创建的收藏夹（你收藏了别人的收藏夹）。
4. **各模块显示条件**：部分模块（如 `tag`、`audio`、`pugv`）数量为 0 时，在个人空间页面可能不显示对应 Tab。


### 📌 接口关联


这个接口和之前抓的 `upstat`、`relation/stat` 配合起来，构成了用户空间顶部的完整数据面板：

| 接口            | 数据                                       |
| --------------- | ------------------------------------------ |
| `upstat`        | 播放数、获赞数                             |
| `relation/stat` | 关注数、粉丝数                             |
| `navnum`        | 各模块内容数量（视频、追番、收藏、相簿等） |
