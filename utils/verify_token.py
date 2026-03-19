from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import db

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    requestToken = credentials.credentials

    dbToken = db.select_one("tokens", where={"token": requestToken})
    if not dbToken:
        print(f"No token found: {requestToken}")
        raise HTTPException(status_code=401, detail="code not found")

    
    userId = dbToken.get('owner_id')
    dbUser = db.select_one("users", where={"id": userId})
    
    if not dbUser:
        print(f"No user with token found: {requestToken}, {userId}")
        raise HTTPException(status_code=404, detail="code not found")

    ordId = dbUser.get('org_id')

    return {"user_id": userId, "org_id": ordId}
