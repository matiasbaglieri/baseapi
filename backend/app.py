from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.base import router as base_router
from controllers.user import router as user_router
from controllers.user.email_validator_controller import router as email_validator_router
from core.init_db import init_db, get_db,drop_db
from core.utils import parse_json_env_var
from core.celery_app import celery_app, init_celery, shutdown_celery
from core.logger import logger
import os
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# CORS Configuration
DEFAULT_CORS_HEADERS = [
    "Content-Type",
    "sessionId",
    "Authorization",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Origin",
    "Access-Control-Request-Headers"
]

CORS_ORIGINS = parse_json_env_var("CORS_ORIGINS", ["*"])
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
CORS_METHODS = parse_json_env_var("CORS_METHODS", ["*"])
CORS_HEADERS = parse_json_env_var("CORS_HEADERS", DEFAULT_CORS_HEADERS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up FastAPI application...")
    init_celery()
    # drop_db()
    # init_db()  # Initialize database tables
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")
    shutdown_celery()
    logger.info("Shutdown complete")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routers
app.include_router(base_router)
app.include_router(user_router)
app.include_router(email_validator_router)

if __name__ == "__main__":
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True) 