# 大会员兑换码

## 获取验证码

> https://api.bilibili.com/x/vip/code/verify

*请求方式：GET*

认证方式：Cookie（SESSDATA）

**url参数：**

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| t | num | 当前时间戳 | 必要 | 毫秒级 |
| web_location | str | 来源标识 | 非必要 | 默认为 `0.0` |

**json回复：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| code | num | 返回值 | 0：成功<br />-101：未登录 |
| message | str | 错误信息 | 默认为0 |
| ttl | num | 1 | |
| data | obj | 信息本体 | |

`data`对象：

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| token | str | 验证码令牌 | 用于获取验证码图片及兑换 |
| url | str | 验证码图片地址 | |

**示例：**

```shell
curl -G 'https://api.bilibili.com/x/vip/code/verify' \
    --data-urlencode 't=1783048944958' \
    --data-urlencode 'web_location=0.0' \
    -b 'SESSDATA=xxx'
```

<details>
<summary>查看响应示例：</summary>

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "token": "b301ed1280d648de8b81830d8fe4e4c5",
        "url": "https://api.bilibili.com/x/v1/captcha/get?bid=account&token=b301ed1280d648de8b81830d8fe4e4c5"
    }
}
```

</details>

## 获取验证码图片

> https://api.bilibili.com/x/v1/captcha/get

*请求方式：GET*

**url参数：**

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| bid | str | 业务标识 | 必要 | 固定为 `account` |
| token | str | 验证码令牌 | 必要 | 从 `verify` 接口获取 |

**返回：**

返回图片二进制数据（PNG格式），可直接显示或保存为图片文件。

**示例：**

```shell
curl -G 'https://api.bilibili.com/x/v1/captcha/get' \
    --data-urlencode 'bid=account' \
    --data-urlencode 'token=b301ed1280d648de8b81830d8fe4e4c5' \
    -o captcha.png
```

## 兑换激活码

> https://api.bilibili.com/x/vip/code/open

*请求方式：POST*

认证方式：Cookie（SESSDATA）

**正文参数（application/x-www-form-urlencoded）：**

| 参数名 | 类型 | 内容 | 必要性 | 备注 |
| ------ | ---- | ---- | ------ | ---- |
| t | num | 当前时间戳 | 必要 | 毫秒级 |
| code | str | 兑换码 | 必要 | 16位十六进制字符串 |
| verify | str | 图片验证码内容 | 必要 | 图片中识别出的字符 |
| mid | num | 目标用户UID | 必要 | 需要兑换到的账号 |
| token | str | 验证码令牌 | 必要 | 从 `verify` 接口获取 |
| csrf | str | CSRF Token | 必要 | 位于 Cookie 中的 `bili_jct` |

**json回复：**

根对象：

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| code | num | 返回值 | 0：成功<br />69068：激活码不存在<br />69070：激活码已被使用<br />69947：验证码输入有误 |
| message | str | 错误信息 | |
| ttl | num | 1 | |
| data | null/obj | 信息本体 | |

**示例：**

```shell
curl 'https://api.bilibili.com/x/vip/code/open' \
    --data-urlencode 't=1783048944958' \
    --data-urlencode 'code=46669c86d0301c64' \
    --data-urlencode 'verify=cjh1z' \
    --data-urlencode 'mid=3707015195003287' \
    --data-urlencode 'token=b301ed1280d648de8b81830d8fe4e4c5' \
    --data-urlencode 'csrf=xxx' \
    -b 'SESSDATA=xxx'
```

<details>
<summary>查看响应示例：</summary>

**成功响应：**

```json
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": null
}
```

**失败响应（不存在）：**

```json
{
    "code": 69068,
    "message": "激活码不存在",
    "ttl": 1,
    "data": null
}
```

**失败响应（已使用）：**

```json
{
    "code": 69070,
    "message": "激活码已被使用",
    "ttl": 1,
    "data": null
}
```

**失败响应（验证码错误）：**

```json
{
    "code": 69947,
    "message": "验证码输入有误",
    "ttl": 1,
    "data": null
}
```

</details>

## 公共错误码

| 状态码 | 含义 |
| ------ | ---- |
| 0 | 兑换成功 |
| -101 | 账号未登录 |
| 69068 | 激活码不存在 |
| 69070 | 激活码已被使用 |
| 69947 | 验证码输入有误 |

## 兑换流程说明

```python
# 伪代码
token, captcha_url = 获取验证码()
验证码图片 = 下载图片(captcha_url)
verify = 识别验证码(验证码图片)  # 人工识别或OCR
result = 提交兑换(code=兑换码, verify=verify, token=token, mid=用户UID)
```

### 注意事项

1. 验证码令牌（token）有效期较短，获取后需尽快使用
2. 验证码图片为4-5位字母数字组合
3. 兑换成功后 Cookie 中的大会员信息会同步更新
4. 兑换码为一次性使用，使用后即失效
5. 建议在 `https://big.bilibili.com` 域下操作，需携带正确的 Referer
