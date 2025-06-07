from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth, user, subscription
from database import engine, Base
from controllers.user import router as user_router
from controllers.payment import router as payment_router
from controllers.subscription import router as subscription_router
from controllers.notification.notification_controller import router as notification_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Base API",
    description="Base API with user management, payments, and subscriptions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router)
app.include_router(user_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(subscription_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Base API"} 