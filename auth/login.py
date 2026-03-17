from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import mail
from random import randint
from datetime import datetime, timedelta
from database import db

router = APIRouter()

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

        now = datetime.now()

        try:
            existing = db.select_one("codes", {"email": email_value})
        except Exception as e:
            print(f"Erreur select codes : {e}")
            existing = None

        # If a code exists and is recent (less than 15 minutes), refuse and return a friendly error
        if existing and existing.get("created_at"):
            created = existing["created_at"]
            if isinstance(created, str):
                try:
                    created = datetime.fromisoformat(created)
                except Exception:
                    created = None

            if created:
                delta = now - created
                if delta.total_seconds() < 15 * 60:
                    remaining = int((15 * 60 - delta.total_seconds()) // 60) + 1
                    raise HTTPException(
                        status_code=429,
                        detail=f"Un code a déjà été envoyé. Réessayez dans {remaining} minute(s)."
                    )

        # Insert a new code or update the old one if expired
        try:
            if existing:
                db.update("codes", {"email": email_value}, {"code": code, "created_at": now})
            else:
                db.insert("codes", {"email": email_value, "code": code, "created_at": now})
        except Exception as e:
            print(f"Erreur détaillée : {e}")
            print(f"Type de payload.email : {type(payload.email)}")
            print(f"Type de code : {type(code)}")
            raise HTTPException(status_code=500, detail="failed to store code")

        mail.MailHelper().verification_email(email_value, code)
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
