from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.base import router as base_router
from controllers.user import router as user_router
from core.init_db import init_db, get_db
from core.utils import parse_json_env_var
import os
from dotenv import load_dotenv

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

app.include_router(base_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    
    # Initialize database
    init_db()
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True) 