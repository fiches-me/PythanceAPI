from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import mail
from random import randint
from database import SimpleDB
import os

router = APIRouter()
db = SimpleDB(os.environ["DATABASE_LINK"])

# modèles définis dans ce fichier (selon ta contrainte)
class LoginRequest(BaseModel):
    email: str

class SuccessRequest(BaseModel):
    success: bool

def random_code() -> str:
    acc = ""
    for _ in range(6):
        acc += str(randint(0, 9))
    return acc


@router.post("/", response_model=SuccessRequest)
async def login_request(payload: LoginRequest):
    """
    Login request. Send a magic code to the asked email.
    """
    try:
        code = random_code()
        email_value = payload.email
        try:
            db.execute("INSERT INTO codes (email, code) VALUES (?, ?)", (email_value, code))
        except Exception as e:
            print(f"Erreur détaillée : {e}")
            print(f"Type de payload.email : {type(payload.email)}")
            print(f"Type de code : {type(code)}")
        mail.MailHelper().verification_email(email_value, code)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": e}, 403
