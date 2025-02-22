from fastapi import Request, HTTPException, Depends
from ..config import BaseConfig

async def require_secret_key(request: Request):
    api_key: str = request.headers.get("X-API-Key", "")
    if not api_key:
        raise HTTPException(status_code=403, detail="No API key provided.")
    if api_key != BaseConfig.FINSECURED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key.")
    return api_key
