from pydantic import BaseModel


class GetUserFriendsResponse(BaseModel):
    count: int = 0
    items: list[int] = []


class UserFriends(BaseModel):
    user_id: int
    friend_ids: list[int] = []
