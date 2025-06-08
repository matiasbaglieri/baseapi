from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from core.init_db import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    name = Column(String(100), nullable=False, index=True)
    state_id = Column(Integer, nullable=False, index=True)
    state_code = Column(String(10), nullable=True, index=True)
    state_name = Column(String(100), nullable=False)
    country_id = Column(Integer,  nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)
    country_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    wikiDataId = Column(String(50), nullable=True, index=True)

    # Add relationship with Users
    users = relationship("User", back_populates="city")

    # Add constraints for coordinates
    __table_args__ = (
        CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_city_latitude_range'),
        CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_city_longitude_range'),
    )

    def __repr__(self):
        return f"<City {self.name}>"

    @property
    def coordinates(self):
        """Return coordinates as a tuple (latitude, longitude)"""
        return (self.latitude, self.longitude) if self.latitude and self.longitude else None

    @property
    def full_name(self):
        """Return the full name including state and country"""
        return f"{self.name}, {self.state_name}, {self.country_name}"

    @property
    def location_info(self):
        """Return location information as a dictionary"""
        return {
            "city": self.name,
            "state": self.state_name,
            "country": self.country_name,
            "coordinates": self.coordinates
        } 