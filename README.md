# SaleSmartly Skill for OpenClaw

📊 SaleSmartly API 集成技能（只读查询），用于 OpenClaw AI 助手。

## 功能特性

- ✅ **只读查询** - 客户查询、消息查询、团队查询
- ✅ **AI 友好** - 支持通过 llms.txt 自主查询新接口
- ✅ **易于扩展** - 新增 API 无需更新代码
- ✅ **安全可靠** - 只封装查询类接口，避免误操作

## 安装方法

### 方式 1：克隆到 OpenClaw skills 目录

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/YOUR_USERNAME/salesmartly_skill.git
```

### 方式 2：手动复制

```bash
cp -r /path/to/salesmartly_skill ~/.openclaw/workspace/skills/
```

## 快速开始

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

### 2. 获取 API Token

1. 登录 SaleSmartly 后台
2. 进入 **项目设置** → **企业开发设置**
3. 生成 **API Token**
4. 在项目首页查看 **Project ID**

### 3. 测试使用

```bash
cd ~/.openclaw/workspace/skills/salesmartly_skill

# 查询客户
python3 scripts/client.py get-contacts --page-size 5

# 查询今天新增客户
python3 scripts/client.py get-contacts --today

# 查询客服团队
python3 scripts/client.py get-members

# 调用任意 API
python3 scripts/client.py api-call get-member-list -p page=1 -p page_size=10
```

## 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `get-contacts` | 获取客户列表 | `--today --channel 2` |
| `get-contact` | 获取客户详情 | `--chat-user-id xxx` |
| `get-messages` | 获取指定客户消息 | `--chat-user-id xxx --limit 20` |
| `get-all-messages` | 获取全量消息 | `--page 1 --page-size 50` |
| `get-members` | 获取团队成员 | `--page 1 --page-size 20` |
| `api-call` | 调用任意 API | `get-member-list -p page=1` |

## 使用示例

### 查看今天新增客户

```bash
python3 scripts/client.py get-contacts --today --page-size 100
```

### 查看某个客户的聊天记录

```bash
# 先查客户 ID
python3 scripts/client.py get-contacts --keyword "张三"

# 再查消息
python3 scripts/client.py get-messages --chat-user-id "abc123" --limit 20
```

### 查看客服团队

```bash
python3 scripts/client.py get-members --page 1
```

### 调用未封装的 API

```bash
# AI 可通过 llms.txt 查询接口文档后调用
python3 scripts/client.py api-call split-link/get-list -p page=1
```

## 项目结构

```
salesmartly_skill/
├── README.md              # 本文档
├── SKILL.md               # OpenClaw 技能文档（详细说明）
├── scripts/
│   └── client.py          # Python CLI 工具
└── references/
    ├── api-full.md        # API 完整文档
    └── response-codes.md  # 错误码文档
```

## API 文档

- **AI 可读格式：** https://salesmartly-api.apifox.cn/llms.txt
- **官方文档：** https://salesmartly-api.apifox.cn/
- **签名说明：** https://help.salesmartly.com/docs/obtain-instructions-for-the-header-parameter-of-api

## 设计理念

1. **只读优先** - 只封装查询类接口，避免误操作
2. **常用 + 通用** - 高频接口封装命令，低频接口用 `api-call`
3. **AI 友好** - 通过 llms.txt 自主查询新接口
4. **易于维护** - 接口增加不需要频繁更新脚本

## 常见问题

### Q: 如何获取总客户数？

A: 执行 `get-contacts --page-size 1`，API 会返回 `data.total` 字段。

### Q: 为什么返回的客户数是 0？

A: 检查：
- Token 和 Project ID 是否正确
- 查询条件是否太严格
- 渠道 ID 是否存在

### Q: 如何调用新接口？

A: 使用 `api-call` 命令：
```bash
python3 scripts/client.py api-call <接口路径> -p 参数=值
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

同 OpenClaw 项目许可证。

---

**最后更新：** 2026-03-05  
**维护者：** OpenClaw 社区
