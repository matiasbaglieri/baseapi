from pydantic import BaseModel, Field
from typing import Optional, List

class CityBase(BaseModel):
    name: str
    country_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state: Optional[str] = None
    state_code: Optional[str] = None
    population: Optional[int] = None
    timezone: Optional[str] = None

class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True

class CitySearchParams(BaseModel):
    name: Optional[str] = Field(None, description="Partial name to search for")
    country_id: Optional[int] = Field(None, description="Country ID to filter by")
    limit: int = Field(10, description="Maximum number of results to return")
    offset: int = Field(0, description="Number of results to skip")

class CitySearchResponse(BaseModel):
    message: str
    status: str
    data: List[CityResponse]
    total: int 