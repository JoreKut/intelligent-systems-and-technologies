import json
from json import JSONDecodeError

from task_2_vk_graph.core import on_exception

CURRENT_QUEUE_filename = "storage/current_queue.json"
NEXT_QUEUE_filename = "storage/next_queue.json"
VISITED_filename = "storage/visited.json"
USER_DATA_filename = "storage/data.json"


def append_datas_to_json_file(data_list: list, output_file=USER_DATA_filename):
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
    append_datas_to_json_file(models, USER_DATA_filename)


def update_current_queue_to_file(data):
    reset_data_to_json_file(data, CURRENT_QUEUE_filename)


def update_next_queue_to_file(data):
    reset_data_to_json_file(data, NEXT_QUEUE_filename)


def update_visited_to_file(data):
    reset_data_to_json_file(data, VISITED_filename)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_current_queue():
    with open(CURRENT_QUEUE_filename, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_next_queue():
    with open(NEXT_QUEUE_filename, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], set())
def load_visited() -> list:
    with open(VISITED_filename, 'r', encoding='utf-8') as file:
        return json.load(file)


@on_exception([FileNotFoundError, JSONDecodeError], [])
def load_data_list():
    with open(USER_DATA_filename, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == '__main__':
    data = load_data_list()
    q = load_data_list()
    visited = load_data_list()
    print(data)
    print(q)
    print(visited)
