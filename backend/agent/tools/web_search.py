from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import os

from utils.config_handler import api_key_conf

tavily_client = TavilySearch(
    tavily_api_key=api_key_conf['TAVILY_API_KEY'],
    max_results=5,
    timeout=10
)

@tool(description="""
用于查询实时互联网信息。

适用场景：
- 实时天气
- 新闻
- 当天日期
- 政策变动
- 价格
- 开放时间
- 互联网资料

输入必须是完整的问题。
仅在本地工具无法回答时使用。
"""
)
def web_search(query: str) -> str:
    return str(tavily_client.invoke(query))