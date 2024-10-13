from pydantic import BaseModel


class GetUserFriendsResponse(BaseModel):
    user_id: int = None
    count: int = 0
    items: list[int] = []
