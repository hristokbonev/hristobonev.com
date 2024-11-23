from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from models.models import Album, Photo
import os

router = APIRouter(prefix="/gallery", tags=["Gallery"])
templates = Jinja2Templates(directory="templates")

ALBUMS_DIR = "media/albums"

def get_albums():
    albums = []
    for album_name in os.listdir(ALBUMS_DIR):
        album_path = os.path.join(ALBUMS_DIR, album_name)
        if os.path.isdir(album_path):
            albums.append(Album(name=album_name, cover=f"/{album_path}/{os.listdir(album_path)[0]}"))
    return albums

def get_album_photos(album_name):
    album_path = os.path.join(ALBUMS_DIR, album_name)
    if not os.path.isdir(album_path):
        return None
    photos = [Photo(src=f"/{album_path}/{photo_name}", name=f'{photo_name}') for photo_name in os.listdir(album_path)]

    return photos

@router.get("/")
async def gallery(request: Request):
    albums = get_albums()
    return templates.TemplateResponse("gallery.html", {"request": request, "albums": albums})

@router.get("/{album_name}")
async def show_album(request: Request, album_name: str):
    photos = get_album_photos(album_name)
    if photos is None:
        return {"message": "Album not found"}
    return templates.TemplateResponse("album.html", {"request": request, "photos": photos, "album_name": album_name})