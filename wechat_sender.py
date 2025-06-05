# wechat_daily_bot/wechat_sender.py
import requests
import os

def send_wecom_message(content):
    webhook_url = os.environ.get("WECHAT_WEBHOOK_URL")
    if not webhook_url:
        print("缺少 WECHAT_WEBHOOK_URL 配置")
        return
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    try:
        resp = requests.post(webhook_url, json=data)
        resp.raise_for_status()
    except Exception as e:
        print("发送失败：", e)
