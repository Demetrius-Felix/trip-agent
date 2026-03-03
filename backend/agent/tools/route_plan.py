import httpx
from langchain_core.tools import tool

from utils.config_handler import api_key_conf


@tool(description="查询两个地点之间的驾车路线，例如：从成都东站到宽窄巷子")
def route_plan(origin: str, destination: str, city: str) -> str:
    """
    查询驾车路线
    """

    api_key = api_key_conf['GAODE_API_KEY']

    # 先把地址转成经纬度
    geo_url = "https://restapi.amap.com/v3/geocode/geo"

    def geocode(address):
        params = {
            "key": api_key,
            "address": address,
            "city": city
        }
        resp = httpx.get(geo_url, params=params)
        data = resp.json()
        if data.get("status") == "1" and data.get("geocodes"):
            return data["geocodes"][0]["location"]
        return None

    origin_loc = geocode(origin)
    dest_loc = geocode(destination)

    if not origin_loc or not dest_loc:
        return "地址解析失败"

    url = "https://restapi.amap.com/v3/direction/driving"

    params = {
        "key": api_key,
        "origin": origin_loc,
        "destination": dest_loc
    }

    response = httpx.get(url, params=params)
    data = response.json()

    if data.get("status") != "1":
        return f"路线查询失败: {data.get('info')}"

    route_info = data.get("route") or {}
    paths = route_info.get("paths") or []
    if not paths:
        return f"路线查询失败: {data.get('info') or '未返回路径数据'}"

    route = paths[0]

    distance = int(route.get("distance") or 0) / 1000
    duration = int(route.get("duration") or 0) / 60


    return (
        f"从 {origin} 到 {destination}：\n"
        f"距离约 {distance:.1f} 公里\n"
        f"预计耗时约 {duration:.0f} 分钟"
    )

if __name__ == '__main__':
    print(route_plan("王府井", "颐和园", "北京"))