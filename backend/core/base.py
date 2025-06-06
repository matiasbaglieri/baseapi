from fastapi import APIRouter
from controllers.country import router as country_router

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello World"}

# Include country routes
router.include_router(country_router, prefix="/countries", tags=["countries"]) 