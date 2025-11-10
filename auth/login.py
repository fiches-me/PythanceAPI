from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import mail
from random import randint
from database import get_session
from models import Code

router = APIRouter()

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
        with get_session() as session:
            code_obj = Code(email=email_value, code=code)
            session.add(code_obj)
            session.commit()
        mail.MailHelper().verification_email(email_value, code)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
