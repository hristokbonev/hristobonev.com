from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models.models import Video
import os
from urllib.parse import urljoin

# Define base URL without f-string
S3_BASE_URL = "https://hristobonevbucket.s3.eu-north-1.amazonaws.com/"

# Create video objects with properly constructed URLs
left_video = Video(
    title="Lights",
    url=urljoin(S3_BASE_URL, "media/videos/15493-264715953_medium.mp4")
)
right_video = Video(
    title="Net",
    url=urljoin(S3_BASE_URL, "media/videos/113367-697718066_small.mp4")
)
resume = {
    "title": "Resume",
    "url": urljoin(S3_BASE_URL, "media/resume/HristoBonevCV.pdf")
}

router = APIRouter(prefix='/about-me', tags=['About Me'])
templates = Jinja2Templates(directory="templates")

@router.get('/', response_model=None)
async def serve_about_me(request: Request):
    return templates.TemplateResponse(
        "about-me.html",
        {
            "request": request,
            "left_video": left_video,
            "right_video": right_video,
            "resume": resume
        }
    )

# Add a redirect route for any S3 URLs that might get caught by the router
