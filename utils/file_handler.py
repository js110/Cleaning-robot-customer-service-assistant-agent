import hashlib

from utils.logger_handler import logger
import os.path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


# md5用来去重的
def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath} does not exist")
        return ()
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            md5_obj.update(chunk)

        return md5_obj.hexdigest()


# 返回文件夹下允许的文件类型的文件
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return None
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.abspath(os.path.join(path, f)))
    return tuple(files)


def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath,encoding="utf-8").load()
