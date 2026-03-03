import httpx
from langchain_core.tools import tool

from utils.config_handler import api_key_conf


REQUEST_TIMEOUT = 8


@tool(description="查询两个地点之间的驾车路线，例如：从成都东站到宽窄巷子")
def route_plan(origin: str, destination: str, city: str) -> str:
    """
    查询驾车路线
    """
    origin = (origin or "").strip()
    destination = (destination or "").strip()
    city = (city or "").strip()

    if not origin or not destination or not city:
        return "路线查询失败：origin、destination、city 不能为空"

    api_key = api_key_conf["GAODE_API_KEY"]
    geo_url = "https://restapi.amap.com/v3/geocode/geo"

    def geocode(address: str):
        params = {
            "key": api_key,
            "address": address,
            "city": city,
        }
        resp = httpx.get(geo_url, params=params, timeout=REQUEST_TIMEOUT)
        data = resp.json()
        geocodes = data.get("geocodes") or []
        if data.get("status") == "1" and geocodes:
            return geocodes[0].get("location")
        return None

    try:
        origin_loc = geocode(origin)
        dest_loc = geocode(destination)

        if not origin_loc or not dest_loc:
            return f"地址解析失败：无法识别 {origin} 或 {destination}"

        url = "https://restapi.amap.com/v3/direction/driving"
        params = {
            "key": api_key,
            "origin": origin_loc,
            "destination": dest_loc,
        }

        response = httpx.get(url, params=params, timeout=REQUEST_TIMEOUT)
        data = response.json()

        if data.get("status") != "1":
            return f"路线查询失败: {data.get('info') or '服务异常'}"

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
    except httpx.TimeoutException:
        return "路线查询超时：请稍后重试，或先提供更精确的起终点名称"
    except Exception as e:
        return f"路线查询异常: {str(e)}"


if __name__ == '__main__':
    print(route_plan("王府井", "颐和园", "北京"))