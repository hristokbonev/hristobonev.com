from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from models.models import Video
from dotenv import load_dotenv
import os
from urllib.parse import urljoin

router = APIRouter(prefix="/reels", tags=["Reels"])
templates = Jinja2Templates(directory="templates")

load_dotenv()

S3_BASE_URL = os.getenv("S3_BASE_URL")



# Videos with updated S3 URLs
video1 = Video(title="Showreel", url=urljoin(S3_BASE_URL, "media/videos/Showreel 5.mp4"))
video2 = Video(title="Please insert a factory here", url=urljoin(S3_BASE_URL, "media/videos/please_insert_a_factory_here_part_one (1080p).mp4"))
video3 = Video(title="Chain of Command", url=urljoin(S3_BASE_URL, "media/videos/Chain Of Command.mp4"))
video4 = Video(title="Some things never change", url=urljoin(S3_BASE_URL, "media/videos/Mira Yonder Showreel.mov"))
video5 = Video(title="From Here to Eternity", url=urljoin(S3_BASE_URL, "media/videos/IAB_mono_HRISTO_720.mp4"))
video6 = Video(title="Voice Reel", url=urljoin(S3_BASE_URL, "media/videos/Voice Reel.wav"))
video7 = Video(title="The Tinderbox", url=urljoin(S3_BASE_URL, "media/videos/the_tinderbox (1080p).mp4"))

videos = [video1, video6, video3, video2, video7, video5, video4]

@router.get("/")
async def show_videos(request: Request, page: int = 1, page_size: int = 5):
    start = (page - 1) * page_size
    end = start + page_size
    paginated_videos = videos[start:end]
    total_pages = (len(videos) + page_size - 1) // page_size  # Ceiling division
    return templates.TemplateResponse("reels.html", {
        "request": request, 
        "videos": paginated_videos,
        "current_page": page,
        "total_pages": total_pages
    })
