from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from decouple import config

API_KEY=config("API_KEY")
