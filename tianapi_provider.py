import os
import requests


def get_tianapi_data(api_name):
    import os  # 添加漏导入的模块
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
            item = data.get("result", {}).get("list", [{}])[0]
            name = item.get("cp_name") or item.get("name") or item.get("title") or "未知菜名"
            content = item.get("zuofa") or item.get("content") or item.get("description") or "暂无描述"
            return f"{name} - {content}"
        elif api_name == "zaoan":
            return f"{data['result']['content']}"
        elif api_name == "health":
            return f"{data['result']['list'][0]['content']}"
        elif api_name == "chengyu":
            item = data['result']['list'][0]
            return f"{item['chengyu']} - {item['content']}"
        elif api_name == "lishi":
            item = data['result']['list'][0]
            return f"{item['title']}"
        elif api_name == "guonei":
            item = data['result']['newslist'][0]
            return f"{item['title']}"
        elif api_name == "guonei":
            items = data.get('result', {}).get('newslist', [])[:3]
            titles = [item.get('title', '').strip() for item in items if item.get('title')]
        if not titles:
            return "📰 国内新闻：暂无"
    return "📰 国内新闻：\n- " + "\n- ".join(titles)
        else:
            return f"✅ {api_name} 接口返回成功"
    except Exception as e:
        return f"❌ 获取{api_name}失败：{str(e)}"
