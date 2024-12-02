from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from common.email_services import send_email
from common.captcha_services import allow_action
from dotenv import load_dotenv
import os

load_dotenv()

credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

credentials_path = "/tmp/google-credentials.json"
with open(credentials_path, "w") as f:
    f.write(credentials_json)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

router = APIRouter(prefix="/contact", tags=["Contact"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/")
async def submit_contact(request: Request, name: str = Form(...), email: str = Form(...), 
                         message: str = Form(...)):
    # Here you can handle the form submission, e.g., send an email or save to a database

    form_data = await request.form()

    g_recaptcha_response = form_data.get("g-recaptcha-response")

    if not g_recaptcha_response:
        return RedirectResponse(url="/contact", status_code=303)

    is_valid = allow_action(token=g_recaptcha_response)

    if not is_valid:
        return RedirectResponse(url="/contact", status_code=303)
    
    send_email(name=name, email=email, content=message)
    return RedirectResponse(url="/contact", status_code=303)