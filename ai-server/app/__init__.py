from .services import *

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, StreamingResponse
from typing import Callable

from .api.restx_config import init_app 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_app(app) 

"""
   Custom responses
"""

class CustomResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": False, "msg": exc.detail}
            )
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"success": False, "msg": "An internal server error occurred"}
            )

        if response.status_code >= 400:
            response_data = await self.process_response(response)
            return JSONResponse(content=response_data, status_code=response.status_code)
        
        return response

    async def process_response(self, response):
        if isinstance(response, StreamingResponse):
            return {'success': False, 'msg': 'Streaming error occurred'}

        try:
            response_body = [chunk async for chunk in response.body_iterator]
            response_data = json.loads("".join(map(bytes.decode, response_body)))
        except json.JSONDecodeError:
            response_data = {'errors': {'general': 'Invalid request.'}}
        
        if 'errors' in response_data:
            msg = list(response_data['errors'].values())[0]
            if isinstance(msg, list):
                msg = msg[0]  
            response_data = {'success': False, 'msg': msg}
        else:
            response_data = {'success': False, 'msg': 'An error occurred'}

        return response_data

app.add_middleware(CustomResponseMiddleware)


