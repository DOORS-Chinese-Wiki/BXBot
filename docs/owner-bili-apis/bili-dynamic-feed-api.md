# 动态首页推荐流

## 接口描述

获取 B站 动态首页（关注/推荐）的 Feed 流内容，包含视频、专栏、图文等多种类型。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于动态首页（`/dynamic`）的 Feed 流展示。

---

## 接口地址

```
GET https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/nav
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容        | 必要性 | 备注                                                         |
| --------------- | ---- | ----------- | ------ | ------------------------------------------------------------ |
| update_baseline | str  | 更新基线 ID | 非必要 | 首次请求可不传或传特定值，后续使用响应中的 `update_baseline` |
| offset          | str  | 翻页偏移量  | 非必要 | 首次请求为空，后续使用响应中的 `offset`                      |
| web_location    | str  | 来源标识    | 非必要 | 固定传 `0.0`                                                 |

**示例请求 URL：**

```
https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/nav?update_baseline=1223979814373818368&offset=&web_location=0.0
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 |            |

### `data` 对象

| 字段            | 类型  | 内容              | 备注                   |
| --------------- | ----- | ----------------- | ---------------------- |
| items           | array | Feed 流条目列表   | 每个元素为一个动态卡片 |
| update_num      | str   | 更新数量          |                        |
| update_baseline | str   | 下次请求的基线 ID |                        |
| offset          | str   | 下次请求的偏移量  |                        |
| has_more        | bool  | 是否有更多数据    | `true`：有下一页       |

### `items` 数组元素

| 字段       | 类型     | 内容              | 备注                                          |
| ---------- | -------- | ----------------- | --------------------------------------------- |
| id_str     | str      | 动态 ID（字符串） |                                               |
| author     | obj      | 发布者信息        |                                               |
| icon_badge | null/obj | 图标徽章          | 通常为 null                                   |
| pub_time   | str      | 发布时间描述      | 如 `"2小时前"`、`"昨天 13:50"`                |
| type       | num      | 内容类型          | `8`：视频，`64`：专栏/文章                    |
| rid        | str      | 资源 ID           | 视频的 `aid` 或专栏的 `id`                    |
| title      | str      | 标题              |                                               |
| cover      | str      | 封面图地址        |                                               |
| jump_url   | str      | 跳转链接          | 相对路径，如 `//www.bilibili.com/video/BVxxx` |
| visible    | bool     | 是否可见          |                                               |
| fold       | null     | 折叠状态          | 通常为 null                                   |

### `author` 对象

| 字段     | 类型 | 内容             | 备注     |
| -------- | ---- | ---------------- | -------- |
| mid      | str  | 用户 UID         |          |
| name     | str  | 用户昵称         |          |
| face     | str  | 头像地址         |          |
| jump_url | str  | 用户空间跳转链接 | 相对路径 |
| vip      | obj  | 大会员信息       |          |
| official | obj  | 官方认证信息     |          |

---

## 翻页说明

该接口使用 **基线游标分页**：

1. **首次请求**：`update_baseline` 可传空字符串，`offset` 传空字符串
2. **后续请求**：使用响应中 `update_baseline` 和 `offset` 作为下一次请求的参数
3. **最后一页**：`has_more` 为 `false`

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
curl 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/nav?update_baseline=&offset=&web_location=0.0' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **无需 WBI 签名**：该接口不需要 WBI 签名。
2. **`type` 含义**：
   - `8`：视频动态
   - `64`：专栏/文章动态
3. **`jump_url` 为相对路径**：需要拼接 `https://www.bilibili.com` 使用。
4. **`pub_time` 为展示文本**：已经是格式化好的时间描述，不提供原始时间戳。
