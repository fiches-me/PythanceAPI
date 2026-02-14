from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db

router = APIRouter()

class CodeRequest(BaseModel):
    email: str
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
    code = db.select_one("codes", where={"email", CodeRequest.email})
    if code == CodeRequest.code:
        user = db.select_one("users", where={"email", CodeRequest.email})
        print("DEBUG:", user)
        return {"success" : True, id: user[0]}
    return
