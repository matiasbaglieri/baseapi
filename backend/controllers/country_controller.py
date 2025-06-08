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
    iso2: Optional[str] = Query(None, description="ISO2 country code"),
    iso3: Optional[str] = Query(None, description="ISO3 country code"),
    region: Optional[str] = Query(None, description="Region name"),
    subregion: Optional[str] = Query(None, description="Subregion name"),
    currency: Optional[str] = Query(None, description="Currency code"),
    limit: int = Query(10, description="Maximum number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    Search for countries with various filters.
    Returns a list of countries that match the search criteria.
    """
    try:
        country_service = CountryService(db)
        search_params = CountrySearchParams(
            name=name,
            iso2=iso2,
            iso3=iso3,
            region=region,
            subregion=subregion,
            currency=currency,
            page=offset // limit + 1,
            per_page=limit
        )
        return country_service.search_countries(search_params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 