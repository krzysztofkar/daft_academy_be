from pydantic import BaseModel


class Album(BaseModel):
    title: str
    artist_id: int
