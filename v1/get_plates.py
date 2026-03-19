from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import db

router = APIRouter()

class PlateRequest(BaseModel):
    name: str

@router.get("/")
async def get_plates():
    """
    Get the list of planned plates.
    """
    oid = 0
    try:
        plates = db.select("plates", where={"org_id": oid})
    except Exception as e:
        print(f"Database error: {e}")
        plates = []
    return {"success": True, "plates": plates or []}