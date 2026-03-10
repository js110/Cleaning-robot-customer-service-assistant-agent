import os.path
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_chroma import Chroma
from langchain_core.documents import Document

from model.factor import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_config
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tools import get_abs_path


class VectorStore:
    def __init__(self):
        # 向量存储
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
        )
        # 文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    def load_document(self):
        def check_md5_hex(md5Str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), "w", encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_config["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5Str:
                        return True
                return False

        def save_md5_hex(md5Str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5Str + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            elif read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path = listdir_with_allowed_type(get_abs_path(chroma_config["data_path"]),
                                                       tuple(chroma_config["allow_knowledge_file_type"]),
                                                       )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内,跳过")
                continue
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本")
                    continue
                split_documents: list[Document] = self.spliter.split_documents(documents)

                if not split_documents:
                    logger.info(f"[加载知识库]{path}分片后没有有效的文本内容,跳过")
                    continue

                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}加载内容成功")
            except Exception as e:
                #    exc_info会记录详细的日志堆栈
                logger.error(f"[加载知识库]{path}加载内容失败:{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStore()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("故障")
    for re in res:
        print(re.page_content)
        print("=" * 20)
