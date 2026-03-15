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
    # look up the stored code by email (use the payload instance)
    record = db.select_one("codes", where={"email": payload.email})
    if not record:
        raise HTTPException(status_code=404, detail="code not found")

    # extract the stored code (handle dict or tuple result)
    if isinstance(record, dict):
        stored_code = record.get("code")
    else:
        try:
            stored_code = record[1]
        except Exception:
            stored_code = None

    if stored_code != payload.code:
        raise HTTPException(status_code=403, detail="invalid code")

    user = db.select_one("users", where={"email": payload.email})
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    # extract user id
    if isinstance(user, dict):
        user_id = user.get("id")
    else:
        user_id = user[0]

    try:
        user_id = int(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="invalid user id")

    # minimal successful response (token generation left as TODO)
    return {"success": True, "id": user_id, "key": "", "first_login": False}
