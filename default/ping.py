from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
async def ping():
    # logique de création → remplace par DB
    return {"status": "online"}
