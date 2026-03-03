from langchain_core.tools import tool
from datetime import datetime
import pytz


@tool(description="""
获取当前真实日期和时间。
用于计算“今天”、“明天”、“未来3天”等时间相关问题。
必须在涉及时间推算时优先调用。
"""
)
def get_current_datetime() -> str:
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")