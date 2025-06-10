from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.base_controller import router as base_router
from controllers.user import router as user_router
from controllers.user.email_validator_controller import router as email_validator_router
from controllers.country_controller import router as country_router
from controllers.city_controller import router as city_router
from controllers.payment import router as payment_router
from controllers.stripe import subscription_router, subscription_user_router
from controllers.notification.notification_controller import router as notification_router
from controllers.user.authorization_controller import router as authorization_router
from controllers.admin.admin_controller import router as admin_router
from controllers.admin.dashboard_admin_controller import router as dashboard_router
from core.init_db import init_db, get_db, drop_db
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

app = FastAPI(
    title="Base API",
    description="Base API with user management and location services",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routers
app.include_router(base_router)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(email_validator_router, prefix="/email", tags=["email"])
app.include_router(country_router, prefix="/countries", tags=["countries"])
app.include_router(city_router, prefix="/cities", tags=["cities"])
app.include_router(payment_router, prefix="/payments", tags=["payments"])
app.include_router(subscription_router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(subscription_user_router, prefix="/subscription-users", tags=["subscription-users"])
app.include_router(notification_router, prefix="/notifications", tags=["notifications"])
app.include_router(authorization_router, prefix="/authz", tags=["authorization"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(dashboard_router, prefix="/admin/dashboard", tags=["admin-dashboard"])

if __name__ == "__main__":
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)