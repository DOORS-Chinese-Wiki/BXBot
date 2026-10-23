# 排行榜

## 接口描述

获取 B站 全站或各分区的排行榜视频列表，按综合数据排序。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于排行榜页面展示。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/web-interface/ranking/v2
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容          | 必要性   | 备注                          |
| ------------ | ---- | ------------- | -------- | ----------------------------- |
| rid          | num  | 排行榜分区 ID | 非必要   | `0`：全站，其他值见分区代码表 |
| type         | str  | 排行榜类型    | 非必要   | `all`：全部                   |
| web_location | str  | 来源标识      | 非必要   | 固定传 `333.934` 或类似值     |
| w_rid        | str  | WBI 签名      | **必要** | 见 WBI 签名算法               |
| wts          | num  | WBI 时间戳    | **必要** | 秒级 Unix 时间戳              |

**示例请求 URL：**

```
https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all&web_location=333.934&w_rid=xxx&wts=xxx
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

| 字段 | 类型  | 内容           | 备注                                                  |
| ---- | ----- | -------------- | ----------------------------------------------------- |
| note | str   | 排行榜说明文案 | 如 `"根据稿件内容质量、近期的数据综合展示，动态更新"` |
| list | array | 排行榜视频列表 | 每个元素为一个视频对象                                |

### `list` 数组元素

| 字段          | 类型  | 内容               | 备注                                    |
| ------------- | ----- | ------------------ | --------------------------------------- |
| aid           | num   | 视频 AV ID         |                                         |
| bvid          | str   | 视频 BV ID         |                                         |
| title         | str   | 视频标题           |                                         |
| pic           | str   | 封面图地址         |                                         |
| pubdate       | num   | 发布时间戳         | Unix 时间戳（秒）                       |
| ctime         | num   | 创建时间戳         | Unix 时间戳（秒）                       |
| duration      | num   | 视频时长（秒）     |                                         |
| videos        | num   | 分 P 数量          |                                         |
| tid           | num   | 分区 ID            |                                         |
| tname         | str   | 分区名称           | 如 `"日常"`、`"手机游戏"`               |
| copyright     | num   | 版权类型           | `1`：原创，`2`：转载，`3`：转载（其他） |
| desc          | str   | 视频简介           |                                         |
| state         | num   | 视频状态           |                                         |
| mission_id    | num   | 活动 ID            | 0 表示无                                |
| rights        | obj   | 权限信息           |                                         |
| owner         | obj   | UP 主信息          | 包含 `mid`、`name`、`face`              |
| stat          | obj   | 统计数据           |                                         |
| dimension     | obj   | 视频尺寸信息       |                                         |
| short_link_v2 | str   | 短链接             | 如 `https://b23.tv/BVxxx`               |
| first_frame   | str   | 首帧图片地址       |                                         |
| pub_location  | str   | 发布地点           | 如 `"上海"`                             |
| cover43       | str   | 封面图（4:3 裁剪） |                                         |
| tidv2         | num   | 新版分区 ID        |                                         |
| tnamev2       | str   | 新版分区名称       | 如 `"UP主小综艺"`                       |
| pid_v2        | num   | 新版父级分区 ID    |                                         |
| pid_name_v2   | str   | 新版父级分区名称   | 如 `"小剧场"`                           |
| attribute_v3  | num   | 属性位 V3          |                                         |
| score         | num   | 排行榜得分         | 综合排序依据                            |
| enable_vt     | num   | 是否启用 VT        |                                         |
| his_rank      | num   | 历史最高排名       |                                         |
| now_rank      | num   | 当前排名           | 0 表示未上榜                            |
| others        | array | 同系列其他视频     | 部分视频包含                            |

### `stat` 对象

| 字段     | 类型 | 内容               | 备注 |
| -------- | ---- | ------------------ | ---- |
| view     | num  | 播放量             |      |
| danmaku  | num  | 弹幕数             |      |
| reply    | num  | 评论数             |      |
| favorite | num  | 收藏数             |      |
| coin     | num  | 投币数             |      |
| share    | num  | 分享数             |      |
| like     | num  | 点赞数             |      |
| dislike  | num  | 踩数               |      |
| his_rank | num  | 历史最高排名       |      |
| now_rank | num  | 当前排名           |      |
| vt       | num  | 视频类型           |      |
| vv       | num  | 播放量（别名）     |      |
| fav_g    | num  | 收藏数（游戏相关） |      |
| like_g   | num  | 点赞数（游戏相关） |      |

### `rights` 对象

| 字段           | 类型 | 内容           | 备注 |
| -------------- | ---- | -------------- | ---- |
| bp             | num  | 是否大会员专享 |      |
| elec           | num  | 是否充电专享   |      |
| download       | num  | 是否可下载     |      |
| movie          | num  | 是否电影       |      |
| pay            | num  | 是否付费       |      |
| hd5            | num  | 是否高清       |      |
| no_reprint     | num  | 是否禁止转载   |      |
| autoplay       | num  | 是否自动播放   |      |
| ugc_pay        | num  | 是否 UGC 付费  |      |
| is_cooperation | num  | 是否联合投稿   |      |
| arc_pay        | num  | 是否稿件付费   |      |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "note": "根据稿件内容质量、近期的数据综合展示，动态更新",
        "list": [
            {
                "aid": 116890622036439,
                "bvid": "BV1UjMn6hEXQ",
                "title": "《下一个是谁》第七季（1）",
                "pic": "http://i2.hdslb.com/bfs/archive/xxx.jpg",
                "pubdate": 1783656000,
                "duration": 5278,
                "owner": {
                    "mid": 147166910,
                    "name": "雨哥到处跑",
                    "face": "https://i2.hdslb.com/bfs/face/xxx.jpg"
                },
                "stat": {
                    "view": 3374830,
                    "danmaku": 140245,
                    "reply": 33372,
                    "favorite": 169463,
                    "coin": 530406,
                    "share": 29439,
                    "like": 432798
                },
                "his_rank": 1,
                "short_link_v2": "https://b23.tv/BV1UjMn6hEXQ"
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
| -400   | WBI 签名缺失或错误          |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all&web_location=333.934&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://www.bilibili.com/v/popular/rank/all' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`rid` 参数**：`0` 表示全站排行榜，其他分区 ID 可参考视频分区代码表。
3. **`his_rank`**：历史最高排名，`1` 表示曾登顶。
4. **`stat` 中的播放量**：`view` 和 `vv` 通常相同，均为播放量。
5. **榜单动态更新**：排行榜数据会动态变化，不同时间请求返回结果不同。
