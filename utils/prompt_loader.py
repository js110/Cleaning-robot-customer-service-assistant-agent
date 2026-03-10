from utils.logger_handler import logger

from utils.config_handler import prompts_config
from utils.path_tools import get_abs_path


def loader_system_prompts():
    try:
        system_prompts = get_abs_path(prompts_config['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[loader_system_prompts]在yaml配置中没有main_prompt_path配置项")
        raise e

    try:
        return open(system_prompts, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_system_prompts]解析系统提示词出错,{str(e)}")
        raise e


def loader_rag_prompts():
    try:
        rag_prompts = get_abs_path(prompts_config['rag_summerize_prompt_path'])
    except KeyError as e:
        logger.error(f"[loader_rag_prompts]在yaml配置中没有rag_summerize_prompt_path配置项")
        raise e

    try:
        return open(rag_prompts, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_rag_prompts]解析系统提示词出错,{str(e)}")
        raise e

def loader_report_prompts():
    try:
        report_prompts = get_abs_path(prompts_config['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[loader_report_prompts]在yaml配置中没有report_prompt_path配置项")
        raise e

    try:
        return open(report_prompts, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_report_prompts]解析系统提示词出错,{str(e)}")
        raise e

