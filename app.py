from fastapi import FastAPI
from v1 import router as v1_router
from auth import router as auth_router
from default import router as default_router

from utils.init_database import init_database_scheme
from database import SimpleDB

import os

# Load App
app = FastAPI(title="Pythance API")

# Load and initialize database
init_database_scheme(SimpleDB(os.environ["DATABASE_LINK"]))

app.include_router(default_router)
app.include_router(v1_router)
app.include_router(auth_router)
