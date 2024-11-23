from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from models.models import Album, Photo
import boto3

router = APIRouter(prefix="/gallery", tags=["Gallery"])
templates = Jinja2Templates(directory="templates")

s3_client = boto3.client('s3', region_name="eu-north-1")
BUCKET_NAME = 'hristobonevbucket'
ALBUMS_DIR = "media/albums"  

def get_albums():
    albums = []
    try:
        # List objects in the "media/albums" folder of your S3 bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=ALBUMS_DIR, Delimiter='/')
        for prefix in response.get('CommonPrefixes', []):
            album_name = prefix['Prefix'].split('/')[-2]

            album_photos = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{ALBUMS_DIR}/{album_name}/")
            
            if album_photos.get('Contents'):
                cover_photo = album_photos['Contents'][0]['Key']  # Assume the first file is the cover
                albums.append(Album(name=album_name, cover=f"https://{BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{cover_photo}"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching albums: {str(e)}")
    return albums

def get_album_photos(album_name):
    try:
        album_path = f"{ALBUMS_DIR}/{album_name}/"
        photos = []
        # List all photos in the album
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=album_path)
        if 'Contents' in response:
            for file in response['Contents']:
                photo_name = file['Key'].split('/')[-1]  # Get file name from S3 key
                photo_url = f"https://{BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{file['Key']}"
                photos.append(Photo(src=photo_url, name=photo_name))
        return photos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching photos: {str(e)}")

@router.get("/")
async def gallery(request: Request):
    albums = get_albums()
    return templates.TemplateResponse("gallery.html", {"request": request, "albums": albums})

@router.get("/{album_name}")
async def show_album(request: Request, album_name: str):
    photos = get_album_photos(album_name)
    if not photos:
        return {"message": "Album not found"}
    return templates.TemplateResponse("album.html", {"request": request, "photos": photos, "album_name": album_name})
