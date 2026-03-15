from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from collections.abc import Mapping
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
    print(f"Looking up code for email: {payload.email}")
    record = db.select_one("codes", where={"email": payload.email})
    if not record:
        print(f"No code found for email: {payload.email}")
        raise HTTPException(status_code=404, detail="code not found")

    # extract the stored code (handle Mapping, dict or tuple/sequence result)
    if isinstance(record, Mapping):
        stored_code = record.get("code")
    else:
        try:
            stored_code = record[1]
        except Exception:
            stored_code = None

    if stored_code != payload.code:
        print(f"Invalid code for email: {payload.email}. Expected: {stored_code}, Received: {payload.code}")
        raise HTTPException(status_code=403, detail="invalid code")

    user = db.select_one("users", where={"email": payload.email})
    first_login = False
    if not user:
        print(f"User not found for email: {payload.email} — creating new user")
        try:
            db.insert("users", {"name": "", "email": payload.email})
        except Exception as e:
            print(f"Failed to create user: {e}")
            raise HTTPException(status_code=500, detail="failed to create user")

        # re-fetch the created user
        user = db.select_one("users", where={"email": payload.email})
        if not user:
            raise HTTPException(status_code=500, detail="user creation failed")
        first_login = True

    # extract user id (Mapping-compatible or sequence)
    if isinstance(user, Mapping):
        user_id = user.get("id")
    else:
        try:
            user_id = user[0]
        except Exception:
            try:
                user_id = user.get("id")
            except Exception:
                user_id = None

    try:
        user_id = int(user_id)
    except Exception:
        print(f"Invalid user id for email: {payload.email}. Value: {user_id}")
        raise HTTPException(status_code=500, detail="invalid user id")

    # minimal successful response (token generation left as TODO)
    return {"success": True, "id": user_id, "key": "", "first_login": first_login}
