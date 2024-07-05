from fastapi import FastAPI
from .endpoints.documents import router as documents_router

def init_app(app: FastAPI):
    app.include_router(documents_router, prefix="/api/v1")
