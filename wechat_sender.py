# wechat_daily_bot/wechat_sender.py
import requests
import os

def send_wecom_message(content):
    webhook_url = os.environ.get("WECHAT_WEBHOOK_URL")
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    requests.post(webhook_url, json=data)
