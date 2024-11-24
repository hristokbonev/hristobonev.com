from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from models.models import Video
from models.models import Photo
from urllib.parse import urljoin


load_dotenv()

router = APIRouter(prefix='', tags=['Homepage'])
templates = Jinja2Templates(directory="templates")

S3_BASE_URL = "https://hristobonevbucket.s3.eu-north-1.amazonaws.com/"

left_video = Video(title="Showreel", url=urljoin(S3_BASE_URL, "media/videos/Chain+of+Command+short.mp4"))
right_video = Video(title="Coding", url=urljoin(S3_BASE_URL, "media/videos/5495899-hd_1080_1920_30fps.mp4"))
centre_image = Photo(name="Myself", url=urljoin(S3_BASE_URL, "media/images/582e4aef44b5d.jpg"))

@router.get('/', response_model=None)
def serve_homepage(request: Request = None):
    return templates.TemplateResponse(name='index.html', request=request, context={'left_video': left_video, 'right_video': right_video, 'centre_image': centre_image})
