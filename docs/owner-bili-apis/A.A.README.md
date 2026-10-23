# Owner-Bili-APIs —— B站 API 个人整理合集

本仓库为个人通过抓包、逆向分析整理所得的 Bilibili（B站）API 文档合集。

> 原项目 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 因故停止维护，本仓库在其基础上补充了大量缺失接口，并更新了已有接口的签名方式与参数说明。所有文档均经过实际抓包验证，确保有效。

---

## 📁 目录结构

```
owner-bili-apis/
├── A.A.README.md                       # 本文件（手动置顶，项目说明）
├── A.B.bili-auth-overview.md           # 认证参数总览（手动置顶）
├── A.C.--------------------------------------  # 视觉分隔线
├── bili-account-safe-api.md            # 账号安全中心
├── bili-article-list-api.md            # 图文动态列表（专栏/文章）
├── bili-assist-add-api.md              # UP主协管员添加
├── bili-assist-del-api.md              # UP主协管员移除
├── bili-assist-list-api.md             # UP主协管员列表
├── bili-assist-set-api.md              # UP主协管员权限设置
├── bili-bangumi-ep-list-api.md         # 番剧剧集列表
├── bili-bcoin-api.md                   # B币钱包（充值/消费）
├── bili-blacklist-api.md               # 黑名单管理
├── bili-coin-api.md                    # 硬币系统（余额/记录/投币经验）
├── bili-dynamic-delete-api.md          # 动态删除
├── bili-dynamic-draw-publish-api.md    # 图文动态发布（带图片）
├── bili-dynamic-feed-api.md            # 动态首页推荐流
├── bili-dynamic-publish-api.md         # 动态发布（纯文本）
├── bili-dynamic-thumb-api.md           # 动态点赞/取消点赞
├── bili-electric-charge-status-api.md  # 充电状态查询
├── bili-electric-rights-guide-api.md   # 充电专属权益页面
├── bili-fans-medal-api.md              # 粉丝勋章
├── bili-fav-api.md                     # 收藏夹（完整CRUD）
├── bili-history-api.md                 # 观看历史（列表/搜索/删除/清空）
├── bili-history-report-api.md          # 历史记录上报（观看进度）
├── bili-history-search-api.md          # 历史记录搜索
├── bili-login-exit-api.md              # 退出登录
├── bili-msg-link-setting-api.md        # 消息通知设置
├── bili-msg-session-api.md             # 私信历史记录
├── bili-msg-session-list-api.md        # 私信会话列表
├── bili-msg-top-api.md                 # 置顶/取消置顶私信
├── bili-msg-update-ack-api.md          # 标记私信已读
├── bili-msg-unread-session-api.md      # 私信未读数
├── bili-msgfeed-unread-api.md          # 通知消息未读数
├── bili-official-conditions-api.md     # UP主认证条件查询
├── bili-ranking-api.md                 # 排行榜
├── bili-relation-fans-api.md           # 粉丝列表
├── bili-relation-followings-api.md     # 关注列表
├── bili-relation-same-followings-api.md # 共同关注列表
├── bili-relation-special-api.md        # 特别关注列表
├── bili-relation-stat-api.md           # 关系统计（关注/粉丝数）
├── bili-reply-api.md                   # 评论列表（视频 + 图文动态）
├── bili-reply-selection-list-api.md    # UP主评论精选列表
├── bili-reply-up-list-api.md           # UP主评论管理列表
├── bili-search-suggest-api.md          # 搜索建议
├── bili-search-type-api.md             # 综合搜索
├── bili-space-archive-api.md           # 用户空间-投稿列表
├── bili-space-bangumi-api.md           # 用户空间-追番列表
├── bili-space-cinema-list-api.md       # 用户空间-追剧列表
├── bili-space-coin-video-api.md        # 用户空间-投币视频列表
├── bili-space-dynamic-feed-api.md      # 用户空间-动态列表
├── bili-space-myinfo-api.md            # 用户空间-我的信息（V2）
├── bili-space-navnum-api.md            # 用户空间-导航计数
├── bili-space-seasons-list-api.md      # 用户空间-合集列表
├── bili-space-setting-api.md           # 用户空间-隐私设置
├── bili-space-top-api.md               # 用户空间-置顶视频
├── bili-space-upstat-api.md            # 用户空间-统计数据
├── bili-space-user-info-api.md         # 用户空间-用户信息（WBI）
├── bili-toview-api.md                  # 稍后再看（完整CRUD）
├── bili-video-audit-api.md             # 视频稿件审核状态查询
├── bili-video-transcode-api.md         # 视频转码状态查询
├── bili-vip-center-api.md              # 大会员中心
├── bili-vip-code-api.md                # 大会员兑换码
└── auth/                               # 认证与通用参考文档
    ├── bvid_desc.md                    # AV/BV 互转算法
    ├── device_identity.md              # 设备标识算法
    ├── errcode.md                      # 公共错误码
    ├── picture.md                      # 图片格式化参数
    ├── time_stamp.md                   # 获取服务器时间
    └── sign/                           # 签名相关
        ├── APP.md                      # APP 签名算法
        ├── APPKey.md                   # 已知 APPKey 汇总
        ├── bili_ticket.md              # bili_ticket 说明
        └── wbi.md                      # WBI 签名算法
```

> **前缀说明**：`A.A.`、`A.B.`、`A.C.` 前缀用于在文件管理器中手动置顶排序，便于快速定位 README、认证总览和视觉分隔线。

---

## 📚 文档列表与功能说明

| 文档                                   | 功能说明                                                     |
| -------------------------------------- | ------------------------------------------------------------ |
| `A.B.bili-auth-overview.md`            | **认证参数总览**：汇总 SESSDATA、CSRF、WBI、APP、风控参数的使用方式 |
| `bili-account-safe-api.md`             | 账号安全中心（绑定手机/邮箱、实名状态、安全评分）            |
| `bili-article-list-api.md`             | 图文动态列表（专栏/文章）—— 需 WBI 签名                      |
| `bili-assist-add-api.md`               | UP主协管员添加                                               |
| `bili-assist-del-api.md`               | UP主协管员移除                                               |
| `bili-assist-list-api.md`              | UP主协管员列表                                               |
| `bili-assist-set-api.md`               | UP主协管员权限设置                                           |
| `bili-bangumi-ep-list-api.md`          | 番剧剧集列表（含分P、OP/ED时间点）                           |
| `bili-bcoin-api.md`                    | B币充值记录与消费记录                                        |
| `bili-blacklist-api.md`                | 黑名单列表、添加、移除                                       |
| `bili-coin-api.md`                     | 硬币余额、收支记录、今日投币经验、投币视频列表               |
| `bili-dynamic-delete-api.md`           | 动态删除 —— 仅需 CSRF                                        |
| `bili-dynamic-draw-publish-api.md`     | **图文动态发布（带图片）** —— 上传图片 → 提交检查 → 正式发布三步流程，含 WBI 签名与风控参数 |
| `bili-dynamic-feed-api.md`             | 动态首页推荐流                                               |
| `bili-dynamic-publish-api.md`          | 动态发布（纯文本）—— 需 WBI 签名 + CSRF                      |
| `bili-dynamic-thumb-api.md`            | 动态点赞/取消点赞 —— 仅需 CSRF                               |
| `bili-electric-charge-status-api.md`   | 充电状态查询（对 UP 主的充电天数、剩余天数）                 |
| `bili-electric-rights-guide-api.md`    | 充电专属权益页面（UP 主所有档位的专属内容）                  |
| `bili-fans-medal-api.md`               | 粉丝勋章墙、佩戴、取消佩戴                                   |
| `bili-fav-api.md`                      | 收藏夹完整 CRUD（列表、内容、创建、修改、删除、添加/删除资源、批量删除、复制、移动） |
| `bili-history-api.md`                  | 观看历史列表（游标分页）、单条删除、清空全部                 |
| `bili-history-report-api.md`           | 历史记录上报（观看进度上报）                                 |
| `bili-history-search-api.md`           | **历史记录搜索** —— 按关键词、时间、时长搜索历史记录，需登录 |
| `bili-login-exit-api.md`               | 退出登录（V2）                                               |
| `bili-msg-link-setting-api.md`         | **消息通知设置** —— 获取消息通知、互动提醒等开关配置         |
| `bili-msg-session-api.md`              | **私信历史记录** —— 获取与指定联系人的私信消息，需 WBI 签名  |
| `bili-msg-session-list-api.md`         | **私信会话列表** —— 获取所有私信会话及最新消息，需 WBI 签名  |
| `bili-msg-top-api.md`                  | **置顶/取消置顶私信** —— 设置或取消私信会话的置顶状态        |
| `bili-msg-update-ack-api.md`           | **标记私信已读** —— 将指定会话的消息标记为已读，清零未读数   |
| `bili-msg-unread-session-api.md`       | **私信未读数** —— 获取私信未读数量（未关注/已关注/垃圾箱等） |
| `bili-msgfeed-unread-api.md`           | **通知消息未读数** —— 获取 at、回复、点赞、系统通知等未读数  |
| `bili-official-conditions-api.md`      | UP主认证条件查询（绑定手机、实名、粉丝数、投稿数）           |
| `bili-ranking-api.md`                  | 排行榜（全站/分区）—— 需 WBI 签名                            |
| `bili-relation-fans-api.md`            | **粉丝列表** —— 获取指定用户的粉丝列表，受隐私设置影响，使用游标分页 |
| `bili-relation-followings-api.md`      | **关注列表** —— 获取用户的关注列表，支持最常访问排序，获取他人时受 100 条限制，受隐私设置影响 |
| `bili-relation-same-followings-api.md` | **共同关注列表** —— 获取当前用户与目标用户的共同关注，不受隐私和 100 条限制 |
| `bili-relation-special-api.md`         | 特别关注列表                                                 |
| `bili-relation-stat-api.md`            | 关注数、粉丝数、黑名单数统计                                 |
| `bili-reply-api.md`                    | 评论列表（视频 + 图文动态）—— 需 WBI 签名                    |
| `bili-reply-selection-list-api.md`     | UP主评论精选列表（待精选）                                   |
| `bili-reply-up-list-api.md`            | UP主评论管理列表（所有稿件）                                 |
| `bili-search-suggest-api.md`           | **搜索建议（联想词）** —— 搜索框输入时自动补全，需 WBI 签名  |
| `bili-search-type-api.md`              | **综合搜索** —— 按用户、视频、番剧等类型搜索，需 WBI 签名    |
| `bili-space-archive-api.md`            | 用户空间视频投稿列表（含分区统计）—— 需 WBI 签名             |
| `bili-space-bangumi-api.md`            | 用户追番列表 —— 需 WBI 签名                                  |
| `bili-space-cinema-list-api.md`        | 用户追剧（电影）列表 —— 需 WBI 签名                          |
| `bili-space-coin-video-api.md`         | 用户投过币的视频列表                                         |
| `bili-space-dynamic-feed-api.md`       | 用户空间动态列表（图文/视频/转发）                           |
| `bili-space-myinfo-api.md`             | 当前用户自己的空间信息（V2）                                 |
| `bili-space-navnum-api.md`             | 用户空间各模块内容数量（视频、追番、收藏、相簿等）           |
| `bili-space-seasons-list-api.md`       | 用户合集列表（视频合集 + 直播回放合集）—— 需 WBI 签名        |
| `bili-space-setting-api.md`            | 用户空间隐私设置                                             |
| `bili-space-top-api.md`                | 用户置顶视频                                                 |
| `bili-space-upstat-api.md`             | 用户视频播放总数、获赞总数、专栏阅读数                       |
| `bili-space-user-info-api.md`          | 用户空间主页信息（含勋章、挂件、大会员）—— 需 WBI 签名       |
| `bili-toview-api.md`                   | 稍后再看：列表、添加、单条删除、批量删除、清空全部           |
| `bili-video-audit-api.md`              | 视频稿件审核状态查询（审核进度、驳回原因）                   |
| `bili-video-transcode-api.md`          | 视频转码状态查询（各清晰度转码进度）                         |
| `bili-vip-center-api.md`               | 大会员中心信息、每日签到、权益列表                           |
| `bili-vip-code-api.md`                 | 大会员兑换码（获取验证码、兑换）                             |
| `auth/bvid_desc.md`                    | AV号与BV号的互转算法                                         |
| `auth/device_identity.md`              | BUVID、设备指纹生成算法                                      |
| `auth/errcode.md`                      | 公共错误码速查表                                             |
| `auth/picture.md`                      | BFS图片格式化参数                                            |
| `auth/time_stamp.md`                   | 获取服务器当前时间戳                                         |
| `auth/sign/APP.md`                     | APP API 签名算法与 Demo                                      |
| `auth/sign/APPKey.md`                  | 已知 APPKey / APPSec 汇总表                                  |
| `auth/sign/bili_ticket.md`             | bili_ticket 生成示例                                         |
| `auth/sign/wbi.md`                     | WBI 签名算法详解与多语言 Demo                                |

---

## 🔑 认证与签名说明

所有接口的认证方式已在 **[A.B.bili-auth-overview.md](./A.B.bili-auth-overview.md)** 中汇总，包含：

- **SESSDATA**（Cookie 登录凭证）
- **bili_jct**（CSRF Token，POST 操作必需）
- **WBI 签名**（部分 GET 接口需要）
- **APP 签名**（APP 端专用）
- **风控参数**（buvid、dm_* 等）

建议开发前先阅读 `A.B.bili-auth-overview.md`，快速定位所需认证方式。

详细签名算法请参考 `auth/sign/` 目录下的文档。

---

## 🚀 如何使用

1. **查阅接口**：直接打开对应 `.md` 文件，查看接口地址、参数、响应示例、注意事项。
2. **调用测试**：根据文档中的 `curl` 示例进行测试，替换 Cookie 与参数。
3. **签名生成**：如需 WBI 或 APP 签名，参考 `auth/sign/` 下的算法文档。
4. **错误排查**：遇到返回码，查阅 `auth/errcode.md` 快速定位问题。

---

## ⚠️ 注意事项

- 本仓库所有文档均基于 **个人抓包与分析**，仅供学习研究使用，请勿用于商业或非法用途。
- 接口可能随 B站 版本更新而变化，若发现失效，可自行修正或留存记录。
- 文档中的示例参数、Cookie 等均为虚构或脱敏数据，请勿直接复制使用。

---

## 📌 与原始项目的区别

| 项目     | 原始项目（SocialSisterYi） | 本仓库（owner-bili-apis）                 |
| -------- | -------------------------- | ----------------------------------------- |
| 状态     | 已停止维护                 | 个人本地存档，持续更新                    |
| 覆盖范围 | 基础模块较全               | 补充大量操作类接口（CRUD）                |
| 签名文档 | 有                         | 保留并补充引用                            |
| 认证总览 | 无                         | 新增 `A.B.bili-auth-overview.md` 统一汇总 |
| 目录结构 | 散落各子目录               | 扁平化，按功能命名，便于检索              |

---

## 📅 更新记录

- **2026-07-11**：完成首批 20+ 接口文档，新增认证总览与签名目录。
- **2026-07-12**：补充番剧、追剧、剧集列表、安全中心、充电模块、动态、空间全家桶、排行榜、评论精选、视频审核/转码等接口，最终总数达 **44 个**，完善 README 与目录结构。
- **2026-07-13**：新增 **5 个** 接口，动态模块完整闭环：搜索建议、用户合集列表、动态发布（纯文本、图文）/点赞/删除（其中动态发布为高价值操作类接口）。
- **2026-07-14**：新增共同关注列表接口（`bili-relation-same-followings-api.md`），支持查询与目标用户的共同关注，不受隐私设置及 Web 端前 100 条限制。
- **2026-07-16**：新增关注列表接口（`bili-relation-followings-api.md`）和粉丝列表接口（`bili-relation-fans-api.md`），关系模块核心列表接口全部补全。
- **2026-07-20**：完善关注列表接口文档，补充 `order_type` 枚举值（最常访问/发布时间）、`contract_info` 契约计划字段、`special` 分页说明，明确自身关注列表无限制而查看他人仅返回前 100 条。
- **2026-07-26**：新增消息模块 **4 个** 接口：消息通知设置、私信历史记录、私信未读数、通知消息未读数，补全消息中心核心功能。
- **2026-07-29**：新增置顶/取消置顶私信接口（`bili-msg-top-api.md`），消息模块进一步完善。
- **2026-07-30**：新增历史记录搜索接口（`bili-history-search-api.md`），历史记录模块补全。
- **2026-08-17**：新增私信会话列表接口（`bili-msg-session-list-api.md`）和标记私信已读接口（`bili-msg-update-ack-api.md`），消息模块会话管理功能补全。
- **2026-08-18**：新增综合搜索接口（`bili-search-type-api.md`），支持按用户、视频、番剧等类型搜索，搜索模块补全。

---

**Happy Coding!** 🎯
