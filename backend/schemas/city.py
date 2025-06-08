from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CityBase(BaseModel):
    name: str
    state_id: int
    state_code: Optional[str] = None
    state_name: str
    country_id: int
    country_code: str
    country_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    wikiDataId: Optional[str] = None

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CitySearchParams(BaseModel):
    name: Optional[str] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    country_code: Optional[str] = None
    wikiDataId: Optional[str] = None
    page: int = 1
    per_page: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page

class CitySearchResponse(BaseModel):
    message: str
    status: str
    data: List[CityResponse]
    total: int

class StateResponse(BaseModel):
    state_id: int
    state_name: str
    state_code: Optional[str] = None
    country_id: int
    country_code: str
    country_name: str

    class Config:
        from_attributes = True

class StateSearchResponse(BaseModel):
    message: str
    status: str
    data: List[StateResponse]
    total: int 