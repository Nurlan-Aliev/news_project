from pydantic import BaseModel, ConfigDict


class LikesSchemas(BaseModel):
    likes: int
    dislikes: int
    user_reaction: bool | None = None
