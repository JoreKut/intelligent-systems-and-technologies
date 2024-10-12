from pydantic import BaseModel


class GetUserFriendsResponse(BaseModel):
    count: int = 0
    items: list[int] = []
