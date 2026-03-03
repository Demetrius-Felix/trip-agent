import hashlib
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.log_handler import logger


def get_file_md5_hex(filepath: str):      # 获取文件的md5的十六进制字符串
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    md5_obj = hashlib.md5()

    chunk_size = 4096       # 4KB分片，避免文件过大爆内存
    try:
        with open(filepath, "rb") as f:     # 二进制方式读取
            while chunk := f.read(chunk_size):     # 先赋值后判断（类似于do while）
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败, {str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_type: tuple[str]):     # 返回文件夹内的文件列表（允许的文件后缀）
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]路径{path}不是文件夹")
        return allowed_type

    for f in os.listdir(path):
        if f.endswith(allowed_type):
            files.append(os.path.join(path, f))     # 将文件全路径加入列表

    return tuple(files)

def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()