from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.database import get_db
from services.city.city_service import CityService
from schemas.base import BaseResponse
from schemas.city import CitySearchParams, CitySearchResponse
from typing import Optional

router = APIRouter()

@router.post("/init_cities", response_model=BaseResponse)
async def init_cities(db: Session = Depends(get_db)):
    """
    Initialize cities in the database.
    This endpoint will populate the cities table with predefined data.
    """
    try:
        city_service = CityService(db)
        result = await city_service.initialize_cities()
        
        return {
            "message": "Cities initialized successfully",
            "status": "success",
            "data": {
                "total_cities": result.get("total_cities", 0),
                "added_cities": result.get("added_cities", 0),
                "updated_cities": result.get("updated_cities", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/search", response_model=CitySearchResponse)
async def search_cities(
    name: Optional[str] = Query(None, description="Partial name to search for"),
    country_id: Optional[int] = Query(None, description="Country ID to filter by"),
    limit: int = Query(10, description="Maximum number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    Search for cities by name and/or country_id.
    If name is not provided, it will search by country_id only.
    """
    try:
        city_service = CityService(db)
        cities = city_service.search_cities(
            name=name,
            country_id=country_id,
            limit=limit,
            offset=offset
        )
        
        return {
            "message": "Cities found successfully",
            "status": "success",
            "data": cities,
            "total": len(cities)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 