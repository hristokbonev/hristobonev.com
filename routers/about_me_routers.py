from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/about-me', tags=['About Me'])
templates = Jinja2Templates(directory="templates")

@router.get('/', response_model=None)
def serve_homepage(request: Request = None):
    return templates.TemplateResponse(name='about-me.html', request=request)