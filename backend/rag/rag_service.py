"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from models.factory import chat_model
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.__init_chain()

    def __init_chain(self):
        return self.prompt_template | print_prompt | self.model | StrOutputParser()                                                 # noqa

    def rag_summarize(self, query: str) -> str:
        # 对用户提问做相似度检索，得到相关文档
        context_docs = self.retriever.invoke(query)

        context = ""
        cnt = 0
        for doc in context_docs:
            cnt += 1
            context += f"【参考资料{cnt}】{doc.page_content} | 参考元数据: {doc.metadata}\n"

        return self.chain.invoke({"input": query, "context": context})


if __name__ == '__main__':
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("杭州旅游建议"))
