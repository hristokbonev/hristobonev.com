from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from models.models import Album, Photo
import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# FastAPI Router setup
router = APIRouter(prefix="/gallery", tags=["Gallery"])
templates = Jinja2Templates(directory="templates")

# AWS S3 client setup
s3_client = boto3.client('s3', region_name="eu-north-1")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ALBUMS_DIR = os.getenv("ALBUMS_DIR", "media/albums/").rstrip("/") + "/"
S3_BASE_URL = os.getenv("S3_BASE_URL", f"https://{BUCKET_NAME}.s3.eu-north-1.amazonaws.com")

# Helper function to fetch albums
def get_albums():
    albums = []
    try:
        # List objects in the albums directory
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=ALBUMS_DIR, Delimiter='/')
       

        prefixes = response.get('CommonPrefixes', [])
        if not prefixes:
            return albums

        for prefix in prefixes:
            album_name = prefix['Prefix'].split('/')[-2]
            album_photos = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{prefix['Prefix']}")

            cover_photo = album_photos['Contents'][0]['Key']
            cover_url = f"{S3_BASE_URL.rstrip('/')}/{cover_photo.lstrip('/')}"  # Fix the extra slash
            albums.append(Album(name=album_name, cover=cover_url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching albums: {str(e)}")
    return albums


def get_album_photos(album_name):
    try:
        album_path = f"{ALBUMS_DIR}{album_name}/"
        photos = []

        # List all photos in the specified album path
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=album_path)

        if 'Contents' in response:
            for file in response['Contents']:
                if file['Key'].endswith('/'):  # Skip directories
                    continue
                photo_name = file['Key'].split('/')[-1]  # Extract the photo name
                photo_url = f"{S3_BASE_URL.rstrip('/')}/{file['Key'].lstrip('/')}"  # Construct clean URL
                photos.append(Photo(url=photo_url, name=photo_name))
       
        return photos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching photos: {str(e)}")


# Gallery endpoint
@router.get("/")
async def gallery(request: Request):
    albums = get_albums()
    return templates.TemplateResponse("gallery.html", {"request": request, "albums": albums})

# Album photos endpoint
@router.get("/{album_name}")
async def show_album(request: Request, album_name: str):
    photos = get_album_photos(album_name)
    if not photos:
        return {"message": "Album not found"}
    return templates.TemplateResponse("album.html", {"request": request, "photos": photos, "album_name": album_name})
