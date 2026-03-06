# SaleSmartly API 完整文档 (V2 新版)

> 官方文档：https://salesmartly-api.apifox.cn/

---

## ⚠️ 重要：API 响应结构

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
# ✅ 正确
total = result['data']['total']

# ❌ 错误：不要用 page × page_size 计算
```

**适用范围：**
- 客户列表接口 (`get-contact-list`)
- 消息列表接口 (`get-message-list`)
- 渠道列表接口 (`channel/get-list`)
- 所有返回 `list` 的接口

---

## 基础信息

**API 版本**: V2  
**API 地址**: `https://developer.salesmartly.com/api/v2`  
**认证方式**: External-Sign 签名

**签名生成步骤**:

1. 将所有请求参数按**字典序排序**（key 的字母顺序）
2. 用 `&` 拼接成字符串：`token 值&key1=value1&key2=value2...`
3. 对整个字符串做 **MD5 加密**（32 位小写）
4. 将生成的签名放在 header 里：`external-sign: <签名值>`

**示例**:

```bash
# 请求参数
project_id=fkybfq
page=1
page_size=50

# 拼接字符串（token 永远在最前面）
JzjjnvDabP861o9&page=1&page_size=50&project_id=fkybfq

# MD5 加密
cd866fd27d4c5cd0faa1421129c6df17

# Header
external-sign: cd866fd27d4c5cd0faa1421129c6df17
```

---

## 客户相关接口 (V2)

### 获取客户列表

```
GET /api/v2/get-contact-list
```

**必填参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目 ID |
| page | int | 页数 |
| page_size | int | 每页数量（最大 100） |
| updated_time | JSON | 客户更新时间 `{"start": 123, "end": 456}` |

**可选参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| chat_user_id | string | 客户 ID |
| name | string | 名称（搜索关键词） |
| phone | string | 手机号码 |
| email | string | 邮箱 |
| channel | int | 渠道 ID（见下方渠道列表） |
| created_time | JSON | 客户创建时间范围 |
| sys_user_id | int | 接待成员 ID（0-未分配/-1 机器人/客服 ID） |

**渠道 ID 列表：**

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

**完整渠道列表（channel 参数可选值）：**

1. Messenger
2. 聊天插件
3. Email
4. Telegram Bot
5. Instagram
6. Line
7. WhatsApp Api
8. Facebook 主页评论
10. Slack
11. 企业微信
12. WhatsApp App
13. Instagram 评论
15. Telegram App
16. TikTok App
17. TikTok 评论
18. Vkontakte
19. Zalo App
20. TikTok Business
21. TikTok Business 评论

**响应**:
```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "chat_user_id": "abc123",
        "name": "张三",
        "remark_name": "备注名",
        "phone": "+8613800138000",
        "email": "zhangsan@example.com",
        "country": "cn",
        "city": "beijing",
        "channel": "2",
        "channel_id": "44539",
        "channel_name": "SS 官网",
        "is_online": "0",
        "created_time": "1772602299",
        "msg_last_send_time": "1772602299"
      }
    ],
    "total": 170226,
    "page": 1,
    "page_size": 50
  },
  "msg": "Success"
}
```

---

### 获取客户详情

```
GET /api/chat-user/get-contact-list?ids=<chat_user_id>
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ids | string | 是 | 客户聊天 ID（多个用逗号分隔） |

---

### 更新客户资料

```
POST /api/chat-user/update
```

**请求体**:
```json
{
  "chat_user_id": "abc123",
  "name": "张三更新",
  "phone": "+8613800138000",
  "email": "new@example.com",
  "remark": "备注信息"
}
```

---

## 消息相关接口 (V2)

### 获取聊天记录列表（指定用户）

```
GET /api/v2/get-message-list
```

**必填参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目 ID |
| chat_user_id | string | 用户 ID |
| page_size | int | 页面大小（最大 100） |

**可选参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| start_sequence_id | string | 开始的消息 ID |
| end_sequence_id | string | 结束的消息 ID |
| updated_time | JSON | 消息更新时间范围 |

**返回字段**:
- `sender_type`: 发送人类型（1-用户，2-团队成员，3-系统）
- `msg_type`: 消息类型（1-文本，2-图片，3-模板，4-文件，6-视频，8-系统消息）
- `text`: 消息文本内容
- `send_time`: 发送时间（时间戳）

**响应**:
```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "content": "你好，我想咨询产品价格",
        "direction": "received",
        "type": "text",
        "created_time": "1772602299"
      }
    ]
  }
}
```

---

### 发送消息

```
POST /api/chat-message/send
```

**请求体**:
```json
{
  "chat_user_id": "abc123",
  "content": "您好，有什么可以帮您？",
  "type": "text"
}
```

**消息类型**:
- `text` - 文本消息
- `image` - 图片消息（content 为图片 URL）
- `file` - 文件消息（content 为文件 URL）

---

## 会话相关接口 (V2)

### 会话分配接口

```
POST /api/v2/assign-chat-user
```

**请求体** (multipart/form-data):
| 参数 | 说明 | 必填 |
|------|------|------|
| session_id | 会话 ID | 是 |
| chat_user_id | 访客 ID | 是 |
| project_id | 项目 ID | 是 |
| sys_user_id | 当前接待客服 ID（存在客服 ID 传 ID，不存在传 -1） | 是 |
| assign_sys_user_id | 即将接待的客服 ID | 是 |

---

## 渠道相关接口

### 获取渠道列表

```
GET /api/channel/get-list
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": "44539",
        "name": "官网预约演示专用插件",
        "type": "plugin",
        "status": 1,
        "phone": ""
      }
    ]
  }
}
```

**常见渠道类型**:
| ID | 类型 | 说明 |
|----|------|------|
| 1 | Messenger | Facebook Messenger |
| 2 | plugin | 网站聊天插件 |
| 3 | email | 邮件 |
| 4 | telegram_bot | Telegram Bot |
| 5 | instagram | Instagram |
| 7 | whatsapp_api | WhatsApp Business API |
| 11 | work_weixin | 企业微信 |
| 12 | whatsapp_app | WhatsApp App |
| 15 | telegram_app | Telegram App |

---

## 错误响应码

详见 `references/response-codes.md`

---

## 使用注意

1. **频率限制**: API 有请求频率限制，建议控制请求间隔
2. **Token 有效期**: Token 过期需重新生成
3. **page-size 限制**: 最大值为 100
4. **时间戳**: 所有时间字段都是 Unix 时间戳（秒）
