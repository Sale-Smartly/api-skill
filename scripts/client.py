#!/usr/bin/env python3
"""
SaleSmartly API Client - 封装常用 API 操作（只读查询）

用法:
    python client.py <command> [options]

命令:
    get-contacts      获取客户列表
    get-contact       获取单个客户详情
    get-messages      获取指定客户消息
    get-all-messages  获取全量消息（所有客户）
    get-members       获取团队成员列表
    api-call          调用任意 SaleSmartly API

环境变量:
    SALESMARTLY_API_TOKEN   - API Token (从项目设置 - 企业开发设置获取)
    SALESMARTLY_PROJECT_ID  - 项目 ID (后台左下角查看)

注意：本脚本只封装查询类接口，写入操作请用 api-call 命令
"""

import os
import sys
import json
import hashlib
import argparse
import urllib.request
import urllib.error
from urllib.parse import urlencode
import datetime

# API 配置 - V2 新版 API
API_BASE = "https://developer.salesmartly.com/api/v2"
API_TOKEN = os.environ.get("SALESMARTLY_API_TOKEN")
PROJECT_ID = os.environ.get("SALESMARTLY_PROJECT_ID")


def check_env():
    """检查环境变量"""
    if not API_TOKEN:
        print("错误：请设置环境变量 SALESMARTLY_API_TOKEN")
        sys.exit(1)
    if not PROJECT_ID:
        print("错误：请设置环境变量 SALESMARTLY_PROJECT_ID")
        sys.exit(1)


def generate_signature(params):
    """
    生成签名
    1. Token 值永远放最前面（直接拼接值，不是 token=xxx）
    2. 其他参数按字典序排序
    3. 用 & 拼接
    4. MD5 加密 (32 位小写)
    """
    # 参数按字典序排序
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    
    # 拼接：token&key1=value1&key2=value2...
    param_str = API_TOKEN + "&" + "&".join(f"{k}={v}" for k, v in sorted_params)
    
    # MD5 加密
    signature = hashlib.md5(param_str.encode("utf-8")).hexdigest()
    
    return signature


def api_request(endpoint, method="GET", params=None, data=None):
    """发送 API 请求"""
    url = f"{API_BASE}/{endpoint}"
    
    # 基础参数（只需要 project_id）
    base_params = {
        "project_id": PROJECT_ID
    }
    
    # 合并参数
    if params:
        base_params.update(params)
    
    # 生成签名
    sign_params = base_params.copy()
    if data and method == "POST":
        # POST 请求把 body 也加入签名
        for k, v in data.items():
            sign_params[k] = json.dumps(v) if isinstance(v, dict) else str(v)
    
    external_sign = generate_signature(sign_params)
    
    # 设置 headers
    headers = {
        "Content-Type": "application/json",
        "external-sign": external_sign
    }
    
    # GET 请求参数放 URL
    if method == "GET" and base_params:
        query = urlencode(base_params)
        url = f"{url}?{query}"
        body = None
    else:
        body = json.dumps(data).encode("utf-8") if data else None
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"code": e.code, "message": f"HTTP Error: {e.reason}", "body": error_body}
    except Exception as e:
        return {"code": 500, "message": str(e)}


def format_timestamp(ts):
    """格式化时间戳"""
    if not ts:
        return "N/A"
    try:
        return datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return str(ts)


def get_contacts(page=1, page_size=50, keyword=None, today_only=False, channel=None):
    """获取客户列表 - V2 API
    
    API 响应结构:
    {
        "code": 0,
        "data": {
            "list": [...],      # 当前页客户列表
            "total": 12345,     # ← 总客户数（直接用这个！）
            "page": 1,
            "page_size": 50
        }
    }
    
    注意：不要用 page × page_size 计算总数，直接用 result['data']['total']
    """
    import time
    
    # V2 API 必填参数：page, page_size, updated_time
    today_start = int(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    params = {
        "page": str(page),
        "page_size": str(min(page_size, 100)),  # V2 最大 100
        "updated_time": json.dumps({"start": today_start, "end": int(time.time())})
    }
    
    # 可选参数
    if keyword:
        params["name"] = keyword  # V2 用 name 而不是 keyword
    if channel:
        params["channel"] = str(channel)
    
    # 如果只要今天的客户，用 created_time 过滤
    if today_only:
        params["created_time"] = json.dumps({"start": today_start, "end": int(time.time())})
    
    result = api_request("get-contact-list", params=params)
    
    if result.get("code") == 0:
        contacts = result.get("data", {}).get("list", [])
        
        print(f"找到 {len(contacts)} 个客户:")
        for c in contacts:
            chat_id = c.get('chat_user_id', 'N/A')
            name = c.get('name', c.get('remark_name', '')) or '未命名'
            phone = c.get('phone', c.get('phone_number', 'N/A'))
            created = format_timestamp(c.get('created_time'))
            channel = c.get('channel', 'N/A')
            print(f"  - ID: {chat_id}, 姓名：{name}, 手机：{phone}, 时间：{created}, 渠道 ID: {channel}")
        
        # 显示总数（直接用 API 返回的 total 字段）
        total = result.get("data", {}).get("total", 0)
        print(f"\n总计：{total} 个客户")
    else:
        print(f"查询失败：{result}")
    
    return result


def get_contact(chat_user_id):
    """获取单个客户详情"""
    params = {"ids": chat_user_id}
    result = api_request("chat-user/get-contact-list", params=params)
    
    if result.get("code") == 0:
        contacts = result.get("data", {}).get("list", [])
        if contacts:
            c = contacts[0]
            print(f"客户详情:")
            print(f"  ID: {c.get('chat_user_id')}")
            print(f"  姓名：{c.get('name', c.get('remark_name', '')) or '未命名'}")
            print(f"  手机：{c.get('phone', 'N/A')}")
            print(f"  邮箱：{c.get('email', 'N/A')}")
            print(f"  国家：{c.get('country', 'N/A')}")
            print(f"  城市：{c.get('city', 'N/A')}")
            print(f"  语言：{c.get('language', 'N/A')}")
            print(f"  在线：{'是' if c.get('is_online') == '1' else '否'}")
            print(f"  备注：{c.get('remark', 'N/A')}")
            print(f"  渠道：{c.get('channel_name', 'N/A')}")
            print(f"  创建时间：{format_timestamp(c.get('created_time'))}")
            print(f"  最后消息：{format_timestamp(c.get('msg_last_send_time'))}")
        else:
            print(f"未找到客户：{chat_user_id}")
    else:
        print(f"查询失败：{result}")
    
    return result


def get_messages(chat_user_id, limit=20):
    """获取客户消息 - V2 API"""
    params = {
        "chat_user_id": chat_user_id,
        "page_size": str(min(limit, 100))  # V2 最大 100
    }
    result = api_request("get-message-list", params=params)
    
    if result.get("code") == 0:
        messages = result.get("data", {}).get("list", [])
        print(f"最近 {len(messages)} 条消息:")
        for msg in messages:
            sender_type = msg.get("sender_type", 0)  # 1-用户 2-团队成员 3-系统
            direction = "→" if sender_type == 2 else "←"
            content = msg.get('text', '')[:50]
            created = format_timestamp(msg.get('send_time'))
            print(f"  {direction} [{created}] {content}")
    else:
        print(f"查询失败：{result}")
    
    return result


def get_all_messages(page=1, page_size=50, start_time=None, end_time=None):
    """获取全量聊天记录（所有客户）
    
    API: GET /api/v2/get-message-list (全量版)
    文档：https://salesmartly-api.apifox.cn/获取聊天记录列表全量 -385681563e0.md
    
    参数:
        page: 页码
        page_size: 每页数量（最大 100）
        start_time: 开始时间（时间戳，可选）
        end_time: 结束时间（时间戳，可选）
    """
    import time
    
    params = {
        "page": str(page),
        "page_size": str(min(page_size, 100))
    }
    
    # 可选时间范围过滤
    if start_time or end_time:
        time_range = {}
        if start_time:
            time_range["start"] = int(start_time)
        else:
            time_range["start"] = int(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        if end_time:
            time_range["end"] = int(end_time)
        else:
            time_range["end"] = int(time.time())
        params["send_time"] = json.dumps(time_range)
    
    result = api_request("get-message-list", params=params)
    
    if result.get("code") == 0:
        messages = result.get("data", {}).get("list", [])
        total = result.get("data", {}).get("total", 0)
        
        print(f"找到 {len(messages)} 条消息（总计：{total} 条）:")
        for msg in messages:
            sender_type = msg.get("sender_type", 0)  # 1-用户 2-团队成员 3-系统
            direction = "→" if sender_type == 2 else "←"
            chat_user_id = msg.get("chat_user_id", "N/A")[:8]
            content = msg.get('text', '')[:50]
            created = format_timestamp(msg.get('send_time'))
            print(f"  {direction} [{created}] 客户：{chat_user_id}... {content}")
        
        print(f"\n总计：{total} 条消息")
    else:
        print(f"查询失败：{result}")
    
    return result


def get_members(page=1, page_size=20):
    """获取团队成员列表
    
    API: GET /api/v2/get-member-list
    文档：https://salesmartly-api.apifox.cn/获取团队成员 -310397215e0.md
    
    参数:
        page: 页码
        page_size: 每页数量（最大 100）
    """
    params = {
        "page": str(page),
        "page_size": str(min(page_size, 100))
    }
    
    result = api_request("get-member-list", params=params)
    
    if result.get("code") == 0:
        members = result.get("data", {}).get("list", [])
        total = result.get("data", {}).get("total", 0)
        
        print(f"找到 {len(members)} 个团队成员:")
        for m in members:
            member_id = m.get('sys_user_id', 'N/A')
            nickname = m.get('nickname', '未命名')
            email = m.get('email', 'N/A')
            online_status = m.get('online_status', 0)  # 0-离线 1-在线 2-忙碌
            status_text = {0: '离线', 1: '在线', 2: '忙碌'}.get(online_status, '未知')
            assign_limit = m.get('assign_limit', 'N/A')
            identity = m.get('identity_name', 'N/A')
            print(f"  - ID: {member_id}, 昵称：{nickname}, 邮箱：{email}, 状态：{status_text}, 接待上限：{assign_limit}, 身份：{identity}")
        
        print(f"\n总计：{total} 个成员")
    else:
        print(f"查询失败：{result}")
    
    return result


def api_call(endpoint, **kwargs):
    """调用任意 SaleSmartly API
    
    用法:
        python client.py api-call <接口名> [--param1 value1] [--param2 value2]
    
    示例:
        python client.py api-call get-member-list --page 1 --page-size 20
        python client.py api-call get-message-list --chat-user-id xxx
    
    参数:
        endpoint: API 接口路径（如 get-member-list）
        **kwargs: 其他参数
    """
    # 分离 GET/POST 参数（简单处理：数字和字符串放 URL，JSON 对象放 body）
    params = {}
    data = None
    
    for key, value in kwargs.items():
        # 简单判断：如果是数字或简单字符串，放 URL 参数
        if isinstance(value, int) or (isinstance(value, str) and not value.startswith('{')):
            params[key] = str(value)
        else:
            # 否则尝试解析为 JSON
            try:
                if data is None:
                    data = {}
                data[key] = json.loads(value) if value.startswith('{') else value
            except:
                params[key] = value
    
    method = "POST" if data else "GET"
    result = api_request(endpoint, method=method, params=params, data=data)
    
    # 打印结果
    print(f"API 调用结果 ({endpoint}):")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result


def main():
    parser = argparse.ArgumentParser(description="SaleSmartly API Client (只读查询)")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # get-contacts
    p_contacts = subparsers.add_parser("get-contacts", help="获取客户列表")
    p_contacts.add_argument("--page", type=int, default=1, help="页码")
    p_contacts.add_argument("--page-size", type=int, default=50, help="每页数量（最大 100）")
    p_contacts.add_argument("--keyword", type=str, help="搜索关键词")
    p_contacts.add_argument("--today", action="store_true", help="只显示今天新增的客户")
    p_contacts.add_argument("--channel", type=str, help="渠道 ID 过滤")
    
    # get-contact
    p_contact = subparsers.add_parser("get-contact", help="获取单个客户详情")
    p_contact.add_argument("--chat-user-id", required=True, help="客户聊天 ID")
    
    # get-messages
    p_messages = subparsers.add_parser("get-messages", help="获取指定客户消息")
    p_messages.add_argument("--chat-user-id", required=True, help="客户聊天 ID")
    p_messages.add_argument("--limit", type=int, default=20, help="消息数量")
    
    # get-all-messages
    p_all_messages = subparsers.add_parser("get-all-messages", help="获取全量消息（所有客户）")
    p_all_messages.add_argument("--page", type=int, default=1, help="页码")
    p_all_messages.add_argument("--page-size", type=int, default=50, help="每页数量（最大 100）")
    
    # get-members
    p_members = subparsers.add_parser("get-members", help="获取团队成员列表")
    p_members.add_argument("--page", type=int, default=1, help="页码")
    p_members.add_argument("--page-size", type=int, default=20, help="每页数量（最大 100）")
    
    # api-call (通用命令)
    p_api = subparsers.add_parser("api-call", help="调用任意 SaleSmartly API")
    p_api.add_argument("endpoint", help="API 接口路径（如 get-member-list）")
    p_api.add_argument("-p", "--param", action="append", help="参数（格式：key=value，可多次使用）")
    
    args = parser.parse_args()
    
    check_env()  # 检查环境变量
    
    if args.command == "get-contacts":
        get_contacts(args.page, args.page_size, args.keyword, args.today, args.channel)
    elif args.command == "get-contact":
        get_contact(args.chat_user_id)
    elif args.command == "get-messages":
        get_messages(args.chat_user_id, args.limit)
    elif args.command == "get-all-messages":
        get_all_messages(args.page, args.page_size)
    elif args.command == "get-members":
        get_members(args.page, args.page_size)
    elif args.command == "api-call":
        # 解析额外参数
        params = {}
        if args.param:
            for p in args.param:
                if "=" in p:
                    key, value = p.split("=", 1)
                    params[key] = value
        api_call(args.endpoint, **params)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
