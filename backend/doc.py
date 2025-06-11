from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import app 

app_docs = FastAPI(
    title=f"Dokumentation für '{app.title}'",
    version=app.version,
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc"
)

openapi_schema = get_openapi(
    title=app_docs.title,
    version=app_docs.version,
    routes=app.routes,
)

app_docs.openapi_schema = openapi_schema

def custom_openapi():
    return app_docs.openapi_schema

app_docs.openapi = custom_openapi