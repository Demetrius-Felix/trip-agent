import httpx
from langchain_core.tools import tool

from utils.config_handler import api_key_conf


@tool(description="查询指定城市的实时天气情况，例如：北京、上海、广州")
def get_weather(city: str) -> str:
    """
    查询高德实时天气
    :param city: 城市名称，例如：北京
    :return: 格式化后的天气信息
    """

    api_key = api_key_conf['GAODE_API_KEY']

    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    params = {
        "key": api_key,
        "city": city,
        "extensions": "base"
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "1":
            return f"查询天气失败：{data.get('info')}"

        lives = data.get("lives", [])
        if not lives:
            return f"未找到城市 {city} 的天气信息"

        weather = lives[0]

        province = weather.get("province") or ""
        city_name = weather.get("city") or city
        weather_desc = weather.get("weather") or "未知"
        temperature = weather.get("temperature") or "未知"
        winddirection = weather.get("winddirection") or "未知"
        windpower = weather.get("windpower") or "未知"
        humidity = weather.get("humidity") or "未知"
        reporttime = weather.get("reporttime") or "未知"

        result = (
            f"{province} {city_name} 当前天气：\n"
            f"天气状况：{weather_desc}\n"
            f"温度：{temperature}℃\n"
            f"风向：{winddirection}\n"
            f"风力：{windpower}级\n"
            f"湿度：{humidity}%\n"
            f"更新时间：{reporttime}"
        )


        return result

    except Exception as e:
        return f"天气查询异常：{str(e)}"

if __name__ == '__main__':
    print(get_weather("北京"))
