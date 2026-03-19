from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1 import router as v1_router
from auth import router as auth_router
from default import router as default_router

from utils.init_database import init_database_scheme
from database import db

origins = [
    "https://pythance.fiches.me",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI(title="Pythance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database_scheme(db)

app.include_router(default_router)
app.include_router(v1_router)
app.include_router(auth_router)