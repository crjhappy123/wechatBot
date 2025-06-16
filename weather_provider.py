# wechat_daily_bot/weather_provider.py
import os
import requests
import openai


def get_weather():
    try:
        api_key = os.environ.get("QWEATHER_API_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "⚠️ 缺少和风天气 API Key 环境变量 QWEATHER_API_KEY"
        if not openai_api_key:
            return "⚠️ 缺少 OpenAI API Key 环境变量 OPENAI_API_KEY"

        location = "101190104"  # 南京市江宁区
        host = "https://n749vgt7bu.re.qweatherapi.com"

        now_url = f"{host}/v7/weather/now?location={location}&key={api_key}"
        air_url = f"{host}/v7/air/now?location={location}&key={api_key}"
        indices_url = f"{host}/v7/indices/1d?location={location}&type=3,5,8&key={api_key}"
        forecast_url = f"{host}/v7/weather/3d?location={location}&key={api_key}"

        now_resp = requests.get(now_url)
        air_resp = requests.get(air_url)
        indices_resp = requests.get(indices_url)
        forecast_resp = requests.get(forecast_url)

        if now_resp.status_code != 200 or now_resp.json().get("code") != "200":
            return f"⚠️ 获取天气失败：{now_resp.json()}"
        if air_resp.status_code != 200 or air_resp.json().get("code") != "200":
            return f"⚠️ 获取空气质量失败：{air_resp.json()}"
        if indices_resp.status_code != 200 or indices_resp.json().get("code") != "200":
            return f"⚠️ 获取指数失败：{indices_resp.json()}"
        if forecast_resp.status_code != 200 or forecast_resp.json().get("code") != "200":
            return f"⚠️ 获取天气预报失败：{forecast_resp.json()}"

        now_data = now_resp.json()["now"]
        air_data = air_resp.json()["now"]
        indices_data = indices_resp.json().get("daily", [])
        forecast_data = forecast_resp.json()["daily"][0]  # 今日预报

        indices_map = {int(i.get("type")): i.get("category", "未知") for i in indices_data}
        uv_level = indices_map.get(5, "未知")
        sport_suggestion = indices_map.get(8, "无")
        dressing_suggestion = indices_map.get(3, "无")

        summary = (
            f"{now_data.get('text', '未知')}，气温 {now_data.get('temp', '?')}℃，"
            f"湿度 {now_data.get('humidity', '?')}%，风力 {now_data.get('windScale', '?')}级；\n"
            f"空气质量：{air_data.get('category', '未知')}，PM2.5：{air_data.get('pm2p5', '?')}；\n"
            f"紫外线强度：{uv_level}；\n"
            f"今日预报：{forecast_data.get('textDay')}转{forecast_data.get('textNight')}，"
            f"最高 {forecast_data.get('tempMax')}℃，最低 {forecast_data.get('tempMin')}℃；\n"
            f"👕 穿衣建议：{dressing_suggestion}，🏃 运动建议：{sport_suggestion}"
        )

        # 提问 GPT 获取进一步建议
        openai.api_key = openai_api_key
        prompt = (
            f"今天南京江宁区天气：{summary}。请基于此提供穿衣建议和运动建议，控制在80字以内，语言亲切自然。"
        )
        try:
            gpt_resp = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            gpt_tip = gpt_resp.choices[0].message.content.strip()
        except Exception as e:
            gpt_tip = f"（⚠️ GPT建议生成失败：{e}）"

        return summary + "\n🤖 ChatGPT建议：" + gpt_tip

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
