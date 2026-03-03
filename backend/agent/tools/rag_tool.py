from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    rag_service = RagSummarizeService()
    return rag_service.rag_summarize(query)