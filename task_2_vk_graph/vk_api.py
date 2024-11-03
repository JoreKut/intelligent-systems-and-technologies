import asyncio
from itertools import batched
from typing import AsyncGenerator
import file_service
import aiohttp

from task_2_vk_graph.models import GetUserFriendsResponse, UserFriends


class VkApi:
    session = None

    def __init__(self):
        self.base_url = "https://api.vk.com/method"
        self.base_payload = {
            "access_token": "vk1.a.sWiY5ZvA4T11Q1uHHo8dyNRqfsuWNBzKNP7RMIvcXpqIcx-3uKdWNptQ2oNeETMSDDkNplv0Dt9RkeTy3YlQNUZT26WbPpKQrDfCEhjT6796KnlyniGI-bFVIcaSY3t3bV-rBEeKhNC9qmfHkVrfYDlR27jAakrYuROCzgQI1AUK8MKaYFUDQQn-spMyesRpTur7CyUuHaYv1B46mPF1dw",
            "v": "5.199",
        }
        self.conn = aiohttp.TCPConnector(limit_per_host=10)
        self.session = aiohttp.ClientSession(connector=self.conn)

    async def get_user_friends(self, user_id) -> GetUserFriendsResponse:
        payload = self.base_payload
        payload.update({"user_id": str(user_id)})
        async with self.session.post(
                url=f"{self.base_url}/friends.get",
                data=payload,
        ) as resp:
            res = await resp.json()

        if 'error' in res:
            print(res)
            return GetUserFriendsResponse(user_id=user_id, count=0, items=[])

        return GetUserFriendsResponse(user_id=user_id, **res['response'])


async def async_collect_gen(func, user_ids_batch) -> AsyncGenerator[list[GetUserFriendsResponse]]:

    print('\t[async_collect_gen] batch', user_ids_batch)
    tasks = [
        func(user_id=_id)
        for _id in user_ids_batch
    ]
    yield await asyncio.gather(*tasks)


async def search_iteration(
        func,
        user_queue: list[int],
        visited_users: set[int],
        tag: str = "untagged"
):
    print("\n\n\n")
    print("#" * 100)
    print(tag)
    print(
        f"| user_queue={len(user_queue)}"
        f" | visited_users={len(visited_users)}"
    )

    coroutine_number = 10
    print('\t[async_collect_gen] count', len(user_queue))
    next_user_queue = file_service.load_next_queue()

    for user_ids_batch in batched(user_queue, coroutine_number):

        # удаляем из очереди первые значения
        user_queue = user_queue[coroutine_number:]

        async for response_batch in async_collect_gen(func, user_ids_batch=user_ids_batch):
            casted_response = []
            for response in response_batch:
                casted_response.append(UserFriends(user_id=int(response.user_id), friend_ids=response.items))

                next_user_ids_set = set(response.items) - visited_users
                # limit for user count = 100
                next_user_ids = list(next_user_ids_set)[:100]
                # set visited and next users
                visited_users.update(user_ids_batch)
                next_user_queue.extend(next_user_ids)

            data_to_save = [el.model_dump() for el in casted_response]
            file_service.save_models_to_file(data_to_save)

            file_service.update_current_queue_to_file(user_queue)
            file_service.update_next_queue_to_file(next_user_queue)
            file_service.update_visited_to_file(list(visited_users))

            print(f"{list(visited_users)=}")

    print(f"Clear user_queue before={len(user_queue)} after={len(next_user_queue)}")
    user_queue.extend(next_user_queue)

    file_service.update_current_queue_to_file(user_queue)
    file_service.update_next_queue_to_file([])

    print(tag, 'casted_response count=', len(user_queue))


async def collect_data():
    vk_api = VkApi()
    visited_users = set(file_service.load_visited())
    user_queue: list[int] = file_service.load_current_queue()
    bsmo_10_24_users = [193887357]

    for user_id in bsmo_10_24_users:
        if user_id not in visited_users:
            user_queue.append(user_id)

    # Друзья одногруппников
    # [bsmo] --> <friends>
    await search_iteration(
        vk_api.get_user_friends,
        user_queue=user_queue,
        visited_users=visited_users,
        tag="[bsmo] --> <friends>",
    )
    #
    # # Друзья друзей одногруппников
    # # [bsmo] --> <friends> --> <friends>
    #
    # result = await search_iteration(
    #     vk_api.get_user_friends,
    #     user_queue=user_queue,
    #     visited_users=visited_users,
    #     tag="[bsmo] --> <friends> --> <friends>",
    # )
    # yield result
    #
    # # Друзья друзей друзей одногруппников
    # # [bsmo] --> <friends> --> [friends] --> <friends>
    #
    # result = await search_iteration(
    #     vk_api.get_user_friends,
    #     user_queue=user_queue,
    #     visited_users=visited_users,
    #     tag="[bsmo] --> <friends> --> [friends] --> <friends>",
    # )
    # yield result

    await vk_api.session.close()
