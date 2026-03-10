"""
用户提问后，先通过 RAG 检索资料，再把问题和资料传给 LLM。
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factor import chat_model
from rag.vector_store import VectorStore
from utils.prompt_loader import loader_rag_prompts


class RagSummerizeService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = loader_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | self.model | StrOutputParser()

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def build_context(self, query: str) -> str:
        context_docs = self.retriever_docs(query)
        context_parts = []
        for index, doc in enumerate(context_docs, start=1):
            context_parts.append(
                f"[参考资料{index}: 参考资料内容 {doc.page_content} | 参考元数据: {doc.metadata}]"
            )
        return "\n".join(context_parts)

    def rag_summerize(self, query: str) -> tuple[str, str]:
        payload = {
            "input": query,
            "context": self.build_context(query),
        }
        formatted_prompt = self.prompt_template.format(**payload)
        result = self.chain.invoke(payload)
        return result, formatted_prompt


if __name__ == "__main__":
    rag = RagSummerizeService()
    query = "小户型适合哪种扫地机器人？"
    result, formatted_prompt = rag.rag_summerize(query)
    print("===== 提示词模板 =====")
    print(rag.prompt_text)
    print("===== 最终 Prompt =====")
    print(formatted_prompt)
    print("===== 模型输出 =====")
    print(result)
