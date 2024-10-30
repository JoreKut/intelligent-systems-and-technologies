import asyncio
from itertools import batched
from typing import Generator

import aiohttp

from task_2_vk_graph.models import GetUserFriendsResponse, UserFriends


class VkApi:

    def __init__(self):
        self.base_url = "https://api.vk.com/method"
        self.base_payload = {
            "access_token": "vk1.a.Swg3AX8bmnufEdG2PI_i1QFj_xrRWx3T16twTLKL_PWLHw5e9AVs1tnmVlrctNbVRZjB0EAmIP_n-eSlr0t7ITZLOMRXHZ7N1ouSdoWG4kZUqXLyeeJP8cnibymajH-oKMtk2WceZDS7Vch2eYziRQFtR9vzTlze3NjjM-OdQzjdxlLobi1gz-b-Qv_YVS5hHyyakPRGp0L8vNMk5c2iJg",
            "v": "5.199",
        }
        self.conn = aiohttp.TCPConnector(limit_per_host=30)
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
            return GetUserFriendsResponse(count=0, items=[])

        return GetUserFriendsResponse(**res['response'])


async def collect_data() -> Generator[UserFriends]:
    vk_api = VkApi()
    bsmo_10_24_users = ['193887357']
    users_friends = []

    for user_id in bsmo_10_24_users:  # 30 await
        print('[processing...]', user_id)
        level_1_resp = await vk_api.get_user_friends(user_id=user_id)
        users_friends.append(UserFriends(user_id=user_id, friend_ids=level_1_resp.items))

        for inner_user_id in level_1_resp.items[:100]:  # 100 await
            level_2_resp = await vk_api.get_user_friends(user_id=inner_user_id)
            users_friends.append(UserFriends(user_id=inner_user_id, friend_ids=level_2_resp.items))

            for inner_users_user_ids in batched(level_2_resp.items[:100], 25):  # 4 await
                print(inner_users_user_ids)
                # START ASYNCIO
                tasks = [
                    vk_api.get_user_friends(user_id=_id)
                    for _id in inner_users_user_ids
                ]
                level_3_resp_list = await asyncio.gather(*tasks)
                # END ASYNCIO

                for level_3_resp in level_3_resp_list:
                    users_friends.append(UserFriends(user_id=inner_user_id, friend_ids=level_3_resp.items))
            print('\t[processed] ', inner_user_id)

        print('[processed] ', user_id)
        yield users_friends
        users_friends.clear()
