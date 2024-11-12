import functools
import json
import os
from json import JSONDecodeError

from task_2_vk_graph.core import on_exception
from task_2_vk_graph.models import UserData

BASE_STORAGE_DIRECTORY = os.getenv("BASE_STORAGE_DIRECTORY", "storage")

CURRENT_QUEUE_FILENAME = f"{BASE_STORAGE_DIRECTORY}/current_queue.json"
NEXT_QUEUE_FILENAME = f"{BASE_STORAGE_DIRECTORY}/next_queue.json"
VISITED_FILENAME = f"{BASE_STORAGE_DIRECTORY}/visited.json"
USER_DATA_FILENAME = f"{BASE_STORAGE_DIRECTORY}/data.json"
ANALYZE_BETWENESS = f"{BASE_STORAGE_DIRECTORY}/betweness.json"
ANALYZE_EIGENVECTOR = f"{BASE_STORAGE_DIRECTORY}/eigenvector.json"


def append_datas_to_json_file(data_list: list, output_file=USER_DATA_FILENAME):
    # Чтение текущего содержимого файла
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        # Файл еще не существует, создаем пустой список
        existing_data = []

    # Добавляем новую запись
    existing_data.extend(data_list)

    # Запись данных обратно в файл
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def reset_data_to_json_file(data, output_file):
    # Запись данных обратно в файл
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_models_to_file(models: list):
    append_datas_to_json_file(models, USER_DATA_FILENAME)


def update_current_queue_to_file(data):
    reset_data_to_json_file(data, CURRENT_QUEUE_FILENAME)


def update_next_queue_to_file(data):
    reset_data_to_json_file(data, NEXT_QUEUE_FILENAME)


def update_visited_to_file(data):
    reset_data_to_json_file(data, VISITED_FILENAME)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_current_queue():
    with open(CURRENT_QUEUE_FILENAME, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_next_queue():
    with open(NEXT_QUEUE_FILENAME, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], set())
def load_visited() -> list:
    with open(VISITED_FILENAME, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_data_list() -> list[UserData]:
    with open(USER_DATA_FILENAME, 'r', encoding='utf-8') as file:
        return json.load(file)


def _dump_analyze_result(filename: str, obj: dict, ):
    with open(filename, "w") as f:
        json.dump(obj, f)

def _load_analyze_result(filename: str):
    with open(filename, "r") as f:
        res = json.load(f)
    return res

save_betweness = functools.partial(_dump_analyze_result, ANALYZE_BETWENESS)
save_eigenvector = functools.partial(_dump_analyze_result, ANALYZE_EIGENVECTOR)

load_betweness = functools.partial(_load_analyze_result, ANALYZE_BETWENESS)
load_eigenvector = functools.partial(_load_analyze_result, ANALYZE_EIGENVECTOR)


if __name__ == '__main__':
    data = load_data_list()
    q = load_data_list()
    visited = load_data_list()
    print(data)
    print(q)
    print(visited)
