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
    plates = db.select("plates", where={"org_id": oid})
    return {"success": True, "plates": plates or []}

@router.post("/")
async def add_plate(payload: PlateRequest):
    """
    Add a new planned plate.
    """
    # Dummy mock insertion
    if not payload.name:
        raise HTTPException(status_code=400, detail="Name is required")
        
    # Example logic matching the flask mock
    return {"success": True, "message": "Plate added."}
