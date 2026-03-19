from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import db
from utils.verify_token import verify_token

router = APIRouter()


@router.get("/")
async def get_plates(data = Depends(verify_token)):
    """
    Get the list of planned plates.
    """
    try:
        plates = db.select("plates", where={"org_id": data.get('org_id')})
    except Exception as e:
        print(f"Database error: {e}")
        plates = []
    return {"success": True, "plates": plates or []}