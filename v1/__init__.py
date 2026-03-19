from fastapi import APIRouter, Depends
from utils.verify_token import verify_token

# importer manuellement chaque fichier d'endpoint du dossier v1
from . import get_plates, create_plate
router = APIRouter(prefix="/plates", tags=["v1"], dependencies=[Depends(verify_token)])

# chaque fichier définit son propre `router` (sans prefix)
# on inclut ici manuellement les routers avec un sous-prefix (chemin final = /v1/users, /v1/items)


router.include_router(get_plates.router, prefix="", tags=["v1"])
router.include_router(create_plate.router, prefix="", tags=["v1"])