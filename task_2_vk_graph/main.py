from dotenv import load_dotenv

load_dotenv()

import asyncio
import sys

from graph import get_graph
from vk_api import collect_data
from task_2_vk_graph.analyzer import show_analyze
import file_service

async def main():
    await collect_data()
    # graph = await get_graph(source=)
    # show_analyze(graph=graph)


if __name__ == '__main__':
    # asyncio.run(main())
    data = file_service.load_data_list()
    print(len(data))
