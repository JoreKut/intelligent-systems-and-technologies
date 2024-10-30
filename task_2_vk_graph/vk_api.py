import asyncio
from itertools import batched
from typing import Generator, AsyncGenerator

import aiohttp

from task_2_vk_graph.models import GetUserFriendsResponse, UserFriends


class VkApi:
    session = None

    def __init__(self):
        self.base_url = "https://api.vk.com/method"
        self.base_payload = {
            "access_token": "vk1.a.Swg3AX8bmnufEdG2PI_i1QFj_xrRWx3T16twTLKL_PWLHw5e9AVs1tnmVlrctNbVRZjB0EAmIP_n-eSlr0t7ITZLOMRXHZ7N1ouSdoWG4kZUqXLyeeJP8cnibymajH-oKMtk2WceZDS7Vch2eYziRQFtR9vzTlze3NjjM-OdQzjdxlLobi1gz-b-Qv_YVS5hHyyakPRGp0L8vNMk5c2iJg",
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


async def async_collect_gen(func, user_ids) -> AsyncGenerator[list[GetUserFriendsResponse]]:
    coroutine_number = 10
    print('\t[async_collect_gen] count', len(user_ids))
    for user_ids_batch in batched(user_ids, coroutine_number):
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
    collected_response_gen = async_collect_gen(func, user_ids=user_queue)
    casted_response = []
    async for response_batch in collected_response_gen:
        print()
        print("response_batch", len(response_batch))
        for response in response_batch:
            casted_response.append(UserFriends(user_id=int(response.user_id), friend_ids=response.items))

            next_user_ids_set = set(response.items) - visited_users
            # limit for user count = 100
            next_user_ids = list(next_user_ids_set)[:100]
            # set visited and next users
            visited_users.update(response.items)
            user_queue.extend(next_user_ids)

    print(tag, len(casted_response))
    return casted_response


async def collect_data() -> Generator[UserFriends]:
    vk_api = VkApi()
    bsmo_10_24_users = [193887357]
    user_queue: list[int] = [*bsmo_10_24_users]
    visited_users = set()

    # Друзья одногруппников
    # [bsmo] --> <friends>
    result = await search_iteration(
        vk_api.get_user_friends,
        user_queue=user_queue,
        visited_users=visited_users,
        tag="[bsmo] --> <friends>",
    )
    yield result

    # Друзья друзей одногруппников
    # [bsmo] --> <friends> --> <friends>

    result = await search_iteration(
        vk_api.get_user_friends,
        user_queue=user_queue,
        visited_users=visited_users,
        tag="[bsmo] --> <friends> --> <friends>",
    )
    yield result

    # Друзья друзей друзей одногруппников
    # [bsmo] --> <friends> --> [friends] --> <friends>

    result = await search_iteration(
        vk_api.get_user_friends,
        user_queue=user_queue,
        visited_users=visited_users,
        tag="[bsmo] --> <friends> --> [friends] --> <friends>",
    )
    yield result

    await vk_api.session.close()

