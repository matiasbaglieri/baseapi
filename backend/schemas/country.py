from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CountryBase(BaseModel):
    name: str = Field(..., description="Country name")
    iso3: str = Field(..., description="ISO3 country code")
    iso2: Optional[str] = Field(None, description="ISO2 country code")
    numeric_code: Optional[str] = Field(None, description="Numeric country code")
    phonecode: Optional[str] = Field(None, description="Country phone code")
    capital: Optional[str] = Field(None, description="Country capital")
    currency: Optional[str] = Field(None, description="Currency code")
    currency_name: Optional[str] = Field(None, description="Currency name")
    currency_symbol: Optional[str] = Field(None, description="Currency symbol")
    tld: Optional[str] = Field(None, description="Top level domain")
    native: Optional[str] = Field(None, description="Native name")
    nationality: Optional[str] = Field(None, description="Nationality")
    timezones: Optional[List[Dict[str, Any]]] = Field(None, description="List of timezones")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    emoji: Optional[str] = Field(None, description="Country emoji")
    emojiU: Optional[str] = Field(None, description="Country emoji Unicode")
    region: Optional[str] = Field(None, description="Region name")
    subregion: Optional[str] = Field(None, description="Subregion name")

class CountryResponse(CountryBase):
    id: int
    country_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CountrySearchParams(BaseModel):
    name: Optional[str] = None
    iso2: Optional[str] = None
    iso3: Optional[str] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    currency: Optional[str] = None
    page: int = 1
    per_page: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page

class CountrySearchResponse(BaseModel):
    message: str = "Countries found successfully"
    status: str = "success"
    data: List[CountryResponse]
    total: int 