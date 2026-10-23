# 搜索建议（联想词）

## 接口描述

获取搜索框输入关键词时的联想词建议列表。

> 该接口位于主站 API 域名 `api.bilibili.com`，用于搜索框输入时的自动补全建议。**该接口需要 WBI 签名。**

---

## 接口地址

```
GET https://api.bilibili.com/x/web-interface/suggest
```

- **请求方式**：GET
- **认证方式**：Cookie（需携带 `SESSDATA`）
- **Content-Type**：`application/json`
- **签名方式**：WBI 签名（需携带 `w_rid` 和 `wts` 参数）

---

## 请求参数（URL Query）

| 参数名       | 类型 | 内容           | 必要性   | 备注                                       |
| ------------ | ---- | -------------- | -------- | ------------------------------------------ |
| term         | str  | 搜索关键词     | **必要** | URL 编码，如 `%E6%B4%9B%E5%B0%91%E7%88%B7` |
| highlight    | num  | 是否高亮匹配词 | 非必要   | `0`：不高亮，`1`：高亮（返回带 HTML 标签） |
| spmid        | str  | 来源标识       | 非必要   | 固定传 `0`                                 |
| web_location | str  | 来源标识       | 非必要   | 固定传 `0.0`                               |
| w_rid        | str  | WBI 签名       | **必要** | 见 WBI 签名算法                            |
| wts          | num  | WBI 时间戳     | **必要** | 秒级 Unix 时间戳                           |

**示例请求 URL：**

```
https://api.bilibili.com/x/web-interface/suggest?highlight=0&term=%E6%B4%9B%E5%B0%91%E7%88%B7&spmid=0&web_location=0.0&w_rid=xxx&wts=xxx
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

| 字段        | 类型 | 内容       | 备注                   |
| ----------- | ---- | ---------- | ---------------------- |
| exp_str     | str  | 实验参数   | 用于 AB 测试或实验分流 |
| code        | num  | 内部状态码 | 通常为 0               |
| result      | obj  | 搜索结果   | 包含 `tag` 数组        |
| stoken      | str  | 安全令牌   | 可能用于防爬或后续请求 |
| total_count | num  | 联想词总数 |                        |

### `result` 对象

| 字段 | 类型  | 内容       | 备注                     |
| ---- | ----- | ---------- | ------------------------ |
| tag  | array | 联想词列表 | 每个元素为一个联想词对象 |

### `tag` 数组元素

| 字段  | 类型 | 内容               | 备注               |
| ----- | ---- | ------------------ | ------------------ |
| value | str  | 完整联想词         | 如 `"洛少爷"`      |
| term  | str  | 搜索词             | 与 `value` 相同    |
| ref   | num  | 引用数             | 通常为 0           |
| name  | str  | 带高亮标签的显示名 | 包含 HTML 高亮标签 |
| spid  | num  | 来源标识           | 通常为 5           |
| type  | str  | 类型               | 通常为空字符串     |

---

## 响应示例

```json
{
    "code": 0,
    "message": "OK",
    "ttl": 1,
    "data": {
        "exp_str": "70729101_71714104_72412102_74615102_75178101_75623106_75792106_75857102_76154104",
        "code": 0,
        "result": {
            "tag": [
                {
                    "value": "洛少爷",
                    "term": "洛少爷",
                    "ref": 0,
                    "name": "<em class=\"suggest_high_light\">洛少爷</em>",
                    "spid": 5,
                    "type": ""
                },
                {
                    "value": "洛少爷直播回放",
                    "term": "洛少爷直播回放",
                    "ref": 0,
                    "name": "<em class=\"suggest_high_light\">洛少爷</em>直播回放",
                    "spid": 5,
                    "type": ""
                }
            ]
        },
        "stoken": "3654856653437788650",
        "total_count": 10
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
curl 'https://api.bilibili.com/x/web-interface/suggest?highlight=0&term=%E6%B4%9B%E5%B0%91%E7%88%B7&spmid=0&web_location=0.0&w_rid=xxx&wts=xxx' \
  -H 'Referer: https://www.bilibili.com/' \
  -H 'Origin: https://www.bilibili.com' \
  -b 'SESSDATA=xxx'
```

---

## 注意事项

1. **WBI 签名**：该接口**必须携带 WBI 签名**（`w_rid` 和 `wts`），否则返回 `-400` 错误。
2. **`highlight` 参数**：`1` 时返回的 `name` 字段会包含 `<em class="suggest_high_light">` 标签，用于前端高亮显示匹配词。
3. **`exp_str` 字段**：由多个实验 ID 拼接而成，用于 AB 测试分流。
4. **`stoken` 字段**：可能用于后续搜索请求的安全校验，但具体用途待验证。
5. **联想词数量**：`total_count` 通常为 10，最多返回 10 个联想词。
