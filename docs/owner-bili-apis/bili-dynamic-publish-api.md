# 动态发布

## 接口描述

发布图文动态到 B站 动态流中。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于创作中心动态发布功能。**该接口需要 WBI 签名和 CSRF 双重认证。**

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

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| platform | str | 平台标识 | 非必要 | 固定传 `web` |
| csrf | str | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` 值 |
| b_wet | str | 风控参数 | 非必要 | 编码数据，用于防重放或安全校验 |
| x-bili-device-req-json | str | 设备请求信息 | 非必要 | URL 编码的 JSON，包含 `platform`、`device`、`spmid` |
| dm_img_list | str | 风控参数（鼠标轨迹） | ⚠️ 风控要求 | JSON 数组字符串 |
| dm_img_str | str | 风控参数（GPU 信息） | ⚠️ 风控要求 | Base64 编码 |
| dm_cover_img_str | str | 风控参数（渲染器信息） | ⚠️ 风控要求 | Base64 编码 |
| dm_img_inter | str | 风控参数（交互信息） | ⚠️ 风控要求 | JSON 字符串 |
| w_dyn_req.upload_id | str | 上传 ID | 非必要 | 格式 `{mid}_{timestamp}_{随机数}` |
| w_dyn_req.meta | str | 元数据 | 非必要 | URL 编码的 JSON，包含 `app_meta` |
| w_rid | str | WBI 签名 | **必要** | 见 WBI 签名算法 |
| wts | num | WBI 时间戳 | **必要** | 秒级 Unix 时间戳 |

### 请求体参数（JSON）

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| dyn_req | obj | 动态请求数据 | **必要** | 包含 `content`、`scene`、`attach_card`、`upload_id` 等 |

### `dyn_req` 对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| content | obj | 动态内容 | 包含 `contents`、`title` 等 |
| scene | num | 发布场景 | `2`：普通发布 |
| attach_card | null | 附加卡片 | 通常为 `null` |
| upload_id | str | 上传 ID | 格式 `{mid}_{timestamp}_{随机数}` |
| meta | obj | 元数据 | 包含 `app_meta` |
| option | obj | 发布选项 | 包含 `aigc`、`private_pub`、`up_choose_comment` |

### `content` 对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| contents | array | 内容节点列表 | 每个元素为一个内容节点 |
| title | str | 动态标题 | 可选 |

### `contents` 数组元素

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| raw_text | str | 纯文本内容 | 动态正文 |
| type | num | 内容类型 | `1`：文本 |
| biz_id | str | 业务 ID | 通常为空字符串 |

### `meta` 对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| app_meta | obj | 应用元数据 | 包含 `from`、`mobi_app` |

### `option` 对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| aigc | num | 是否 AI 生成 | `1`：是，`0`：否 |
| private_pub | num | 是否仅自己可见 | `1`：是，`0`：否 |
| up_choose_comment | num | 是否开启精选评论 | `1`：开启 |

**示例请求体：**

```json
{
    "dyn_req": {
        "content": {
            "contents": [
                {
                    "raw_text": "Here can write something.",
                    "type": 1,
                    "biz_id": ""
                }
            ],
            "title": "Title-Title"
        },
        "scene": 2,
        "attach_card": null,
        "upload_id": "3690995472402999_1783735062_7788",
        "meta": {
            "app_meta": {
                "from": "create.dynamic.web",
                "mobi_app": "web"
            }
        },
        "option": {
            "aigc": 1,
            "private_pub": 1,
            "up_choose_comment": 1
        }
    }
}
```

---

## 响应结构

### 根对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| code | num | 状态码 | 0 表示成功 |
| message | str | 状态信息 | `"OK"` |
| ttl | num | 1 | |
| data | obj | 数据本体 | |

### `data` 对象

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| dyn_id | num | 动态 ID（数字） | 全局唯一标识 |
| dyn_id_str | str | 动态 ID（字符串） | 与 `dyn_id` 相同，字符串格式 |
| dyn_type | num | 动态类型 | `2`：图文动态 |
| dyn_rid | num | 动态资源 ID | 可能指向具体内容资源 |

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "dyn_id": 1224308010054058001,
        "dyn_id_str": "1224308010054058001",
        "dyn_type": 2,
        "dyn_rid": 401538909
    }
}
```

---

## 提交前检查

### 接口地址

```
POST https://api.bilibili.com/x/dynamic/feed/create/submit_check
```

- **请求方式**：POST
- **认证方式**：Cookie（需携带 `SESSDATA` 和 `bili_jct`）
- **Content-Type**：`application/json`
- **签名方式**：❌ 不需要 WBI 签名，仅需 CSRF

### URL Query 参数

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| csrf | str | CSRF Token | **必要** | 位于 Cookie 中的 `bili_jct` |
| x-bili-device-req-json | str | 设备请求信息 | 非必要 | URL 编码的 JSON |

### 请求体参数

与发布接口的 `dyn_req` 结构一致（不含 `upload_id`、`meta` 等额外字段），但 URL Query 中无需携带 WBI 签名。

**示例请求体：**

```json
{
    "content": {
        "contents": [
            {
                "raw_text": "Hello B站！",
                "type": 1,
                "biz_id": ""
            }
        ],
        "title": ""
    },
    "scene": 2,
    "attach_card": null,
    "option": {
        "aigc": 0,
        "private_pub": 0,
        "up_choose_comment": 1
    }
}
```

**响应示例（成功）：**

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "pass": true
    }
}
```

> **说明**：该接口用于提交前检查内容是否符合发布规范，`pass: true` 表示通过。


## 错误码

| 状态码 | 含义 |
| ------ | ---- |
| 0 | 操作成功 |
| -101 | 未登录（Cookie 无效或过期） |
| -111 | CSRF 校验失败（`bili_jct` 不匹配或过期） |
| -400 | WBI 签名缺失或错误 |
| -403 | 风控拦截 |
| 其他 | 参见 `message` 字段 |


## 调用示例（curl）

```bash
curl 'https://api.bilibili.com/x/dynamic/feed/create/dyn?platform=web&csrf=xxx&b_wet=xxx&x-bili-device-req-json=%7B%22platform%22:%22web%22%7D&dm_img_list=[]&dm_img_str=xxx&dm_cover_img_str=xxx&dm_img_inter=%7B%7D&w_dyn_req.upload_id=xxx&w_dyn_req.meta=%7B%22app_meta%22:%7B%22from%22:%22create.dynamic.web%22%7D%7D&w_rid=xxx&wts=xxx' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://t.bilibili.com/' \
  -H 'Origin: https://t.bilibili.com' \
  -b 'SESSDATA=xxx; bili_jct=xxx' \
  --data-raw '{
    "dyn_req": {
        "content": {
            "contents": [
                {
                    "raw_text": "Hello B站！",
                    "type": 1,
                    "biz_id": ""
                }
            ],
            "title": ""
        },
        "scene": 2,
        "attach_card": null,
        "upload_id": "123456789_1234567890_1234",
        "meta": {
            "app_meta": {
                "from": "create.dynamic.web",
                "mobi_app": "web"
            }
        },
        "option": {
            "aigc": 0,
            "private_pub": 0,
            "up_choose_comment": 1
        }
    }
  }'
```


## 注意事项

1. **WBI 签名**：发布接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **CSRF 双重校验**：需同时携带 Cookie 中的 `bili_jct` 和 URL 参数中的 `csrf`，两者值一致。
3. **风控参数**：`dm_img_list`、`dm_img_str`、`dm_cover_img_str`、`dm_img_inter` 为设备指纹/行为采集参数，缺失可能导致 `-403` 风控拦截。
4. **`b_wet` 参数**：推测为防重放或安全校验参数，具体生成方式待补充。
5. **`upload_id` 格式**：`{mid}_{timestamp}_{随机数}`，`timestamp` 可能为秒级或毫秒级。
6. **两步流程**：
   - 先调用 `/submit_check` 进行内容检查（无 WBI 签名）
   - 通过后再调用 `/create/dyn` 正式发布（需 WBI 签名）
7. **`private_pub` 选项**：`1` 表示仅自己可见，适合测试或私密动态。
8. **动态访问 URL**：发布成功后，可通过 `https://t.bilibili.com/{dyn_id_str}` 访问该动态（仅自己可见时需登录）。



### 📂 动态模块文件清单

| 文件 | 内容 |
| ---- | ---- |
| `bili-dynamic-feed-api.md` | 动态首页推荐流 |
| `bili-article-list-api.md` | 图文动态列表（专栏） |
| `bili-space-dynamic-feed-api.md` | 用户空间动态列表 |
| **`bili-dynamic-publish-api.md`** | **动态发布（新增）** |