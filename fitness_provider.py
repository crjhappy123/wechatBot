# wechat_daily_bot/fitness_provider.py
import openai
import os
import time
from openai import APIStatusError

def get_fitness_tip():
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "请为一位普通南京市民生成今日的健身饮食建议，控制在60字以内。"
    models = ["gpt-4o", "gpt-3.5-turbo"]

    for model in models:
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except openai.RateLimitError:
                if model == "gpt-4o" and attempt == 2:
                    break  # 继续尝试 gpt-3.5-turbo
                time.sleep(2)  # 等待后重试
            except Exception as e:
                return f"今日建议生成失败：{str(e)}"

    return "今日建议生成失败：已尝试 gpt-4o 和 gpt-3.5-turbo，但均超出速率限制或出错"
