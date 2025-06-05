# wechat_daily_bot/stock_provider.py
import requests

def get_stock_summary():
    url = "http://hq.sinajs.cn/list=sh000001,sz399001,sz399006"
    try:
        resp = requests.get(url)
        resp.encoding = 'gbk'
        lines = resp.text.strip().split("\n")
        index_map = {"sh000001": "上证指数", "sz399001": "深证成指", "sz399006": "创业板"}
        summary = []
        for line, code in zip(lines, index_map):
            if '"' in line:
                name, cur, open_, high, low = line.split('"')[1].split(',')[:5]
                summary.append(f"{index_map[code]}：{cur}点，开盘{open_}，高{high}，低{low}")
        return "\n".join(summary)
    except Exception:
        return "股市数据获取失败"
