from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Tools(BaseModel):
    type: int

class UserIn(BaseModel):
    name: str
    last_name: str
    tools: list[Tools]
    group: int

class SuccessRequest(BaseModel):
    success: bool


@router.post("/", response_model=SuccessRequest)
async def create_user(payload: UserIn):
    """
    Ovveride dummy data to create a user account. Can only be run once.
    """
    # logique de création → remplace par DB
    return {"success": True}
