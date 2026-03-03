import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.factory import embed_model
from utils.config_handler import chroma_conf
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.log_handler import logger
from utils.path_tool import get_abs_path


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['collection_name'],
            embedding_function=embed_model,
            persist_directory=chroma_conf['persist_directory'],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf['chunk_size'],
            chunk_overlap=chroma_conf['chunk_overlap'],
            separators=chroma_conf['seperator'],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf['k']})

    def load_document(self):
        """
        将文件读取为Document文档, 存入向量库中
        """

        # 检查文件md5值是否已经存在
        def check_md5_hex(md5_for_check: str) -> bool:
            if not os.path.exists(get_abs_path(chroma_conf['md5_hex_store'])):
                # 创建文件
                open(get_abs_path(chroma_conf['md5_hex_store']), 'w').close()
                return False

            with open(get_abs_path(chroma_conf['md5_hex_store']), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf['md5_hex_store']), 'a', encoding='utf-8') as f:
                f.write(md5_for_check + '\n')

        # 将文件加载为Document文档
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        # data路径下所有允许后缀的文件列表
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf['data_path']),
            tuple(chroma_conf['allow_knowledge_file_type'])
        )

        # 处理列表中每个文件
        for path in allowed_files_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在于知识库内, 跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容, 跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容, 跳过")
                    continue

                # 将内容存入向量库中
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5值
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path}内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}内容加载失败, {str(e)}", exc_info=True)


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()