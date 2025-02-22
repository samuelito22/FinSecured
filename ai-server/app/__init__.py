from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, StreamingResponse
from typing import Callable
from fastapi.exceptions import RequestValidationError
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .config import BaseConfig
from fastapi.concurrency import run_in_threadpool


from .restx_config import init_app 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[BaseConfig.CORS_ORIGIN], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embed_model = None

@app.on_event("startup")
async def load_model():
    global embed_model
    # Load model asynchronously and store it globally
    embed_model = await run_in_threadpool(lambda: HuggingFaceEmbedding(model_name="thenlper/gte-large"))

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": str(exc)},
    )


init_app(app) 


