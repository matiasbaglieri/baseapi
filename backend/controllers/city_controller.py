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
    state_id: Optional[int] = Query(None, description="State ID to filter by"),
    state_code: Optional[str] = Query(None, description="State code to filter by"),
    state_name: Optional[str] = Query(None, description="Partial state name to search for"),
    country_code: Optional[str] = Query(None, description="Country code to filter by"),
    wikiDataId: Optional[str] = Query(None, description="WikiData ID to filter by"),
    limit: int = Query(10, description="Maximum number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    Search for cities with various filters.
    Returns a list of cities that match the search criteria.
    """
    try:
        city_service = CityService(db)
        search_params = CitySearchParams(
            name=name,
            country_id=country_id,
            state_id=state_id,
            state_code=state_code,
            state_name=state_name,
            country_code=country_code,
            wikiDataId=wikiDataId,
            page=offset // limit + 1,
            per_page=limit
        )
        return city_service.search_cities(search_params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 