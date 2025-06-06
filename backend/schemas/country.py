from pydantic import BaseModel, Field
from typing import Optional, List

class CountryBase(BaseModel):
    name: str
    iso2: str
    iso3: str
    phone_code: Optional[str] = None
    currency: Optional[str] = None
    currency_symbol: Optional[str] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    emoji: Optional[str] = None

class CountryResponse(CountryBase):
    id: int

    class Config:
        from_attributes = True

class CountrySearchParams(BaseModel):
    name: Optional[str] = Field(None, description="Partial name to search for")
    limit: int = Field(10, description="Maximum number of results to return")
    offset: int = Field(0, description="Number of results to skip")

class CountrySearchResponse(BaseModel):
    message: str
    status: str
    data: List[CountryResponse]
    total: int 