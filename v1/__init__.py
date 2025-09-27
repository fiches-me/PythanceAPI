from fastapi import APIRouter

# importer manuellement chaque fichier d'endpoint du dossier v1
from . import plates
router = APIRouter(prefix="/v1", tags=["v1"])

# chaque fichier définit son propre `router` (sans prefix)
# on inclut ici manuellement les routers avec un sous-prefix (chemin final = /v1/users, /v1/items)


router.include_router(plates.router, prefix="/plates", tags=["v1"])