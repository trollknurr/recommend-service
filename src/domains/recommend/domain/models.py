from pydantic import BaseModel


class UserHistory(BaseModel):
    item_ids: list[int]


class UserRecommendation(BaseModel):
    item_ids: list[int]
