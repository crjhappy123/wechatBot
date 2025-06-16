import os
import requests

def get_tianapi_data(api_name):
    api_key = os.environ.get("TIAN_API_KEY")
    if not api_key:
        return f"⚠️ 缺少天行数据 API Key"

    url = f"https://apis.tianapi.com/{api_name}/index?key={api_key}"
    try:
        resp = requests.get(url)
        data = resp.json()
        if data.get("code") != 200:
            return f"⚠️ 获取{api_name}失败"

        if api_name == "caipu":
            item = data["result"]["list"][0]
            return f"🥗 今日菜谱：{item.get('name')} - {item.get('content')}"
        elif api_name == "zaoan":
            return f"📖 每日一句：{data['result']['content']}"
        elif api_name == "health":
            return f"🧘 健康养生：{data['result']['list'][0]['content']}"
        elif api_name == "chengyu":
            item = data['result']['list'][0]
            return f"📚 成语：{item['chengyu']} - {item['content']}"
        elif api_name == "lishi":
            item = data['result']['list'][0]
            return f"📅 历史上的今天：{item['title']}"
        else:
            return f"✅ {api_name} 接口返回成功"
    except Exception as e:
        return f"❌ 获取{api_name}失败：{str(e)}"
