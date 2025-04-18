
import os
import asyncio
from typing import Optional

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI


def init_agent_service():
    llm_cfg = {'model': 'qwen-plus','model_server':'dashscope','api_key':'填写自己的大模型apikey'}
    system = ('你扮演一个GIS助手，你具有GIS工具使用的能力')
    tools = [{
        "mcpServers": {
            "amap-maps": {
                "command": "npx",
                "args": ["-y", "@amap/amap-maps-mcp-server"],
                "env": {
                    "AMAP_MAPS_API_KEY": "5f4144ccb8d100dbaad5a59b246cb72d"
                }}
        }
    }]
    bot = Assistant(
        llm=llm_cfg,
        name='Spatial Reasoning',
        description='Spatial Reasoning',
        system_message=system,
        function_list=tools,
    )

    return bot


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        query = input('user question: ')
        file = input('file url (press enter if no file): ').strip()
        if not query:
            print('user question cannot be empty！')
            continue
        if not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})
        
        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        messages.extend(response)


def app_gui():
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '我现在在苏州的吴中区，我要去无锡看樱花，给我规划个路径'
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()