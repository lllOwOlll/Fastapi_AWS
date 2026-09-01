from fastapi import FastAPI
from routers import images, jobs
import socket


app = FastAPI()

@app.get("/whoami")
def whoami():
    return {
        "hostname": socket.gethostname()
    }

app.include_router(images.router)
app.include_router(jobs.router)