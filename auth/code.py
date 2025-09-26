from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import mail

router = APIRouter()

# modèles définis dans ce fichier (selon ta contrainte)
class UserIn(BaseModel):
    email: str

@router.post("/")
async def send_mail_code(payload: UserIn):
    try:
        mail.MailHelper().verification_email(payload.email, 1111)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": e}, 500
