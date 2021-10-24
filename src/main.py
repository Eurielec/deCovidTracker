import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import events
from api.routers import tasks
# from utilities import task

app = FastAPI(title="deCovidTracker",
              events={
                  "type": "access | exit",
                  "time": "datetime object of the event",
                  "email": "upm email account",
                  "nif_nie": "spanish id",
                  "association": "association name"
              })

origins = [
    "http://localhost:3000",
    os.environ.get("FRONTEND_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(events.router)
app.include_router(tasks.router)

# t = task.Task()
# t.start()
