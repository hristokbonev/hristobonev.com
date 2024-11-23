from pydantic import BaseModel

class Video(BaseModel):

    title: str
    url: str


class Album(BaseModel):

    name: str | None = None
    cover: str | None = None

class Photo(BaseModel):

    name: str | None = None
    src: str