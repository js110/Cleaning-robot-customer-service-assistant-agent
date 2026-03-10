import datetime
import os
import random

from langchain_core.tools import tool

from rag.rag_service import RagSummerizeService
from utils.weather_service import fetch_weather, get_user_city
from utils.config_handler import agent_config
from utils.path_tools import get_abs_path
from utils.logger_handler import logger

rag_service = RagSummerizeService()
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009"]
external_data = {}


@tool(description="从向量存储中检索参考资料并总结回答")
def rag_summarize(query: str) -> str:
    result, _ = rag_service.rag_summerize(query)
    return result


@tool(description="查询指定城市的实时天气和今日预报，以字符串形式返回")
def get_weather(city: str) -> str:
    try:
        return fetch_weather(city)
    except Exception as exc:
        return f"查询城市“{city}”天气失败：{exc}"


@tool(description="获取用户所在城市名称，以字符串形式返回")
def get_user_location() -> str:
    try:
        return get_user_city()
    except Exception as exc:
        return f"获取用户所在城市失败：{exc}"


@tool(description="获取用户的id,以纯字符串返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份,以纯字符串返回")
def get_current_month() -> str:
    return str(datetime.date.today().month).zfill(2)


def generator_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")
                user_id = arr[0].replace('"', "")
                feature = arr[1].replace('"', "")
                efficiency = arr[2].replace('"', "")
                consumables = arr[3].replace('"', "")
                comparison = arr[4].replace('"', "")
                time = arr[5].replace('"', "")
                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取用户的使用记录,以纯字符串返回,如果未检索到,返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generator_external_data()
    try:
        return external_data[user_id][month]
    except KeyError as exc:
        logger.warning(f"[fetch_external_data]未能检索到用户{user_id}在{month}的使用记录数据")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"
