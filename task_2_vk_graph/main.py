import json

from dotenv import load_dotenv

load_dotenv()

import asyncio

from graph import get_graph, draw_graph
from vk_api import collect_data
from task_2_vk_graph.analyzer import show_analyze
import file_service

CHECKPOINT_FILENAME = "analyze.json"


async def collect_dataset():
    await collect_data()


def analyze_dataset():
    data = file_service.load_data_list()
    graph = get_graph(data)
    betweenness, eigenvector, closeness = show_analyze(graph=graph)
    file_service.save_betweness(betweenness)
    file_service.save_eigenvector(eigenvector)
    file_service.save_eigenvector(closeness)


def draw_dataset():
    data = file_service.load_data_list()
    graph = get_graph(data)
    betweness = file_service.load_betweness()
    betweness: dict[int, float]

    betweness_main_nodes = list(betweness.keys())[:1]
    betweness_main_nodes = [int(n) for n in betweness_main_nodes]  # from json we get str and must cast to int
    draw_graph(
        graph,
        main_nodes=betweness_main_nodes,
        min_edges=0,
    )


async def main():
    # await collect_dataset()
    # analyze_dataset()
    draw_dataset()


if __name__ == '__main__':
    asyncio.run(main())
