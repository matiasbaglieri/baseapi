from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.database import get_db
from services.country.country_service import CountryService
from schemas.base import BaseResponse
from schemas.country import CountrySearchParams, CountrySearchResponse
from typing import Optional

router = APIRouter()

@router.post("/init_countries", response_model=BaseResponse)
async def init_countries(db: Session = Depends(get_db)):
    """
    Initialize countries in the database.
    This endpoint will populate the countries table with predefined data.
    """
    try:
        country_service = CountryService(db)
        result = await country_service.initialize_countries()
        
        return {
            "message": "Countries initialized successfully",
            "status": "success",
            "data": {
                "total_countries": result.get("total_countries", 0),
                "added_countries": result.get("added_countries", 0),
                "updated_countries": result.get("updated_countries", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/search", response_model=CountrySearchResponse)
async def search_countries(
    name: Optional[str] = Query(None, description="Partial name to search for"),
    limit: int = Query(10, description="Maximum number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    Search for countries by name.
    Returns a list of countries that match the search criteria.
    """
    try:
        country_service = CountryService(db)
        countries = country_service.search_countries(
            name=name,
            limit=limit,
            offset=offset
        )
        
        return {
            "message": "Countries found successfully",
            "status": "success",
            "data": countries,
            "total": len(countries)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 