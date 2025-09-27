from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
async def get_plates():
    """
    Get the list of planned plates.
    """
    # logique de création → remplace par DB
    return {"status": "online"}
