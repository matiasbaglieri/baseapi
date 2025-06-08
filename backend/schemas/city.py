from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CityBase(BaseModel):
    name: str = Field(..., description="City name")
    country_id: int = Field(..., description="ID of the country this city belongs to")
    state_id: Optional[int] = Field(None, description="ID of the state/province this city belongs to")
    latitude: Optional[float] = Field(None, description="City's latitude")
    longitude: Optional[float] = Field(None, description="City's longitude")
    timezone: Optional[str] = Field(None, description="City's timezone")
    population: Optional[int] = Field(None, description="City's population")
    is_active: bool = Field(True, description="Whether the city is active")

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, description="City name")
    country_id: Optional[int] = Field(None, description="ID of the country this city belongs to")
    state_id: Optional[int] = Field(None, description="ID of the state/province this city belongs to")
    latitude: Optional[float] = Field(None, description="City's latitude")
    longitude: Optional[float] = Field(None, description="City's longitude")
    timezone: Optional[str] = Field(None, description="City's timezone")
    population: Optional[int] = Field(None, description="City's population")
    is_active: Optional[bool] = Field(None, description="Whether the city is active")

class CityResponse(CityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CitySearchParams(BaseModel):
    name: Optional[str] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    is_active: Optional[bool] = None
    page: int = 1
    per_page: int = 10

class CitySearchResponse(BaseModel):
    items: List[CityResponse]
    total: int
    page: int
    per_page: int 