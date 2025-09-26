from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# modèles définis dans ce fichier (selon ta contrainte)
class UserIn(BaseModel):
    email: str
    code: int

class UserOut(UserIn):
    id: int
    username: str
    avatar: str
    role_id: int
    token: str


@router.post("/", response_model=UserOut)
async def create_user(payload: UserIn):
    # logique de création → remplace par DB
    return {"id": 1, **payload.model_dump()}
