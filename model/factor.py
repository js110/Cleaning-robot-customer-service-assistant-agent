import os
from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms.tongyi import Tongyi
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from utils.config_handler import rag_config


def get_dashscope_api_key() -> str:
    api_key = (os.getenv("DASHSCOPE_API_KEY") or rag_config.get("dashscope_api_key") or "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing DashScope API key. Set DASHSCOPE_API_KEY in your environment "
            "or configure dashscope_api_key in config/rag.yml."
        )
    return api_key


class BaseModelFactor(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactor(BaseModelFactor):

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=rag_config['chat_model_name'],
            dashscope_api_key=get_dashscope_api_key(),
        )


class EmbedModelFactor(BaseModelFactor):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_config['embedding_model_name'],
            dashscope_api_key=get_dashscope_api_key(),
        )


chat_model = ChatModelFactor().generator()
embedding_model = EmbedModelFactor().generator()
