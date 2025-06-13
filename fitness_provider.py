import openai
import os
import time
from openai import OpenAI, RateLimitError

def get_fitness_tip():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "请为一位普通南京市民生成今日的健身饮食建议，控制在60字以内。"
    models = ["gpt-4o", "gpt-3.5-turbo"]

    for model in models:
        for attempt in range(2):  # 每个模型最多重试2次
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except RateLimitError:
                if model == "gpt-4o" and attempt == 1:
                    break  # 跳到 gpt-3.5 尝试
                time.sleep(8)  # 等待时间可调
            except Exception as e:
                return f"❌ 今日建议生成失败：{str(e)}"

    return "❌ 今日建议生成失败：gpt-4o 和 gpt-3.5-turbo 均请求过于频繁，请稍后重试"
