from fastapi import APIRouter

# importer manuellement chaque fichier d'endpoint du dossier v1
from . import ping

router = APIRouter(tags=["default"])

# chaque fichier définit son propre `router` (sans prefix)
# on inclut ici manuellement les routers avec un sous-prefix (chemin final = /v1/users, /v1/items)

router.include_router(ping.router)