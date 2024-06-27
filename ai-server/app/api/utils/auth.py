from fastapi import Request, HTTPException, Depends
from ...common.config import BaseConfig

async def require_secret_key(request: Request):
    api_key: str = request.headers.get("finsecured_api_key", "")
    if not api_key:
        raise HTTPException(status_code=403, detail="No API key provided.")
    if api_key != BaseConfig.FINSECURED_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key.")
    return api_key
