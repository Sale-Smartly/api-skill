---
name: salesmartly
description: SaleSmartly API 集成技能（只读查询），用于客户查询、消息查询、团队查询。通过封装的 Python 脚本调用 SaleSmartly API。使用场景：(1) 查询客户列表和详情，(2) 获取客户消息，(3) 查询团队成员，(4) 筛选今天新增客户，(5) 调用任意 API 接口。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
    env:
      - SALESMARTLY_API_TOKEN
      - SALESMARTLY_PROJECT_ID
homepage: https://salesmartly-api.apifox.cn/
---

# SaleSmartly API 技能

## 📁 技能包结构

```
salesmartly/
├── SKILL.md                 # 本文档（使用说明）
├── scripts/
│   └── client.py            # Python CLI 工具（封装 API 调用）
└── references/
    ├── api-full.md          # API 完整文档（本地缓存）
    ├── response-codes.md    # 错误码文档
    └── llms.txt             # AI 可读 API 目录（外部链接）
```

### 文件说明

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `SKILL.md` | 用户使用说明 | 低（功能变化时更新） |
| `scripts/client.py` | API 调用脚本 | 中（新增常用接口时） |
| `references/api-full.md` | API 参考文档 | 低（API 大版本更新） |
| `references/response-codes.md` | 错误码对照 | 低 |
| `llms.txt` | AI 接口目录 | **高**（SaleSmartly 自动更新） |

### 设计理念

1. **只读优先** - 只封装查询类接口，避免误操作
2. **常用 + 通用** - 高频接口封装命令，低频接口用 `api-call`
3. **AI 友好** - 通过 llms.txt 自主查询新接口
4. **易于维护** - 接口增加不需要频繁更新脚本

---

## ⚠️ 重要说明

### API 响应结构

**所有返回列表的接口，响应格式统一：**

```json
{
  "code": 0,              // 响应码（0=成功）
  "data": {
    "list": [...],        // 当前页数据列表
    "total": 12345,       // ← 总记录数（直接用这个！）
    "page": 1,            // 当前页码
    "page_size": 50       // 每页数量
  },
  "msg": "success",       // 响应消息
  "request_id": "xxx"     // 请求追踪 ID
}
```

**获取总数的正确方式：**
```python
result = api_request("get-contact-list", params)
total = result['data']['total']  # 总客户数
```

**❌ 错误做法：** 不要用 `page × page_size` 计算总数！

---

## ✅ 何时使用此技能

**✅ USE this skill when:**

- 查询 SaleSmartly 客户数据（列表、详情）
- 读取客户聊天记录
- 查询客服团队信息
- 统计报表（今天新增、渠道分布等）
- 调用任意 SaleSmartly API 接口（通过 `api-call`）
- AI 需要自主查询新接口（通过 llms.txt）

**❌ DON'T use this skill when:**

- 发送消息给客户 → 用 `api-call` 或 SaleSmartly 后台
- 分配会话给客服 → 用 `api-call` 或 SaleSmartly 后台
- 实时 webhook 通知 → 用 SaleSmartly 后台配置
- 大批量数据导出 → 用官方导出功能
- 修改客户资料 → 用 `api-call` 或 SaleSmartly 后台

---

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 临时设置（当前会话有效）
export SALESMARTLY_API_TOKEN="你的 Token"
export SALESMARTLY_PROJECT_ID="你的项目 ID"

# 永久设置（写入 ~/.zshrc）
echo 'export SALESMARTLY_API_TOKEN="你的 Token"' >> ~/.zshrc
echo 'export SALESMARTLY_PROJECT_ID="你的项目 ID"' >> ~/.zshrc
source ~/.zshrc
```

### 2. 验证配置

```bash
# 测试查询客户
python3 scripts/client.py get-contacts --page-size 3
```

### 3. 开始使用

```bash
# 查看今天新增客户
python3 scripts/client.py get-contacts --today

# 查看客服团队
python3 scripts/client.py get-members

# 调用任意 API
python3 scripts/client.py api-call get-member-list --page 1
```

---

## 前置条件

1. **账号要求**：SaleSmartly 企业版或 Max 版
2. **获取 API Token**：项目设置 → 企业开发设置 → API Token
3. **获取项目 ID**：SaleSmartly 后台左下角查看

## 技术说明

**API 版本**: V2 (新版)  
**Base URL**: `https://developer.salesmartly.com/api/v2`  
**认证方式**: External-Sign 签名（MD5）

## 快速开始

### 1. 配置环境变量

```bash
# 方式 1：临时设置（当前会话有效）
export SALESMARTLY_API_TOKEN="你的 Token"
export SALESMARTLY_PROJECT_ID="你的项目 ID"

# 方式 2：永久设置（写入 ~/.zshrc）
echo 'export SALESMARTLY_API_TOKEN="你的 Token"' >> ~/.zshrc
echo 'export SALESMARTLY_PROJECT_ID="你的项目 ID"' >> ~/.zshrc
source ~/.zshrc
```

**注意：只需要配置 Token 和 Project ID，不需要配置客户 ID（查询时作为参数传入）**

### 2. 验证配置

```bash
python scripts/client.py get-contacts --page-size 5
```

---

## 可用命令

### 1. 获取客户列表

```bash
# 查询所有客户
python scripts/client.py get-contacts

# 分页查询
python scripts/client.py get-contacts --page 1 --page-size 50

# 搜索客户（按名称/手机号）
python scripts/client.py get-contacts --keyword "张三"

# 查询今天新增客户
python scripts/client.py get-contacts --today

# 按渠道过滤（渠道 ID 见下方渠道列表）
python scripts/client.py get-contacts --channel 2

# 组合使用
python scripts/client.py get-contacts --today --page-size 100
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--page` | 页码 | 1 |
| `--page-size` | 每页数量（最大 100） | 50 |
| `--keyword` | 搜索关键词（名称/手机） | - |
| `--today` | 只显示今天新增客户 | false |
| `--channel` | 渠道 ID 过滤 | - |

---

### 2. 获取客户详情

```bash
python scripts/client.py get-contact --chat-user-id "abc123"
```

**参数说明：**
| 参数 | 说明 | 必填 |
|------|------|------|
| `--chat-user-id` | 客户聊天 ID | 是 |

---

### 3. 获取客户消息

```bash
python scripts/client.py get-messages --chat-user-id "abc123" --limit 20
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--chat-user-id` | 客户聊天 ID | 是 |
| `--limit` | 消息数量 | 20 |

---

### 4. 获取全量消息

```bash
python scripts/client.py get-all-messages --page 1 --page-size 50
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--page` | 页码 | 1 |
| `--page-size` | 每页数量（最大 100） | 50 |

---

### 5. 获取团队成员

```bash
python scripts/client.py get-members --page 1 --page-size 20
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--page` | 页码 | 1 |
| `--page-size` | 每页数量（最大 100） | 20 |

---

### 6. 调用任意 API

```bash
# 调用团队成员接口
python3 scripts/client.py api-call get-member-list -p page=1 -p page_size=20

# 调用消息接口
python3 scripts/client.py api-call get-message-list -p chat_user_id=xxx
```

**说明：** 
- 使用 `-p` 或 `--param` 传递参数
- 参数格式：`key=value`（使用 API 原始参数名，如下划线而非连字符）
- 可调用任何 SaleSmartly API 接口

---

### 7. 渠道列表

**渠道 ID 对照表：**

| ID | 渠道 | ID | 渠道 |
|----|------|----|------|
| 1 | Messenger | 12 | WhatsApp App |
| 2 | 聊天插件 | 13 | Instagram 评论 |
| 3 | Email | 15 | Telegram App |
| 4 | Telegram Bot | 16 | TikTok App |
| 5 | Instagram | 17 | TikTok 评论 |
| 6 | Line | 18 | Vkontakte |
| 7 | WhatsApp Api | 19 | Zalo App |
| 8 | Facebook 主页评论 | 20 | TikTok Business |
| 10 | Slack | 21 | TikTok Business 评论 |
| 11 | 企业微信 | | |

**渠道参数说明：**

`channel` 参数（可选）支持以下值：

- `1` - Messenger
- `2` - 聊天插件
- `3` - Email
- `4` - Telegram Bot
- `5` - Instagram
- `6` - Line
- `7` - WhatsApp Api
- `8` - Facebook 主页评论
- `10` - Slack
- `11` - 企业微信
- `12` - WhatsApp App
- `13` - Instagram 评论
- `15` - Telegram App
- `16` - TikTok App
- `17` - TikTok 评论
- `18` - Vkontakte
- `19` - Zalo App
- `20` - TikTok Business
- `21` - TikTok Business 评论

**使用示例：**
```bash
# 按渠道过滤客户
python scripts/client.py get-contacts --channel 7  # WhatsApp Api 客户
python scripts/client.py get-contacts --channel 2  # 聊天插件客户
python scripts/client.py get-contacts --channel 11 # 企业微信客户
python scripts/client.py get-contacts --channel 16 # TikTok App 客户
```

> 注：`get-channels` 命令待后续接口完善后添加

---

## 使用示例

### 示例 1：查看今天新增客户

```
用户：查一下今天新增了多少客户
→ 执行：python scripts/client.py get-contacts --today --page-size 100
→ 返回：今天新增客户列表（姓名、联系方式、来源渠道）
```

### 示例 2：查看某个客户的聊天记录

```
用户：看看客户张三最近的聊天记录
→ 先查客户 ID：python scripts/client.py get-contacts --keyword "张三"
→ 再查消息：python scripts/client.py get-messages --chat-user-id "abc123"
```

### 示例 3：查看客服团队

```
用户：我们有哪些客服？
→ 执行：python scripts/client.py get-members --page 1
→ 返回：客服团队列表（昵称、状态、接待上限）
```

### 示例 4：调用未封装的 API

```
用户：查一下分流链接
→ 执行：python scripts/client.py api-call split-link/get-list --page 1
→ 返回：分流链接列表
```

---

## 错误码处理

常见错误码及处理方式：

| 响应码 | 含义 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | 正常处理返回数据 |
| 100 | 无效的 API Token | 检查 Token 配置 |
| 102 | 签名验证失败 | 检查签名算法 |
| 103 | 请求频率超限 | 降低请求频率 |
| 201 | 渠道不存在 | 确认渠道 ID |
| 210 | 成员不存在 | 检查分配的成员 ID |
| 400 | 参数有误 | 检查请求参数格式 |
| 500 | 数据库错误 | 联系技术支持 |

详细响应码见 `references/response-codes.md`

---

## 注意事项

1. **Token 安全**：不要将 Token 提交到代码仓库
2. **频率限制**：API 有请求频率限制，避免短时间内大量请求
3. **page-size 限制**：最大值为 100
4. **时间过滤**：`--today` 参数会自动计算今天 0 点到当前的时间戳
5. **总数获取**：所有列表接口都返回 `data.total` 字段，直接用，不要计算！

---

## 📊 常见场景速查

### 统计类查询

```bash
# 总客户数
python scripts/client.py get-contacts --page-size 1
# → 看输出中的"总计：XXX 个客户"

# 今天新增客户数
python scripts/client.py get-contacts --today --page-size 1
# → 看输出中的"总计：XXX 个客户"

# WhatsApp 渠道客户数
python scripts/client.py get-contacts --channel 7 --page-size 1
# → 看输出中的"总计：XXX 个客户"
```

**原理：** API 返回的 `data.total` 是过滤后的总数，不是全部客户数

### 获取客户联系方式

```bash
# 查有手机号的客户（用 keyword 搜索）
python scripts/client.py get-contacts --keyword "138" --page-size 50
# → 会返回名称或手机号包含"138"的客户
```

### 查看客户活跃度

```bash
# 看今天有沟通的客户（用 updated_time 过滤）
python scripts/client.py get-contacts --today --page-size 100
# → 返回今天有更新或新增的客户
```

---

## 🐛 常见问题 FAQ

**Q1: 为什么 `--today` 返回的客户数比实际多？**  
A: `--today` 用的是 `created_time` 过滤，只包括今天**新增**的客户。如果想看今天**有沟通**的客户（包括老客户），需要用 `updated_time` 过滤（待实现）。

**Q2: 如何获取总客户数？**  
A: 执行 `get-contacts --page-size 1`，看输出中的"总计"，API 会返回 `data.total` 字段。

**Q3: 为什么有时候返回的客户数是 0？**  
A: 检查：
- Token 和 Project ID 是否正确
- 渠道 ID 是否存在
- 时间范围是否正确

**Q4: 如何批量导出所有客户？**  
A: 分页查询，循环调用：
```bash
python scripts/client.py get-contacts --page 1 --page-size 100
python scripts/client.py get-contacts --page 2 --page-size 100
# ... 直到返回的客户数 < 100
```

---

## 🤖 AI 使用指南

### 如何调用新接口

当用户请求的功能没有封装命令时：

**步骤 1：查询 llms.txt**
```
访问：https://salesmartly-api.apifox.cn/llms.txt
查找：相关接口文档链接
```

**步骤 2：使用 api-call 命令**
```bash
# 格式
python3 scripts/client.py api-call <接口路径> --param1 value1 --param2 value2

# 示例：查询分流链接
python3 scripts/client.py api-call split-link/get-list --page 1
```

**步骤 3：解析返回结果**
```python
# api-call 返回 JSON 格式
{
  "code": 0,
  "data": { "list": [...], "total": 123 },
  "msg": "success"
}
```

### 常见 AI 使用场景

| 用户需求 | AI 操作 |
|---------|--------|
| "查一下今天新增客户" | `get-contacts --today` |
| "看看客服团队有谁" | `get-members` |
| "查张三的聊天记录" | `get-contacts --keyword "张三"` → `get-messages --chat-user-id xxx` |
| "我们有哪些分流链接" | `api-call split-link/get-list` |
| "查 WhatsApp 设备列表" | `api-call whatsapp-app/get-list` |

---

## 🐛 故障排查

### 问题 1：环境变量未设置

**错误信息：**
```
错误：请设置环境变量 SALESMARTLY_API_TOKEN
```

**解决方法：**
```bash
export SALESMARTLY_API_TOKEN="你的 Token"
export SALESMARTLY_PROJECT_ID="你的项目 ID"
```

---

### 问题 2：API Token 无效

**错误信息：**
```json
{"code": 100, "message": "Invalid API Token"}
```

**解决方法：**
1. 检查 Token 是否正确（项目设置 → 企业开发设置）
2. 确认 Token 未过期
3. 重新生成 Token

---

### 问题 3：返回数据为空

**错误信息：**
```
找到 0 个客户
总计：0 个客户
```

**可能原因：**
- 查询条件太严格（如今天没有新增客户）
- 渠道 ID 不存在
- 时间范围不正确

**解决方法：**
1. 放宽查询条件（去掉 `--today` 或 `--channel`）
2. 检查渠道 ID 是否在对照表中
3. 确认时间范围正确

---

### 问题 4：请求频率超限

**错误信息：**
```json
{"code": 103, "message": "API Frequency Limit"}
```

**解决方法：**
- 降低请求频率（每秒不超过 5 次）
- 添加请求间隔（`sleep 1`）
- 分批处理大量数据

---

## 完整 API 文档

如需使用脚本未封装的功能，参考 `references/api-full.md` 或使用 `api-call` 命令。

官方文档：
- **AI 可读格式：** https://salesmartly-api.apifox.cn/llms.txt
- [API 使用指南](https://help.salesmartly.com/docs/api-use)
- [签名说明](https://help.salesmartly.com/docs/obtain-instructions-for-the-header-parameter-of-api)
- [完整 API 文档](https://salesmartly-api.apifox.cn/)

**提示：** AI 可通过 llms.txt 自主查询接口文档并调用 `api-call` 命令。

---

## 📝 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-03-05 | 初始版本（只读查询） |
| | | - 封装 5 个查询命令 |
| | | - 添加 `api-call` 通用命令 |
| | | - 删除写入类命令 |
| | | - 添加 AI 使用指南 |

### 更新日志

**v1.0 (2026-03-05)**
- ✅ 设计原则：只读优先、常用 + 通用、AI 友好
- ✅ 封装命令：`get-contacts`, `get-contact`, `get-messages`, `get-all-messages`, `get-members`
- ✅ 通用命令：`api-call`（调用任意 API）
- ✅ 文档：llms.txt 引用、AI 使用指南、故障排查
- ❌ 移除：`send-message`, `assign-chat`, `get-channels`

---

**文档最后更新：** 2026-03-05  
**维护者：** OpenClaw 社区  
**许可证：** 同 OpenClaw
