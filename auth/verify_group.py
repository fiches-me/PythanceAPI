from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class VerifyGroupRequest(BaseModel):
    group_code: str

class VerifyGroupResponse(BaseModel):
    success: bool
    valid: bool

@router.post("/", response_model=VerifyGroupResponse)
async def verify_group(payload: VerifyGroupRequest):
    """
    Check if a group code is valid.
    """
    is_valid = bool(payload.group_code and len(payload.group_code) > 3)
    return {"success": True, "valid": is_valid}
