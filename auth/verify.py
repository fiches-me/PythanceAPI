from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import SimpleDB
import os

router = APIRouter()
db = SimpleDB(os.environ["DATABASE_LINK"])

# modèles définis dans ce fichier (selon ta contrainte)
class CodeRequest(BaseModel):
    code: str

class SuccessUserLogin(BaseModel):
    success: bool
    id: int
    key: str
    first_login: bool

@router.post("/", response_model=SuccessUserLogin)
async def send_mail_code(payload: CodeRequest):
    """
    Check verification code & validity.
    If valid, sends back a token and some accounts infos.
    """
    return
