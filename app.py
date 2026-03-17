from fastapi import FastAPI
from v1 import router as v1_router
from auth import router as auth_router
from default import router as default_router

from utils.init_database import init_database_scheme
from database import db

app = FastAPI(title="Pythance API")

init_database_scheme(db)

app.include_router(default_router)
app.include_router(v1_router)
app.include_router(auth_router)