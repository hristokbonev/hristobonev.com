from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from models.models import Album, Photo
import boto3
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
import os
from functools import lru_cache
from typing import List, Optional
import logging
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

router = APIRouter(prefix="/gallery", tags=["Gallery"])
templates = Jinja2Templates(directory="templates")

# Environment variables with validation
BUCKET_NAME = os.getenv("BUCKET_NAME")
ALBUMS_DIR = os.getenv("ALBUMS_DIR", "media/albums").rstrip('/')
REGION = os.getenv("AWS_REGION", "eu-north-1")

if not BUCKET_NAME:
    raise ValueError("BUCKET_NAME environment variable is not set")

# Initialize S3 client with error handling
try:
    s3_client = boto3.client('s3', region_name=REGION)
except (Boto3Error, BotoCoreError) as e:
    logger.error(f"Failed to initialize S3 client: {str(e)}")
    raise

def get_s3_url(key: str) -> str:
    """Generate a proper S3 URL for an object."""
    return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{key}"

@lru_cache(maxsize=32)
def get_albums() -> List[Album]:
    """
    Fetch and cache list of albums from S3.
    Uses LRU cache to improve performance for repeated requests.
    """
    albums = []
    try:
        # List objects in the albums directory
        paginator = s3_client.get_paginator('list_objects_v2')
        prefix_pages = paginator.paginate(
            Bucket=BUCKET_NAME,
            Prefix=ALBUMS_DIR,
            Delimiter='/'
        )

        for page in prefix_pages:
            for prefix in page.get('CommonPrefixes', []):
                album_name = prefix['Prefix'].split('/')[-2]
                
                # Get the first image as cover
                cover_response = s3_client.list_objects_v2(
                    Bucket=BUCKET_NAME,
                    Prefix=prefix['Prefix'],
                    MaxKeys=1
                )

                if cover_response.get('Contents'):
                    cover_key = cover_response['Contents'][0]['Key']
                    cover_url = get_s3_url(cover_key)
                    albums.append(Album(
                        name=album_name,
                        cover=cover_url
                    ))

        return sorted(albums, key=lambda x: x.name)

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS S3 error: {error_code} - {error_message}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch albums: {error_message}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_albums: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching albums"
        )

@lru_cache(maxsize=100)
def get_album_photos(album_name: str) -> List[Photo]:
    """
    Fetch and cache photos for a specific album.
    Uses LRU cache to improve performance for repeated requests.
    """
    if not album_name or '/' in album_name:
        raise HTTPException(status_code=400, detail="Invalid album name")

    try:
        album_path = f"{ALBUMS_DIR}/{album_name}/"
        photos = []
        
        # Use pagination to handle large albums
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=BUCKET_NAME,
            Prefix=album_path
        )

        for page in pages:
            if 'Contents' in page:
                for file in page['Contents']:
                    # Skip folder objects
                    if file['Key'].endswith('/'):
                        continue
                        
                    photo_name = file['Key'].split('/')[-1]
                    # Skip hidden files
                    if photo_name.startswith('.'):
                        continue
                        
                    photo_url = get_s3_url(file['Key'])
                    photos.append(Photo(
                        src=photo_url,
                        name=photo_name
                    ))

        return sorted(photos, key=lambda x: x.name)

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS S3 error in get_album_photos: {error_code} - {error_message}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch photos: {error_message}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_album_photos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching photos"
        )

@router.get("/")
async def gallery(request: Request):
    """Serve the gallery page with all albums."""
    try:
        albums = get_albums()
        return templates.TemplateResponse(
            "gallery.html",
            {
                "request": request,
                "albums": albums,
                "title": "Photo Gallery"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in gallery route: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while loading the gallery"
        )

@router.get("/{album_name}")
async def show_album(
    request: Request,
    album_name: str
):
    """Serve a specific album page."""
    try:
        photos = get_album_photos(album_name)
        if not photos:
            raise HTTPException(status_code=404, detail="Album not found")
            
        return templates.TemplateResponse(
            "album.html",
            {
                "request": request,
                "photos": photos,
                "album_name": album_name,
                "title": f"Album - {album_name}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in show_album route: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while loading the album"
        )

# Optionally, add a route to clear the cache if needed
@router.post("/clear-cache")
async def clear_cache():
    """Clear the LRU cache for albums and photos."""
    get_albums.cache_clear()
    get_album_photos.cache_clear()
    return {"message": "Cache cleared successfully"}