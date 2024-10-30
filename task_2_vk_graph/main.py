import asyncio

from graph import get_graph
from vk_api import collect_data
from task_2_vk_graph.analyzer import show_analyze


async def main():

    graph = await get_graph(source=collect_data())
    show_analyze(graph=graph)


if __name__ == '__main__':
    asyncio.run(main())
