from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
import os


@tool(description="查询天气")
def get_weather() -> str:
    return "大风天"


agent = create_agent(
    model=ChatTongyi(
        model="qwen3-max",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY", ""),
    ),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题。",
)

res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "明天北京的天气如何？"},
        ]
    }
)

for msg in res['messages']:
    print(type(msg).__name__,msg.content)
