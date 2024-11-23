from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from common.email_services import send_email


router = APIRouter(prefix="/contact", tags=["Contact"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/")
async def submit_contact(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # Here you can handle the form submission, e.g., send an email or save to a database
    send_email(name=name, email=email, content=message)
    return RedirectResponse(url="/contact", status_code=303)