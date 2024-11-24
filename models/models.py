from pydantic import BaseModel, validator
from urllib.parse import quote

class Video(BaseModel):
    title: str
    url: str
 # URL encode the url


class Album(BaseModel):
    name: str | None = None
    cover: str | None = None
    url: str | None = None


class Photo(BaseModel):
    name: str | None = None
    url: str

