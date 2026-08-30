from fastapi import FastAPI

from routers import images, jobs


app = FastAPI()


app.include_router(images.router)
app.include_router(jobs.router)