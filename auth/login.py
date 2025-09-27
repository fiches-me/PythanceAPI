from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import mail

router = APIRouter()

# modèles définis dans ce fichier (selon ta contrainte)
class LoginRequest(BaseModel):
    email: str

class SuccessRequest(BaseModel):
    success: bool


@router.post("/", response_model=SuccessRequest)
async def login_request(payload: LoginRequest):
    """
    Login request. Send a magic code to the asked email.
    """
    try:
        mail.MailHelper().verification_email(payload.email, 1111)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": e}, 500
