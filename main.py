from fastapi import FastAPI
from v1 import router as v1_router
from auth import router as auth_router
from default import router as default_router

from utils.init_database import init_database_scheme
from database import SimpleDB

# Load App
app = FastAPI(title="Pythance API")

# Load and initialize database
#db = SimpleDB("sqlite:///local.db")
#init_database_scheme(db)

app.include_router(default_router)
app.include_router(v1_router)
app.include_router(auth_router)
