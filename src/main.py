import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import events
from api.routers import tasks
from api.routers import monitor
from api.routers import management
from api.routers import root
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
app.include_router(monitor.router)
app.include_router(management.router)
app.include_router(root.router)

# t = task.Task()
# t.start()
