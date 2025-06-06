from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class State(Base):
    __tablename__ = "states"
    #state_id,name,country_id,country_code,country_name,state_code,type,latitude,longitude
    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, index=True)
    name = Column(String(100), nullable=False, index=True)
    country_id = Column(Integer, nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)
    country_name = Column(String(100), nullable=False)
    state_code = Column(String(10), nullable=True, index=True)
    type = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


    # Add constraints for coordinates
    __table_args__ = (
        CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_state_latitude_range'),
        CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_state_longitude_range'),
    )

    def __repr__(self):
        return f"<State {self.name} ({self.country_code})>"

    @property
    def coordinates(self):
        """Return coordinates as a tuple (latitude, longitude)"""
        return (self.latitude, self.longitude) if self.latitude and self.longitude else None

    @property
    def full_name(self):
        """Return the full name of the state including country"""
        return f"{self.name}, {self.country_name}" 