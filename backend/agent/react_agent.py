import asyncio
from langchain.agents import create_agent

from agent.tools.get_weather import get_weather
from agent.tools.poi_search import search_poi
from agent.tools.route_plan import route_plan
from models.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.rag_tool import rag_summarize


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, search_poi, route_plan],
            middleware=[],
        )

    async def execute_stream(self, messages: list[dict[str, str]]):
        input_dict = {"messages": messages}

        async for chunk in self.agent.astream(input_dict, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            content = latest_message.content
            msg_type = getattr(latest_message, "type", None)
            if msg_type not in {"ai", "assistant"}:
                continue
            if isinstance(content, str) and content:
                yield content

if __name__ == '__main__':
    agent = ReactAgent()

    async def main():
        async for chunk in agent.execute_stream([{"role": "user", "content": "你好"}]):
            print(chunk, end="", flush=True)

    asyncio.run(main())
