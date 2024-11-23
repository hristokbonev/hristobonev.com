from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/projects", tags=["Git Projects"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def git_projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})