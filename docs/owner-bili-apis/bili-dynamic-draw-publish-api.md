# 图文动态发布（带图片）- 完整版

## 接口列表

### 1. 上传图片到 BFS
### 2. 动态发布提交前检查
### 3. 正式发布动态
### 4. 动态更新检查（辅助接口）
### 5. 获取 RSA 公钥（辅助接口）


# 1. 上传图片到 BFS

## 接口描述

将图片上传到 B站 图床（BFS），返回图片 URL 供动态发布使用。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于动态发布前上传图片。

---

## 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`multipart/form-data`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（表单数据 `multipart/form-data`）

| 参数名   | 类型   | 内容               | 必要性   | 备注                               |
| -------- | ------ | ------------------ | -------- | ---------------------------------- |
| file_up  | binary | 图片文件二进制数据 | **必要** | 支持的格式：jpg、png、gif、webp 等 |
| biz      | str    | 业务标识           | **必要** | 固定传 `new_dyn`                   |
| category | str    | 分类               | **必要** | 固定传 `daily`                     |
| csrf     | str    | CSRF Token         | **必要** | 位于 Cookie 中的 `bili_jct` 值     |

**示例请求体（multipart/form-data）：**

```
------WebKitFormBoundaryHgOId40x7m02oEWH
Content-Disposition: form-data; name="file_up"; filename="image.jpg"
Content-Type: image/jpeg

[二进制图片数据]
------WebKitFormBoundaryHgOId40x7m02oEWH
Content-Disposition: form-data; name="biz"

new_dyn
------WebKitFormBoundaryHgOId40x7m02oEWH
Content-Disposition: form-data; name="category"

daily
------WebKitFormBoundaryHgOId40x7m02oEWH
Content-Disposition: form-data; name="csrf"

1eaefa721216ddee6444fcbedace61b2
------WebKitFormBoundaryHgOId40x7m02oEWH--
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

| 字段         | 类型 | 内容             | 备注             |
| ------------ | ---- | ---------------- | ---------------- |
| image_url    | str  | 图片 CDN 地址    | 可访问的图片链接 |
| image_width  | num  | 图片宽度（像素） |                  |
| image_height | num  | 图片高度（像素） |                  |
| img_size     | num  | 图片大小（KB）   |                  |
| ai_gen_pic   | num  | 是否 AI 生成图片 | 0：否，1：是     |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "image_url": "http://i0.hdslb.com/bfs/new_dyn/ba8da16d8fe47b6079b57f3151db8b7e3690995472402999.jpg",
        "image_width": 600,
        "image_height": 600,
        "img_size": 39.233,
        "ai_gen_pic": 0
    }
}
```

---

## 错误码

| 状态码 | 含义                        |
| ------ | --------------------------- |
| 0      | 上传成功                    |
| -101   | 未登录（Cookie 无效或过期） |
| -403   | CSRF 验证失败               |
| -616   | 上传文件不存在              |
| -617   | 上传文件太大                |
| 其他   | 参见 `message` 字段         |

---

## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs' \
  -X POST \
  -H 'Referer: https://t.bilibili.com/' \
  -H 'Origin: https://t.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  -F 'file_up=@/path/to/image.jpg' \
  -F 'biz=new_dyn' \
  -F 'category=daily' \
  -F 'csrf=xxx'
```

---

## 注意事项

1. **图片限制**：单张图片大小建议不超过 10MB，支持 jpg/png/gif/webp 等常见格式。
2. **上传后 URL 有效期**：图片上传后需在短时间内用于发布，否则可能过期。
3. **`biz` 与 `category`**：固定值，不要修改。
4. **响应中的 `image_url`**：使用 `http` 协议，但实际访问时会重定向到 `https`。
5. **BFS 图片格式化**：返回的图片 URL 支持通过后缀参数进行格式化处理（如缩放、转格式等），详见 [`picture.md`](./auth/picture.md)。


# 2. 动态发布提交前检查

## 接口描述

在正式发布动态前，对内容进行合规性检查（敏感词、格式等），通过后方可发布。

> 该接口位于主站 API 域名 `api.bilibili.com`，是动态发布流程的第二步。

---

## 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/create/submit_check
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要（仅需 CSRF）

---

## 请求参数

### URL Query 参数

| 参数名                 | 类型 | 内容         | 必要性   | 备注                                                         |
| ---------------------- | ---- | ------------ | -------- | ------------------------------------------------------------ |
| csrf                   | str  | CSRF Token   | **必要** | 位于 Cookie 中的 `bili_jct` 值                               |
| x-bili-device-req-json | str  | 设备请求信息 | 非必要   | URL 编码的 JSON，如 `%7B%22platform%22:%22web%22%2C%22device%22:%22pc%22%2C%22spmid%22:%220.0%22%7D` |

### 请求体参数（JSON）

| 参数名        | 类型  | 内容     | 必要性   | 备注                                  |
| ------------- | ----- | -------- | -------- | ------------------------------------- |
| content       | obj   | 动态内容 | **必要** | 与发布接口 `dyn_req.content` 结构相同 |
| create_option | obj   | 创建选项 | 非必要   | 包含 `aigc`、`pic_mode`               |
| pics          | array | 图片列表 | **必要** | 上传图片后返回的 URL 信息             |
| scene         | num   | 发布场景 | **必要** | `2`：普通发布                         |
| attach_card   | null  | 附加卡片 | 非必要   | 固定传 `null`                         |

### `content` 对象

| 字段     | 类型  | 内容         | 备注                   |
| -------- | ----- | ------------ | ---------------------- |
| contents | array | 内容节点列表 | 每个元素为一个内容节点 |
| title    | str   | 动态标题     | 可选，可为空字符串     |

### `contents` 数组元素

| 字段     | 类型 | 内容       | 备注           |
| -------- | ---- | ---------- | -------------- |
| raw_text | str  | 纯文本内容 | 动态正文       |
| type     | num  | 内容类型   | `1`：文本      |
| biz_id   | str  | 业务 ID    | 通常为空字符串 |

### `create_option` 对象

| 字段     | 类型 | 内容        | 备注                                   |
| -------- | ---- | ----------- | -------------------------------------- |
| aigc     | num  | AI 生成标识 | `0`：非 AI，`1`：AI 生成，`2`：AI 辅助 |
| pic_mode | num  | 图片模式    | `0`：普通图片                          |

### `pics` 数组元素

| 字段       | 类型 | 内容           | 备注                           |
| ---------- | ---- | -------------- | ------------------------------ |
| img_src    | str  | 图片 URL       | 上传图片接口返回的 `image_url` |
| img_width  | num  | 图片宽度       |                                |
| img_height | num  | 图片高度       |                                |
| img_size   | num  | 图片大小（KB） |                                |
| ai_gen_pic | num  | 是否 AI 生成   | 0：否                          |

---

## 请求示例（JSON Body）

```json
{
    "content": {
        "contents": [
            {
                "raw_text": "Have not something.",
                "type": 1,
                "biz_id": ""
            }
        ],
        "title": "None"
    },
    "create_option": {
        "aigc": 2,
        "pic_mode": 0
    },
    "pics": [
        {
            "img_src": "http://i0.hdslb.com/bfs/new_dyn/xxx.jpg",
            "img_width": 600,
            "img_height": 600,
            "img_size": 38.3134765625,
            "ai_gen_pic": 0
        }
    ],
    "scene": 2,
    "attach_card": null
}
```

---

## 响应结构

### 根对象

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示通过 |
| message | str  | 状态信息 | `"OK"`     |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 | 空对象     |

**响应示例（通过）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {}
}
```

---

## 错误码

| 状态码 | 含义                                  |
| ------ | ------------------------------------- |
| 0      | 检查通过                              |
| -101   | 未登录（Cookie 无效或过期）           |
| -111   | CSRF 校验失败                         |
| -403   | 风控拦截                              |
| 其他   | 参见 `message` 字段，可能为敏感词提示 |


# 3. 正式发布动态

## 接口描述

正式发布图文动态到 B站 动态流中，需携带 WBI 签名和风控参数。

> 该接口位于主站 API 域名 `api.bilibili.com`，是动态发布流程的第三步。**该接口需要 WBI 签名和 CSRF 双重认证。**

---

## 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/create/dyn
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）+ CSRF

---

## 请求参数

### URL Query 参数

| 参数名                 | 类型 | 内容                   | 必要性     | 备注                                                         |
| ---------------------- | ---- | ---------------------- | ---------- | ------------------------------------------------------------ |
| platform               | str  | 平台标识               | 非必要     | 固定传 `web`                                                 |
| csrf                   | str  | CSRF Token             | **必要**   | 位于 Cookie 中的 `bili_jct` 值                               |
| b_wet                  | str  | 风控参数               | **必要**   | RSA 加密的防重放/安全校验数据，格式为 `{加密数据}.{签名}.v1` |
| x-bili-device-req-json | str  | 设备请求信息           | 非必要     | URL 编码的 JSON                                              |
| dm_img_list            | str  | 风控参数（鼠标轨迹）   | ⚠️ 风控要求 | JSON 数组字符串，详见下方说明                                |
| dm_img_str             | str  | 风控参数（GPU 信息）   | ⚠️ 风控要求 | Base64 编码，详见下方说明                                    |
| dm_cover_img_str       | str  | 风控参数（渲染器信息） | ⚠️ 风控要求 | Base64 编码，详见下方说明                                    |
| dm_img_inter           | str  | 风控参数（交互信息）   | ⚠️ 风控要求 | JSON 字符串，详见下方说明                                    |
| w_dyn_req.upload_id    | str  | 上传 ID                | 非必要     | 格式 `{mid}_{timestamp}_{随机数}`                            |
| w_dyn_req.meta         | str  | 元数据                 | 非必要     | URL 编码的 JSON，包含 `app_meta`                             |
| w_rid                  | str  | WBI 签名               | **必要**   | 见 [WBI 签名算法](./auth/sign/wbi.md)                        |
| wts                    | num  | WBI 时间戳             | **必要**   | 秒级 Unix 时间戳                                             |

### 请求体参数（JSON）

| 参数名  | 类型 | 内容         | 必要性   | 备注             |
| ------- | ---- | ------------ | -------- | ---------------- |
| dyn_req | obj  | 动态请求数据 | **必要** | 包含完整动态内容 |

### `dyn_req` 对象

| 字段        | 类型  | 内容     | 备注                                |
| ----------- | ----- | -------- | ----------------------------------- |
| content     | obj   | 动态内容 | 与提交检查接口的 `content` 结构相同 |
| scene       | num   | 发布场景 | `2`：普通发布                       |
| attach_card | null  | 附加卡片 | 固定传 `null`                       |
| upload_id   | str   | 上传 ID  | 格式 `{mid}_{timestamp}_{随机数}`   |
| meta        | obj   | 元数据   | 包含 `app_meta`                     |
| option      | obj   | 发布选项 | 包含 `aigc`、`pic_mode`             |
| pics        | array | 图片列表 | 与提交检查接口的 `pics` 结构相同    |

---

## 请求示例（JSON Body）

```json
{
    "dyn_req": {
        "content": {
            "contents": [
                {
                    "raw_text": "Have not something.",
                    "type": 1,
                    "biz_id": ""
                }
            ],
            "title": "None"
        },
        "scene": 2,
        "attach_card": null,
        "upload_id": "3690995472402999_1783894822_3886",
        "meta": {
            "app_meta": {
                "from": "create.dynamic.web",
                "mobi_app": "web"
            }
        },
        "option": {
            "aigc": 2,
            "pic_mode": 0
        },
        "pics": [
            {
                "img_src": "http://i0.hdslb.com/bfs/new_dyn/ba8da16d8fe47b6079b57f3151db8b7e3690995472402999.jpg",
                "img_width": 600,
                "img_height": 600,
                "img_size": 38.3134765625,
                "ai_gen_pic": 0
            }
        ]
    }
}
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

| 字段       | 类型 | 内容              | 备注                         |
| ---------- | ---- | ----------------- | ---------------------------- |
| dyn_id     | num  | 动态 ID（数字）   | 全局唯一标识                 |
| dyn_id_str | str  | 动态 ID（字符串） | 与 `dyn_id` 相同，字符串格式 |
| dyn_type   | num  | 动态类型          | `2`：图文动态                |
| dyn_rid    | num  | 动态资源 ID       | 指向具体内容资源             |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "dyn_id": 1224311768130519040,
        "dyn_id_str": "1224311768130519040",
        "dyn_type": 2,
        "dyn_rid": 401540082
    }
}
```

---

## 错误码

| 状态码 | 含义                                 |
| ------ | ------------------------------------ |
| 0      | 发布成功                             |
| -101   | 未登录（Cookie 无效或过期）          |
| -111   | CSRF 校验失败                        |
| -400   | WBI 签名缺失或错误                   |
| -403   | 风控拦截                             |
| -412   | 请求被拦截（客户端 IP 被服务端风控） |
| -799   | 请求过于频繁，请稍后再试             |
| 其他   | 参见 `message` 字段                  |


# 4. 动态更新检查（辅助接口）

## 接口描述

检查动态首页是否有新内容更新，用于发布后刷新动态流。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于动态流更新轮询。

---

## 接口地址

```
GET https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all/update
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数（URL Query）

| 参数名          | 类型 | 内容     | 必要性 | 备注               |
| --------------- | ---- | -------- | ------ | ------------------ |
| type            | str  | 更新类型 | 非必要 | 固定传 `all`       |
| update_baseline | str  | 基线 ID  | 非必要 | 从动态首页接口获取 |
| web_location    | str  | 来源标识 | 非必要 | 固定传 `0.0`       |

---

## 响应结构

| 字段            | 类型 | 内容     | 备注           |
| --------------- | ---- | -------- | -------------- |
| code            | num  | 状态码   | 0 表示成功     |
| message         | str  | 状态信息 | `"0"`          |
| ttl             | num  | 1        |                |
| data            | obj  | 数据本体 |                |
| data.update_num | num  | 更新数量 | 0 表示无新内容 |

**响应示例：**

```json
{
    "code": 0,
    "message": "0",
    "data": {
        "update_num": 0
    },
    "ttl": 1
}
```

---

## 注意事项

1. **该接口为辅助接口**：主要用于前端轮询检查动态流是否有更新，不是发布流程的必要步骤。
2. **`update_num`**：大于 0 表示有新动态内容可刷新。


# 5. 获取 RSA 公钥（辅助接口）

## 接口描述

获取用于 `b_wet` 参数加密的 RSA 公钥。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于动态发布时获取加密公钥。

---

## 接口地址

```
GET https://api.bilibili.com/x/internal/gaia-gateway/ExGetAxe
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **是否需要 WBI 签名**：❌ 不需要

---

## 请求参数

无请求参数。

---

## 响应结构

| 字段    | 类型 | 内容     | 备注       |
| ------- | ---- | -------- | ---------- |
| code    | num  | 状态码   | 0 表示成功 |
| message | str  | 状态信息 | `"0"`      |
| ttl     | num  | 1        |            |
| data    | obj  | 数据本体 |            |

### `data` 对象

| 字段       | 类型 | 内容                 | 备注                  |
| ---------- | ---- | -------------------- | --------------------- |
| version    | str  | 密钥版本             | `"v1"`                |
| public_key | str  | RSA 公钥（PEM 格式） | 用于加密 `b_wet` 参数 |
| deadline   | num  | 密钥过期时间戳       | Unix 时间戳（秒）     |

---

## 响应示例

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "version": "v1",
        "public_key": "-----BEGIN rsa public key-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1SomDTbicibEZdRNTFIf\nG0MZI9Vm+VLvXvoS6YGtHkMexd+O8ImALMxiMkydZ0h5XPPfiUXGiyfWawVW1Q6Q\nL8E9HV8tXgI82zMc/2ZnAyAp5dACWfcsqF1lH4hh63W424c9EJ/Ryqk4ZFss+vDr\nn33+FN1LOyJtg8nPqCt9DN9PFaRvJTEXT0Bt2ZQTiSznHPIpalgHUNsg1OPV3ou9\n5ahf5CpRl89QeIptrbObEqsmRqC0rDwsMUhY1NnvPKGYnCqOWl006q6OBP77qHa9\nHRLZS0EuCEuLUnKRQq2vbbpqKrgIQln+HjMy4oIjV7Bdv9e6SJSxwausegaCQ+pt\nIzy6O41iIQSISCRf+2iywvKGxvi3Jhhc39GxvhBPl9W3QF4knJmWHHbqAb94mDNE\nT0GzjbU6c3j7FJcC2JjK7PeC44+VSyiY7N+9Dc0ulw7OIoigPl+R6zyWEPCdKems\n9Cd8vn/njM+o7BRaBzyqJSYSOjQQiQHJYzcMRhhue/2W1wSx2S9Ry/zNvpP/Qapw\n4Z6IlDt+wL9omIwcFMndUruAaRKQEDgDRKZHspUIRkXhCiaV4MwUH1rF6EFq8BRc\nIsoS5O0o8ew5mzW81q2I1Mkvx2wDRyX9+zlVBMkKAvv3xMzU5l7sUM1eP3tw3mhg\n6D6utwZfuFFb7Zj1oGJq4VMCAwEAAQ==\n-----END rsa public key-----",
        "deadline": 2524608000
    }
}
```


## 完整发布流程图

```
┌─────────────────────────────────────────────────────────────────────┐
│                       图文动态发布完整流程                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐                                              │
│  │ 0. 获取 RSA 公钥  │ (可选) GET /x/internal/gaia-gateway/ExGetAxe │
│  │                  │ → 用于生成 b_wet 参数                        │
│  └────────┬─────────┘                                              │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                              │
│  │ 1. 上传图片       │ POST /x/dynamic/feed/draw/upload_bfs       │
│  │                  │ → 返回 image_url, width, height, size       │
│  └────────┬─────────┘                                              │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                              │
│  │ 2. 提交检查       │ POST /x/dynamic/feed/create/submit_check   │
│  │                  │ → 验证内容合规性 (无需 WBI 签名)             │
│  └────────┬─────────┘                                              │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                              │
│  │ 3. 正式发布       │ POST /x/dynamic/feed/create/dyn            │
│  │                  │ → 返回 dyn_id, dyn_id_str, dyn_rid          │
│  └──────────────────┘                                              │
│                                                                     │
│  📌 第 3 步需要:                                                   │
│     ① WBI 签名 (w_rid + wts)                                      │
│     ② CSRF Token (csrf)                                           │
│     ③ 风控参数 (dm_img_list, dm_img_str, dm_cover_img_str, dm_img_inter) │
│     ④ RSA 加密参数 (b_wet)                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```


# 认证与签名补充说明

## WBI 签名

该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。WBI 签名算法详见 [`wbi.md`](./auth/sign/wbi.md)。

**简要流程：**

1. 从导航接口 `/x/web-interface/nav` 获取 `wbi_img.img_url` 和 `wbi_img.sub_url`
2. 提取文件名作为 `img_key` 和 `sub_key`（如 `7cd084941338484aae1ad9425b84077c`）
3. 将 `sub_key` 拼接在 `img_key` 后面，通过重排映射表 `MIXIN_KEY_ENC_TAB` 打乱并截取前 32 位，得到 `mixin_key`
4. 向请求参数中添加 `wts`（当前秒级时间戳），按键名升序排序后编码为 URL Query
5. 拼接 `mixin_key` 后计算 MD5，得到 `w_rid`

```python
# Python 示例（核心部分）
def get_mixin_key(orig: str) -> str:
    mixin_key_enc_tab = [46, 47, 18, 2, 53, 8, ...]  # 完整表见 wbi.md
    return ''.join(orig[i] for i in mixin_key_enc_tab)[:32]

def enc_wbi(params: dict, img_key: str, sub_key: str) -> dict:
    mixin_key = get_mixin_key(img_key + sub_key)
    params['wts'] = int(time.time())
    params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(params)
    params['w_rid'] = hashlib.md5((query + mixin_key).encode()).hexdigest()
    return params
```

## `b_wet` 参数生成说明

`b_wet` 参数格式为 `{加密数据}.{签名}.v1`，基于 RSA 公钥加密：

1. 调用 `/x/internal/gaia-gateway/ExGetAxe` 获取 RSA 公钥（PEM 格式）
2. 将需要加密的数据（可能包含时间戳、用户标识、随机数等）用公钥加密
3. 使用 `bili_jct` 或 `SESSDATA` 对加密数据进行签名
4. 拼接为 `{加密数据(base64)}.{签名}.v1`

> **注意**：具体加密和签名算法仍需逆向分析，建议直接从浏览器抓包复制完整 `b_wet` 值使用，或参考 `bili_ticket.md` 中的生成思路。

## 风控参数说明

| 参数名             | 内容                     | 来源                         |
| ------------------ | ------------------------ | ---------------------------- |
| `dm_img_list`      | 鼠标轨迹坐标数组         | 页面鼠标事件采集             |
| `dm_img_str`       | GPU/WebGL 信息（Base64） | `WebGLRenderingContext` 采集 |
| `dm_cover_img_str` | 渲染器驱动信息（Base64） | 浏览器渲染器信息             |
| `dm_img_inter`     | 页面交互元素信息（JSON） | DOM 交互采集                 |

这些参数**难以在纯后端模拟**，建议从真实浏览器环境采集后传递。

## 公共错误码参考

详见 [`errcode.md`](./auth/errcode.md)。

| 错误码 | 含义                                 |
| ------ | ------------------------------------ |
| -101   | 账号未登录                           |
| -111   | CSRF 校验失败                        |
| -400   | 请求错误 / WBI 签名缺失或错误        |
| -403   | 访问权限不足 / 风控拦截              |
| -412   | 请求被拦截（客户端 IP 被服务端风控） |
| -799   | 请求过于频繁，请稍后再试             |


## 📂 动态模块文件清单

| 文件                                   | 内容                                 |
| -------------------------------------- | ------------------------------------ |
| `bili-dynamic-feed-api.md`             | 动态首页推荐流                       |
| `bili-article-list-api.md`             | 图文动态列表（专栏）                 |
| `bili-space-dynamic-feed-api.md`       | 用户空间动态列表                     |
| `bili-dynamic-publish-api.md`          | 动态发布（纯文本）                   |
| **`bili-dynamic-draw-publish-api.md`** | **图文动态发布（带图片，本次新增）** |
| `bili-dynamic-delete-api.md`           | 动态删除                             |
| `bili-dynamic-thumb-api.md`            | 动态点赞/取消点赞                    |
