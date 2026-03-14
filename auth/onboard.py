from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class OnboardResponse(BaseModel):
    success: bool
    message: str

@router.post("/", response_model=OnboardResponse)
async def onboard(request: Request, authorization: Optional[str] = Header(None)):
    """
    Onboarding endpoint.
    In a real app, we'd check the Authorization header properly.
    """
    if not authorization:
         raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    print(f"Onboarding data received: {data}")
    return {"success": True, "message": "Onboarding completed."}