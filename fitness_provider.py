# wechat_daily_bot/fitness_provider.py
import openai
import os

def get_fitness_tip():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    prompt = "请为一位普通南京市民生成今日的健身饮食建议，控制在60字以内。"
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()
