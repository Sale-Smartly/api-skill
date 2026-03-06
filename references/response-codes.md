# SaleSmartly API 响应码文档

> 来源：https://salesmartly-api.apifox.cn/

---

## ✅ 成功状态码

| 响应码 | 中文含义 | 英文描述 | 处理建议 |
|--------|----------|----------|----------|
| 0 | 请求成功 | Success | 正常处理返回数据 |

---

## 🔐 认证与授权错误

| 响应码 | 中文含义 | 英文描述 | 处理建议 |
|--------|----------|----------|----------|
| 100 | 无效的 API Token | Invalid API Token | 检查 API Token 是否正确配置 |
| 101 | 无效的访问令牌 | Invalid Bearer Token | 重新获取有效的 Bearer Token |
| 102 | 无效的 External-Sign 签名 | Invalid External Sign | 验证签名算法和密钥是否正确 |
| 103 | API 请求频率超出限制 | API Frequency Limit | 降低请求频率，增加间隔 |

---

## 🏢 业务逻辑错误

| 响应码 | 中文含义 | 英文描述 | 处理建议 |
|--------|----------|----------|----------|
| 201 | 社媒渠道不存在 | Channel Not Exist | 确认渠道 ID 是否正确 |
| 202 | 社媒渠道信息不存在 | Channel Info Not Exist | 检查渠道配置信息 |
| 203 | 社媒渠道用户已存在 | Channel User Exist | 使用更新接口而非创建接口 |
| 204 | 新增客户失败 | Create Contact Failed | 检查客户信息格式和必填字段 |
| 205 | 更新客户资料失败 | Update Contact Failed | 验证数据格式 |
| 206 | 新增订单已存在 | Chat Order Exist | 检查订单唯一性约束 |
| 207 | WhatsApp 个号无法启动 | Individual Whatsapp Can't Start | 检查传参是否正确，个号是否是未连接状态 |
| 208 | WhatsApp 个号已启动 | Individual Whatsapp Is Start | 个号已经连接了，换未连接的号 |
| 209 | 会话信息不存在 | Chat Session Not Exist | 根据条件查询的会话信息不存在，请检查传参 |
| 210 | 分配指定成员不存在 | Sys User Not Exist | 检查分配的成员 id 是否正确 |
| 211 | 分流链接不存在 | Split Link Not Exist | 检查传入参数是否正确 |
| 212 | 项目可用消耗不足 | Project Consume Not Enough | 检查需要新增的设备额度是否充足 |
| 213 | WhatsApp 可用服务器不足 | Whatsapp Server Not Enough | 反馈给 SaleSmartly 官方增加服务器 |
| 214 | WhatsApp 个人号不存在 | Individual Whatsapp Not Exist | 检查传入参数是否正确 |
| 215 | 设备代理配置有误 | Proxy Config Error | 检查配置是否可用 |
| 216 | 数据库异常 | Redis Lock Error | 请找技术人员协助排查 |
| 217 | 请勿频繁操作 | Is Operation Now | 避免频繁操作，稍后重试 |
| 218 | 社媒渠道用户不存在 | Channel User Not Exist | 请检查该社媒渠道用户是否存在 |

---

## ⚠️ 系统错误

| 响应码 | 中文含义 | 英文描述 | 处理建议 |
|--------|----------|----------|----------|
| 400 | 参数有误 | Invalid Params | 检查请求参数格式和必填项 |
| 500 | 数据库错误 | Database Error | 联系技术支持处理 |
| 600 | 创建用户失败 | Create User Error | 检查用户信息完整性 |
| 601 | 创建授权码失败 | Create Login Code Error | 重试或联系技术支持 |

---

## 快速排查指南

**认证问题 (100-103)**:
1. 检查 `SALESMARTLY_API_TOKEN` 环境变量
2. 确认 Token 未过期
3. 降低请求频率

**业务问题 (200-218)**:
1. 确认传入的 ID 参数正确
2. 检查资源是否存在
3. 查看账号额度是否充足

**系统问题 (400-601)**:
1. 检查请求参数格式
2. 稍后重试
3. 联系 SaleSmartly 技术支持
