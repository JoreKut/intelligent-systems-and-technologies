from typing import TypedDict

from pydantic import BaseModel


class GetUserFriendsResponse(BaseModel):
    user_id: int = None
    count: int = 0
    items: list[int] = []


class UserFriends(BaseModel):
    user_id: int
    friend_ids: list[int] = []


class UserData(TypedDict):
    user_id: int
    friends_ids: list[int]
