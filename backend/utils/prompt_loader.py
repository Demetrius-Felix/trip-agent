from utils.config_handler import prompts_conf
from utils.log_handler import logger
from utils.path_tool import get_abs_path


def load_system_prompt():
    # 获取系统提示词文件的绝对路径
    try:
        system_prompt_path = get_abs_path(prompts_conf['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompt]yaml文件中没有main_prompt_path配置项")
        raise e

    # 读取文件内容
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]解析系统提示词出错, {str(e)}")
        raise e

def load_rag_prompt():
    # 获取rag提示词文件的绝对路径
    try:
        rag_prompt_path = get_abs_path(prompts_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompt]yaml文件中没有rag_summarize_prompt_path配置项")
        raise e

    # 读取文件内容
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompt]解析RAG总结提示词出错, {str(e)}")
        raise e


