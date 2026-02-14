from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db

router = APIRouter()


@router.get("/")
async def get_plates():
    """
    Get the list of planned plates.
    """
    oid = 0
    db.select("plates", where={"org_id", oid})
    return {"status": "online"}
