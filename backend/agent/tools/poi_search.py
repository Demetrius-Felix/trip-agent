# 兴趣点搜索
import httpx
from langchain_core.tools import tool

from utils.config_handler import api_key_conf


@tool(description="搜索某个城市的景点、美食或酒店，例如：成都火锅、北京故宫")
def search_poi(keyword: str, city: str) -> str:
    """
    使用高德 POI 搜索
    :param keyword: 搜索关键词，如 火锅、景点、酒店
    :param city: 城市名称，如 成都
    """

    api_key = api_key_conf['GAODE_API_KEY']

    url = "https://restapi.amap.com/v3/place/text"

    params = {
        "key": api_key,
        "keywords": keyword,
        "city": city,
        "offset": 5,  # 返回前5个
        "page": 1,
        "extensions": "base"
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "1":
            return f"POI 查询失败: {data.get('info')}"

        pois = data.get("pois", [])

        if not pois:
            return f"未找到 {city} 的 {keyword}"

        result = f"{city} 推荐的 {keyword}：\n\n"

        for i, poi in enumerate(pois, 1):
            result += (
                f"{i}. {poi['name']}\n"
                f"地址: {poi['address']}\n"
                f"类型: {poi['type']}\n\n"
            )

        return result

    except Exception as e:
        return f"POI 查询异常: {str(e)}"

if __name__ == '__main__':
    print(search_poi("火锅", "成都"))