from fastapi import FastAPI
from routers.homepage_routers import router as homapage_router
from routers.about_me_routers import router as about_me_router
from routers.projects_routers import router as projects_router
from routers.reels_routers import router as reels_router
from routers.contact_routers import router as contact_router
from routers.gallery_routers import router as gallery_router
from fastapi.staticfiles import StaticFiles
import uvicorn
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')

app = FastAPI()

app.include_router(homapage_router)
app.include_router(about_me_router)
app.include_router(projects_router)
app.include_router(reels_router)
app.include_router(contact_router)
app.include_router(gallery_router)



app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
