import pickle
from typing import Any

from dotenv import load_dotenv

load_dotenv()

import asyncio

from graph import get_graph, draw_graph
from vk_api import collect_data
from task_2_vk_graph.analyzer import show_analyze
import file_service

def _pickle_res(obj: Any, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)

async def collect_dataset():
    await collect_data()

async def process_dataset():
    data = file_service.load_data_list()
    graph = get_graph(data)
    analyze_dump = show_analyze(graph=graph)
    # checkpoint
    _pickle_res(analyze_dump, "analyze_dump")
    draw_graph(graph, *analyze_dump)


async def main():
    # await collect_dataset()
    await process_dataset()


if __name__ == '__main__':
    asyncio.run(main())
