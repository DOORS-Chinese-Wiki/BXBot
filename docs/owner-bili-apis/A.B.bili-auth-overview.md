# B站 API 认证参数总览

本文档汇总整理 B站 API 涉及的所有认证相关参数，包括获取方式、依赖关系和常见错误码。

---

## 1. Cookie 认证（SESSDATA）

| 参数名   | 位置   | 用途         | 获取方式       |
| -------- | ------ | ------------ | -------------- |
| SESSDATA | Cookie | 核心登录凭证 | 登录后自动下发 |

- **有效期**：约 1 个月（以实际为准）
- **失效表现**：接口返回 `-101`（未登录）
- **注意事项**：禁止明文传输，需配合 HTTPS

---

## 2. CSRF 防护（bili_jct）

| 参数名   | 位置   | 用途       | 获取方式                         |
| -------- | ------ | ---------- | -------------------------------- |
| bili_jct | Cookie | CSRF Token | 登录后自动下发，与 SESSDATA 绑定 |

- **使用场景**：所有 POST/PUT/DELETE 操作类接口
- **传递方式**：表单参数 `csrf` 或 `csrf_token`
- **失效表现**：接口返回 `-403`（访问权限不足）
- **注意事项**：与 SESSDATA 一一对应，更换设备或重新登录后更新

---

## 3. WBI 签名

| 参数名 | 位置      | 用途     | 获取方式               |
| ------ | --------- | -------- | ---------------------- |
| w_rid  | URL Query | 请求签名 | 算法生成（见下方）     |
| wts    | URL Query | 时间戳   | 当前 Unix 时间戳（秒） |

- **使用场景**：部分查询接口（如用户空间投稿列表、用户关系查询等）
- **签名算法**：详见 [WBI 签名文档](./auth/sign/wbi.md)
- **失效表现**：接口返回 `-400` 或带 `v_voucher` 的响应
- **注意事项**：`img_key` 和 `sub_key` 每日更新，需做好缓存

---

## 4. APP 签名

| 参数名 | 位置             | 用途     | 获取方式               |
| ------ | ---------------- | -------- | ---------------------- |
| appkey | URL Query / Body | 应用标识 | 固定值（见 APPKey 表） |
| sign   | URL Query / Body | 请求签名 | 算法生成（见下方）     |

- **使用场景**：部分 APP 端接口
- **签名算法**：详见 [APP 签名文档](./auth/sign/APP.md)
- **注意事项**：不同 APP（粉版/概念版/必剪等）使用不同的 appkey/appsec

---

## 5. 风控参数（buvid / dm_* / b_wet）

| 参数名           | 位置               | 用途           | 获取方式                  |
| ---------------- | ------------------ | -------------- | ------------------------- |
| buvid            | Cookie / URL Query | 设备标识       | 浏览器生成，取自 `buvid3` |
| dm_img_list      | URL Query          | 鼠标轨迹       | 页面采集                  |
| dm_img_str       | URL Query          | GPU/WebGL 信息 | 页面采集                  |
| dm_cover_img_str | URL Query          | 渲染器信息     | 页面采集                  |
| dm_img_inter     | URL Query          | 交互信息       | 页面采集                  |
| b_wet            | URL Query          | RSA 加密风控   | 算法生成（RSA 加密签名）  |

- **使用场景**：WBI 签名接口通常伴随这些风控参数，动态发布接口需额外携带 `b_wet`
- **失效表现**：缺失可能导致 `-400` 或 `-403`
- **注意事项**：纯后端模拟请求时较难伪造，建议从真实浏览器环境采集

---

## 6. 认证方式汇总表

| 接口类型           | SESSDATA | bili_jct (CSRF) | WBI 签名 | APP 签名 | 风控参数   | 示例接口                                           |
| ------------------ | -------- | --------------- | -------- | -------- | ---------- | -------------------------------------------------- |
| 查询类（公开数据） | 可选     | ❌               | ❌        | ❌        | ❌          | 视频信息、用户公开信息                             |
| 查询类（需登录）   | ✅        | ❌               | ❌        | ❌        | ❌          | 历史列表、空间统计、硬币余额                       |
| WBI 查询类         | ✅        | ❌               | ✅        | ❌        | ⚠️ 部分需要 | 投稿列表、用户空间信息、追番列表、排行榜、评论列表 |
| 操作类（POST）     | ✅        | ✅               | ❌        | ❌        | ❌          | 黑名单、大会员签到、收藏夹 CRUD                    |
| WBI 操作类         | ✅        | ✅               | ✅        | ❌        | ⚠️ 部分需要 | 稍后再看批量删除、清空稍后再看                     |
| 动态发布           | ✅        | ✅               | ✅        | ❌        | ✅          | 动态发布（纯文本/图文）                            |
| APP 接口           | ✅        | ❌               | ❌        | ✅        | ❌          | APP 专用接口（本次未抓）                           |

> **说明**：风控参数（`dm_img_list`、`dm_img_str`、`dm_cover_img_str`、`dm_img_inter`）在部分 WBI 签名接口中为必要参数，缺失可能导致 `-403` 风控拦截。涉及接口包括 `/x/space/wbi/arc/search`（投稿列表）和 `/x/space/wbi/acc/info`（用户空间信息）等。动态发布接口额外需要 `b_wet`（RSA 加密签名参数）。

---

## 7. 各接口认证需求明细

| 模块              | 接口路径                                    | 请求方式 | SESSDATA | CSRF | WBI  | 风控 | 文档                                   |
| ----------------- | ------------------------------------------- | -------- | -------- | ---- | ---- | ---- | -------------------------------------- |
| **B币钱包**       |                                             |          |          |      |      |      |                                        |
|                   | `/paywallet/wallet/listForUserRecharges`    | POST     | ✅        | ❌    | ❌    | ❌    | `bili-bcoin-api.md`                    |
|                   | `/paywallet/wallet/listForUserPays`         | POST     | ✅        | ❌    | ❌    | ❌    | `bili-bcoin-api.md`                    |
| **黑名单**        |                                             |          |          |      |      |      |                                        |
|                   | `/x/relation/blacks`                        | GET      | ✅        | ❌    | ❌    | ❌    | `bili-blacklist-api.md`                |
|                   | `/x/relation/modify` (act=5)                | POST     | ✅        | ✅    | ❌    | ❌    | `bili-blacklist-api.md`                |
|                   | `/x/relation/modify` (act=6)                | POST     | ✅        | ✅    | ❌    | ❌    | `bili-blacklist-api.md`                |
| **硬币**          |                                             |          |          |      |      |      |                                        |
|                   | `/site/getCoin`                             | GET      | ✅        | ❌    | ❌    | ❌    | `bili-coin-api.md`                     |
|                   | `/x/member/web/coin/log`                    | GET      | ✅        | ❌    | ❌    | ❌    | `bili-coin-api.md`                     |
|                   | `/x/web-interface/coin/today/exp`           | GET      | ✅        | ❌    | ❌    | ❌    | `bili-coin-api.md`                     |
|                   | `/x/space/coin/video`                       | GET      | ✅        | ❌    | ❌    | ❌    | `bili-coin-api.md`                     |
| **充电**          |                                             |          |          |      |      |      |                                        |
|                   | `/x/upower/charge/follow/info`              | GET      | ✅        | ✅    | ❌    | ❌    | `bili-electric-charge-status-api.md`   |
|                   | `/x/upowerv2/gw/rights/guide`               | GET      | ✅        | ✅    | ❌    | ❌    | `bili-electric-rights-guide-api.md`    |
| **动态**          |                                             |          |          |      |      |      |                                        |
|                   | `/x/polymer/web-dynamic/v1/feed/nav`        | GET      | ✅        | ❌    | ❌    | ❌    | `bili-dynamic-feed-api.md`             |
|                   | `/x/polymer/web-dynamic/v1/opus/feed/space` | GET      | ✅        | ❌    | ✅    | ❌    | `bili-article-list-api.md`             |
|                   | `/x/polymer/web-dynamic/v1/feed/space`      | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-dynamic-feed-api.md`       |
|                   | `/x/dynamic/feed/draw/upload_bfs`           | POST     | ✅        | ✅    | ❌    | ❌    | `bili-dynamic-draw-publish-api.md`     |
|                   | `/x/dynamic/feed/create/submit_check`       | POST     | ✅        | ✅    | ❌    | ❌    | `bili-dynamic-publish-api.md`          |
|                   | `/x/dynamic/feed/create/dyn`                | POST     | ✅        | ✅    | ✅    | ✅    | `bili-dynamic-publish-api.md`          |
|                   | `/x/dynamic/feed/operate/remove`            | POST     | ✅        | ✅    | ❌    | ❌    | `bili-dynamic-delete-api.md`           |
|                   | `/x/dynamic/feed/dyn/thumb`                 | POST     | ✅        | ✅    | ❌    | ❌    | `bili-dynamic-thumb-api.md`            |
| **粉丝勋章**      |                                             |          |          |      |      |      |                                        |
|                   | `/xlive/web-ucenter/user/MedalWall`         | GET      | ✅        | ❌    | ❌    | ❌    | `bili-fans-medal-api.md`               |
|                   | `/xlive/app-ucenter/v1/fansMedal/wear`      | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fans-medal-api.md`               |
|                   | `/xlive/app-ucenter/v1/fansMedal/take_off`  | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fans-medal-api.md`               |
| **收藏夹**        |                                             |          |          |      |      |      |                                        |
|                   | `/x/v3/fav/folder/created/list-all`         | GET      | ✅        | ❌    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/resource/list`                   | GET      | ✅        | ❌    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/folder/add`                      | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/folder/edit`                     | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/folder/del`                      | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/resource/deal`                   | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/resource/batch-del`              | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/resource/copy`                   | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
|                   | `/x/v3/fav/resource/move`                   | POST     | ✅        | ✅    | ❌    | ❌    | `bili-fav-api.md`                      |
| **历史记录**      |                                             |          |          |      |      |      |                                        |
|                   | `/x/web-interface/history/cursor`           | GET      | ✅        | ❌    | ❌    | ❌    | `bili-history-api.md`                  |
|                   | `/x/web-interface/history/search`           | GET      | ✅        | ❌    | ❌    | ❌    | `bili-history-search-api.md`           |
|                   | `/x/v2/history/delete`                      | POST     | ✅        | ✅    | ❌    | ❌    | `bili-history-api.md`                  |
|                   | `/x/v2/history/clear`                       | POST     | ✅        | ✅    | ❌    | ❌    | `bili-history-api.md`                  |
|                   | `/x/v2/history/report`                      | POST     | ✅        | ✅    | ❌    | ❌    | `bili-history-report-api.md`           |
| **退出登录**      |                                             |          |          |      |      |      |                                        |
|                   | `/login/exit/v2`                            | POST     | ✅        | ✅    | ❌    | ❌    | `bili-login-exit-api.md`               |
| **认证条件**      |                                             |          |          |      |      |      |                                        |
|                   | `/x/member/official/conditions`             | GET      | ✅        | ❌    | ❌    | ❌    | `bili-official-conditions-api.md`      |
| **排行榜**        |                                             |          |          |      |      |      |                                        |
|                   | `/x/web-interface/ranking/v2`               | GET      | ✅        | ❌    | ✅    | ❌    | `bili-ranking-api.md`                  |
| **关系**          |                                             |          |          |      |      |      |                                        |
|                   | `/x/relation/stat`                          | GET      | ✅        | ❌    | ❌    | ❌    | `bili-relation-stat-api.md`            |
|                   | `/x/relation/tag` (tagid=-10)               | GET      | ✅        | ❌    | ❌    | ❌    | `bili-relation-special-api.md`         |
|                   | `/x/relation/followings`                    | GET      | ✅        | ❌    | ❌    | ❌    | `bili-relation-followings-api.md`      |
|                   | `/x/relation/fans`                          | GET      | ✅        | ❌    | ❌    | ❌    | `bili-relation-fans-api.md`            |
|                   | `/x/relation/same/followings`               | GET      | ✅        | ❌    | ❌    | ❌    | `bili-relation-same-followings-api.md` |
| **空间-投稿**     |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/wbi/arc/search`                   | GET      | ✅        | ❌    | ✅    | ✅    | `bili-space-archive-api.md`            |
| **空间-置顶**     |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/top/arc`                          | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-top-api.md`                |
| **空间-追番**     |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/bangumi/follow/list` (type=1)     | GET      | ✅        | ❌    | ✅    | ❌    | `bili-space-bangumi-api.md`            |
| **空间-追剧**     |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/bangumi/follow/list` (type=2)     | GET      | ✅        | ❌    | ✅    | ❌    | `bili-space-cinema-list-api.md`        |
| **空间-剧集列表** |                                             |          |          |      |      |      |                                        |
|                   | `/pgc/view/web/ep/list`                     | GET      | ✅        | ❌    | ❌    | ❌    | `bili-bangumi-ep-list-api.md`          |
| **空间-用户信息** |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/wbi/acc/info`                     | GET      | ✅        | ❌    | ✅    | ✅    | `bili-space-user-info-api.md`          |
| **空间-我的信息** |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/v2/myinfo`                        | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-myinfo-api.md`             |
| **空间-统计**     |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/upstat`                           | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-upstat-api.md`             |
| **空间-导航计数** |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/navnum`                           | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-navnum-api.md`             |
| **空间-隐私设置** |                                             |          |          |      |      |      |                                        |
|                   | `/x/space/setting`                          | GET      | ✅        | ❌    | ❌    | ❌    | `bili-space-setting-api.md`            |
| **空间-合集列表** |                                             |          |          |      |      |      |                                        |
|                   | `/x/polymer/web-space/seasons_series_list`  | GET      | ✅        | ❌    | ✅    | ❌    | `bili-space-seasons-list-api.md`       |
| **账号安全**      |                                             |          |          |      |      |      |                                        |
|                   | `/x/safecenter/user/info`                   | GET      | ✅        | ❌    | ❌    | ❌    | `bili-account-safe-api.md`             |
| **稍后再看**      |                                             |          |          |      |      |      |                                        |
|                   | `/x/v2/history/toview/web`                  | GET      | ✅        | ❌    | ❌    | ❌    | `bili-toview-api.md`                   |
|                   | `/x/v2/history/toview/add`                  | POST     | ✅        | ✅    | ❌    | ❌    | `bili-toview-api.md`                   |
|                   | `/x/v2/history/toview/del`                  | POST     | ✅        | ✅    | ❌    | ❌    | `bili-toview-api.md`                   |
|                   | `/x/v2/history/toview/v2/dels`              | POST     | ✅        | ✅    | ✅    | ❌    | `bili-toview-api.md`                   |
|                   | `/x/v2/history/toview/clear`                | POST     | ✅        | ✅    | ✅    | ❌    | `bili-toview-api.md`                   |
| **评论**          |                                             |          |          |      |      |      |                                        |
|                   | `/x/v2/reply/wbi/main` (type=1)             | GET      | ✅        | ❌    | ✅    | ❌    | `bili-reply-api.md`                    |
|                   | `/x/v2/reply/wbi/main` (type=12)            | GET      | ✅        | ❌    | ✅    | ❌    | `bili-reply-api.md`                    |
|                   | `/x/v2/reply/up/fulllist`                   | GET      | ✅        | ❌    | ❌    | ❌    | `bili-reply-up-list-api.md`            |
|                   | `/x/v2/reply/up/selection/list`             | GET      | ✅        | ❌    | ❌    | ❌    | `bili-reply-selection-list-api.md`     |
| **搜索**          |                                             |          |          |      |      |      |                                        |
|                   | `/x/web-interface/suggest`                  | GET      | ✅        | ❌    | ✅    | ❌    | `bili-search-suggest-api.md`           |
|                   | `/x/web-interface/wbi/search/type`          | GET      | ✅        | ❌    | ✅    | ❌    | `bili-search-type-api.md`              |
| **创作中心**      |                                             |          |          |      |      |      |                                        |
|                   | `/member.bilibili.com/x/web/assist`         | GET      | ✅        | ❌    | ❌    | ❌    | `bili-assist-list-api.md`              |
|                   | `/member.bilibili.com/x/web/assist/set`     | POST     | ✅        | ✅    | ❌    | ❌    | `bili-assist-set-api.md`               |
|                   | `/member.bilibili.com/x/web/assist/add`     | POST     | ✅        | ✅    | ❌    | ❌    | `bili-assist-add-api.md`               |
|                   | `/member.bilibili.com/x/web/assist/del`     | POST     | ✅        | ✅    | ❌    | ❌    | `bili-assist-del-api.md`               |
|                   | `/member.bilibili.com/x/web/detail/xcode`   | GET      | ✅        | ❌    | ❌    | ❌    | `bili-video-transcode-api.md`          |
|                   | `/member.bilibili.com/x/web/detail/audit`   | GET      | ✅        | ❌    | ❌    | ❌    | `bili-video-audit-api.md`              |
| **大会员**        |                                             |          |          |      |      |      |                                        |
|                   | `/x/vip/web/vip_center/info`                | GET      | ✅        | ❌    | ❌    | ❌    | `bili-vip-center-api.md`               |
|                   | `/x/vip/experience/add`                     | POST     | ✅        | ✅    | ❌    | ❌    | `bili-vip-center-api.md`               |
|                   | `/x/vip/privilege/my`                       | GET      | ✅        | ❌    | ❌    | ❌    | `bili-vip-center-api.md`               |
| **大会员兑换码**  |                                             |          |          |      |      |      |                                        |
|                   | `/x/vip/code/verify`                        | GET      | ✅        | ❌    | ❌    | ❌    | `bili-vip-code-api.md`                 |
|                   | `/x/v1/captcha/get`                         | GET      | ❌        | ❌    | ❌    | ❌    | `bili-vip-code-api.md`                 |
|                   | `/x/vip/code/open`                          | POST     | ✅        | ✅    | ❌    | ❌    | `bili-vip-code-api.md`                 |
| **消息**          |                                             |          |          |      |      |      |                                        |
|                   | `/link_setting/v1/link_setting/get`         | GET      | ✅        | ❌    | ❌    | ❌    | `bili-msg-link-setting-api.md`         |
|                   | `/session_svr/v1/session_svr/new_sessions`  | GET      | ✅        | ❌    | ✅    | ❌    | `bili-msg-session-list-api.md`         |
|                   | `/svr_sync/v1/svr_sync/fetch_session_msgs`  | GET      | ✅        | ❌    | ✅    | ❌    | `bili-msg-session-api.md`              |
|                   | `/session_svr/v1/session_svr/set_top`       | POST     | ✅        | ✅    | ❌    | ❌    | `bili-msg-top-api.md`                  |
|                   | `/session_svr/v1/session_svr/update_ack`    | POST     | ✅        | ✅    | ❌    | ❌    | `bili-msg-update-ack-api.md`           |
|                   | `/session_svr/v1/session_svr/single_unread` | GET      | ✅        | ❌    | ❌    | ❌    | `bili-msg-unread-session-api.md`       |
|                   | `/x/im/web/msgfeed/unread`                  | GET      | ✅        | ❌    | ❌    | ❌    | `bili-msgfeed-unread-api.md`           |

> **图例**：
> - ✅ 表示该认证参数为**必要**
> - ❌ 表示该认证参数为**不需要**
> - ⚠️ 表示**部分接口需要**（详见具体文档）

---

## 8. 快速排查指南

| 错误码    | 常见原因                 | 排查方向                                     |
| --------- | ------------------------ | -------------------------------------------- |
| -101      | 未登录或 SESSDATA 过期   | 重新登录                                     |
| -111      | CSRF 校验失败            | 检查 `bili_jct` 是否与 `csrf` 参数一致       |
| -400      | 请求参数错误或签名缺失   | 检查 WBI/APP 签名是否正确                    |
| -403      | 访问权限不足或 CSRF 无效 | 检查 `bili_jct` 是否有效，或风控参数是否完整 |
| v_voucher | WBI 签名错误             | 检查 `w_rid` 和 `wts` 是否正确生成           |
| -352      | 请求被风控拦截           | 检查 `buvid` 和风控参数是否完整              |
| 53013     | 用户隐私设置未公开       | 目标用户关闭了关注/粉丝列表展示              |

---

## 9. 参考文档

| 文档                                           | 说明                   |
| ---------------------------------------------- | ---------------------- |
| [WBI 签名文档](./auth/sign/wbi.md)             | WBI 签名算法详解       |
| [APP 签名文档](./auth/sign/APP.md)             | APP 签名算法详解       |
| [APPKey 列表](./auth/sign/APPKey.md)           | 已知 APPKey 汇总       |
| [bili_ticket 说明](./auth/sign/bili_ticket.md) | bili_ticket 生成与使用 |
| [公共错误码](./auth/errcode.md)                | 接口返回码参考         |
| [图片格式化](./auth/picture.md)                | BFS 图片处理参数       |
| [设备标识算法](./auth/device_identity.md)      | BUVID、FP 生成算法     |
| [BV ID 说明](./auth/bvid_desc.md)              | AV/BV 互转算法         |
| [时间戳获取](./auth/time_stamp.md)             | 服务器时间接口         |
