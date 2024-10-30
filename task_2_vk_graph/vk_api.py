import aiohttp

from task_2_vk_graph.models import GetUserFriendsResponse, UserFriends


class VkApi:

    def __init__(self):
        self.base_url = "https://api.vk.com/method"
        self.base_payload = {
            "access_token": "<your token>",
            "v": "5.199",
        }

    async def get_user_friends(self, user_id) -> GetUserFriendsResponse:
        payload = self.base_payload
        payload.update({"user_id": str(user_id)})

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{self.base_url}/friends.get",
                    data=payload,
            ) as resp:
                res = await resp.json()

        if 'error' in res:
            return GetUserFriendsResponse(count=0, items=[])

        return GetUserFriendsResponse(**res['response'])


async def collect_data() -> list[UserFriends]:
    vk_api = VkApi()
    bsmo_10_24_users = ['193887357']
    users_friends = []
    # TODO: optimize with asyncio.gather. Exec coroutines by batches.
    for user_id in bsmo_10_24_users:
        level_1_resp = await vk_api.get_user_friends(user_id=user_id)
        users_friends.append(UserFriends(user_id=user_id, friend_ids=level_1_resp.items))

        for inner_user_id in level_1_resp.items:
            level_2_resp = await vk_api.get_user_friends(user_id=inner_user_id)
            users_friends.append(UserFriends(user_id=inner_user_id, friend_ids=level_2_resp.items))

            for inner_users_user_id in level_2_resp:
                level_3_resp = await vk_api.get_user_friends(user_id=inner_users_user_id)
                users_friends.append(UserFriends(user_id=inner_user_id, friend_ids=level_3_resp.items))

    return users_friends
