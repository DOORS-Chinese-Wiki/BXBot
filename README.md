# BXBot

把指定 X/Twitter 账号的新推文翻译成中文，并按内容类型同步到 B 站：

- 纯文字推文发布为 B 站文字动态。
- 图片推文发布为 B 站图文动态。
- 视频推文投稿为 B 站视频，默认标记为转载并附原推链接。
- 使用 OpenAI 兼容接口完成翻译和内容过滤。
- 不依赖付费 Twitter API。

## 环境要求

- Python 3.11+
- Windows、Linux 或 macOS
- 可用的 B 站账号、X cookies（可选）和 LLM 接口
- ffmpeg（可选，用于生成视频封面）

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m bxbot init
```

编辑 `config.yaml`，填写要同步的 X 账号；编辑 `.env`，填写 `LLM_API_KEY`。然后完成登录和自检：

```powershell
.\.venv\Scripts\python.exe -m bxbot login-bili
.\.venv\Scripts\python.exe -m bxbot login-x
.\.venv\Scripts\python.exe -m bxbot doctor
```

先试跑一轮，不会实际发布：

```powershell
.\.venv\Scripts\python.exe -m bxbot once --dry-run
```

确认无误后运行：

```powershell
run.bat
```

Linux 或 macOS 使用 `.venv/bin/python -m bxbot run`。

## 常用命令

| 命令 | 作用 |
| --- | --- |
| `python -m bxbot init` | 生成 `config.yaml`、`.env` 和 `data/` |
| `python -m bxbot login-bili` | 通过二维码登录 B 站 |
| `python -m bxbot login-x` | 导入 X cookies |
| `python -m bxbot doctor` | 检查配置、LLM、账号凭证和状态库 |
| `python -m bxbot once --dry-run` | 执行一轮但不发布 |
| `python -m bxbot once --tweet-id ID` | 回放指定推文 |
| `python -m bxbot run` | 按配置间隔持续轮询 |

## 配置

主要配置项如下，完整模板见 `config.example.yaml`。

- `target.handle`：目标 X 账号，不带 `@`。
- `twitter.backend_order`：抓取后端及降级顺序。
- `twitter.proxy`：访问 X 不稳定时使用的代理。
- `llm.*`：OpenAI 兼容接口、模型和翻译失败策略。
- `filter.*`：关键词和 LLM 内容过滤规则。
- `translate.mode`：仅译文、仅原文或双语。
- `bilibili.*`：分区、标签、发布间隔和单轮上限。
- `poll.interval_seconds`：轮询间隔，默认 600 秒。

密钥应放在 `.env` 中。`config.yaml`、`.env` 和 `data/` 已被 Git 忽略。

## 工作流程

```text
抓取 X 推文 -> 过滤 -> LLM 翻译与判断 -> 下载媒体 -> 发布到 B 站 -> SQLite 去重
```

首次运行只建立推文水位，不回填历史。发布失败会重试，遇到 B 站风控会暂停一段时间。

## 开发与测试

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

项目目录：

```text
bxbot/      主程序
tests/      单元测试
docs/       B 站接口参考文档
```

## 注意事项

- B 站动态发布和 X 抓取都依赖非官方接口，接口调整后可能需要更新代码。
- 搬运内容时请保留来源并遵守原作者要求、B 站规则和当地法律。
- `bilibili-api-python` 已锁定版本，升级前请先运行测试。

## 许可证

本项目源码采用 [CC BY-SA 4.0](LICENSE) 许可。使用、修改或分发时须保留署名，并以相同协议共享。第三方依赖及引用内容仍适用其各自的许可证。
