from pydantic import BaseModel, ConfigDict


class LikesSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    like: bool
