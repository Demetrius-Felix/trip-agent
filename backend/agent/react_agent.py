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

    @staticmethod
    def _extract_text(content) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if isinstance(block, str):
                    parts.append(block)
                    continue

                if isinstance(block, dict):
                    text = block.get("text")
                    if isinstance(text, str):
                        parts.append(text)
                    continue

                text = getattr(block, "text", None)
                if isinstance(text, str):
                    parts.append(text)

            return "".join(parts)

        return ""

    async def execute_stream(self, messages: list[dict[str, str]]):
        input_dict = {"messages": messages}
        last_full_text = ""

        async for chunk in self.agent.astream(input_dict, stream_mode="values"):
            all_messages = chunk.get("messages") or []
            if not all_messages:
                continue

            latest_message = all_messages[-1]
            msg_type = getattr(latest_message, "type", None)
            if msg_type not in {"ai", "assistant"}:
                continue

            full_text = self._extract_text(getattr(latest_message, "content", ""))
            if not full_text:
                continue

            if full_text.startswith(last_full_text):
                delta = full_text[len(last_full_text):]
            else:
                delta = full_text

            last_full_text = full_text
            if delta:
                yield delta


if __name__ == '__main__':
    agent = ReactAgent()

    async def main():
        async for chunk in agent.execute_stream([{"role": "user", "content": "你好"}]):
            print(chunk, end="", flush=True)

    asyncio.run(main())
