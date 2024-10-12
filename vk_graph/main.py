import asyncio

from graph import get_graph
from vk_api import collect_data
from vk_graph.analyzer import show_analyze


async def main():
    data = await collect_data()
    graph = get_graph(data=data)
    show_analyze(graph=graph)


if __name__ == '__main__':
    asyncio.run(main())
