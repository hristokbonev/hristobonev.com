from fastapi import FastAPI
from routers.homepage_routers import router as homapage_router
from routers.about_me_routers import router as about_me_router
from routers.projects_routers import router as projects_router
from routers.reels_routers import router as reels_router
from routers.contact_routers import router as contact_router
from routers.gallery_routers import router as gallery_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()


app.include_router(homapage_router)
app.include_router(about_me_router)
app.include_router(projects_router)
app.include_router(reels_router)
app.include_router(contact_router)
app.include_router(gallery_router)



app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")




if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
