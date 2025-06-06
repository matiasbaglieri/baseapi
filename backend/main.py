from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth, user, subscription
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(subscription.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"} 