from sqlalchemy import Column, Integer, String, Float, JSON, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, validates
from core.init_db import Base
import re
from typing import Optional, Union, List

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, index=True)
    name = Column(String(100), nullable=False, index=True)
    iso3 = Column(String(3), unique=True, nullable=False, index=True)
    iso2 = Column(String(2), nullable=True, index=True)
    numeric_code = Column(String(3), nullable=True)
    phonecode = Column(String(20), nullable=True)
    capital = Column(String(100), nullable=True)
    currency = Column(String(3), nullable=True)
    currency_name = Column(String(50), nullable=True)
    currency_symbol = Column(String(10), nullable=True)
    tld = Column(String(10), nullable=True)
    native = Column(String(100), nullable=True)
    nationality = Column(String(100), nullable=True)
    timezones = Column(JSON, nullable=True)  # Store as JSON array
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    emoji = Column(String(10), nullable=True)
    emojiU = Column(String(20), nullable=True)
    region = Column(String(50), nullable=True, index=True)
    subregion = Column(String(50), nullable=True, index=True)

    # Relationship with Users
    users = relationship("User", back_populates="country")

    # Add constraints for coordinates
    __table_args__ = (
        CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_latitude_range'),
        CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_longitude_range'),
    )

    @validates('iso3')
    def validate_iso3(self, key: str, value: str) -> str:
        """Validate ISO3 code format."""
        if not value or not re.match(r'^[A-Z]{3}$', value):
            raise ValueError('ISO3 code must be exactly 3 uppercase letters')
        return value

    @validates('iso2')
    def validate_iso2(self, key: str, value: str) -> str:
        """Validate ISO2 code format."""
        if not value:
            return None
        if not re.match(r'^[A-Z]{2}$', value):
            raise ValueError('ISO2 code must be exactly 2 uppercase letters')
        return value

    @validates('numeric_code')
    def validate_numeric_code(self, key: str, value: Optional[str]) -> Optional[str]:
        """Validate numeric code format."""
        if value and not re.match(r'^\d{3}$', value):
            raise ValueError('Numeric code must be exactly 3 digits')
        return value

    @validates('phonecode')
    def validate_phonecode(self, key: str, value: Optional[str]) -> Optional[str]:
        """Validate phone code format."""
        if value and not re.match(r'^\+\d{1,4}$', value):
            raise ValueError('Phone code must start with + followed by 1-4 digits')
        return value

    @validates('currency')
    def validate_currency(self, key: str, value: Optional[str]) -> Optional[str]:
        """Validate currency code format."""
        if value and not re.match(r'^[A-Z]{3}$', value):
            raise ValueError('Currency code must be exactly 3 uppercase letters')
        return value

    @validates('tld')
    def validate_tld(self, key: str, value: Optional[str]) -> Optional[str]:
        """Validate TLD format."""
        if value and not re.match(r'^\.[a-z]{2,}$', value):
            raise ValueError('TLD must start with a dot followed by 2 or more lowercase letters')
        return value

    @validates('timezones')
    def validate_timezones(self, key: str, value: Optional[List[str]]) -> Optional[List[str]]:
        """Validate timezone format."""
        if value:
            if not isinstance(value, list):
                raise ValueError('Timezones must be a list')
            for tz in value:
                if not re.match(r'^[A-Za-z]+/[A-Za-z_]+$', tz):
                    raise ValueError(f'Invalid timezone format: {tz}')
        return value

    def __repr__(self):
        return f"<Country {self.name} ({self.iso3})>"

    @property
    def coordinates(self):
        """Return coordinates as a tuple (latitude, longitude)"""
        return (self.latitude, self.longitude) if self.latitude and self.longitude else None

    @property
    def currency_info(self):
        """Return currency information as a dictionary"""
        if not self.currency:
            return None
        return {
            "code": self.currency,
            "name": self.currency_name,
            "symbol": self.currency_symbol
        }

    @property
    def location_info(self):
        """Return location information as a dictionary"""
        return {
            "region": self.region,
            "subregion": self.subregion,
            "capital": self.capital,
            "coordinates": self.coordinates
        } 