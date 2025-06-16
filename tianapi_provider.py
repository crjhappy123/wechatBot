# wechat_daily_bot/tianapi_provider.py

import os
import requests

TIAN_API_BASE = "https://apis.tianapi.com"
TIAN_API_KEY = os.environ.get("TIAN_API_KEY")

ENDPOINTS = {
    "caipu": "/caipu/index",
    "zaoan": "/zaoan/index",
    "health": "/health/index",
    "chengyu": "/chengyu/index",
    "lishi": "/lishi/index",
    "guonei": "/guonei/index"
}

def get_tianapi_data(name):
    if name not in ENDPOINTS:
        return f"❌ 无效的接口名：{name}"

    url = f"{TIAN_API_BASE}{ENDPOINTS[name]}"
    params = {
        "key": TIAN_API_KEY,
        "num": 5 if name == "caipu" else 3 if name in ["health", "guonei"] else 1
    }

    try:
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 200:
            return f"❌ {name} 接口错误：{data.get('msg')}"

        result = data.get("result", {})
        items = result.get("list", [])

        if name == "caipu":
            return items  # 返回完整列表让 main.py 随机选择

        elif name == "zaoan":
            item = items[0]
            return f"{item.get('content')} — {item.get('note')}"

        elif name == "health":
            return [item.get("title") for item in items if item.get("title")]

        elif name == "chengyu":
            item = items[0]
            return f"{item.get('chengyu')}：{item.get('content')}"

        elif name == "lishi":
            item = items[0]
            return f"{item.get('title')}（{item.get('year')}年）"

        elif name == "guonei":
            return [item.get("title") for item in items if item.get("title")]

        else:
            return f"⚠️ 未知处理逻辑：{name}"

    except Exception as e:
        return f"❌ {name} 获取失败：{str(e)}"
