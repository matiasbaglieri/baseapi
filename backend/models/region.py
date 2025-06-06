from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, index=True)
    name = Column(String(100), nullable=False, index=True)
    wikiDataId = Column(String(50), unique=True, nullable=True, index=True)

    def __repr__(self):
        return f"<Region {self.name}>"

    @property
    def country_count(self):
        """Return the number of countries in this region"""
        return len(self.countries) if self.countries else 0

    @property
    def subregion_count(self):
        """Return the number of subregions in this region"""
        return len(self.subregions) if self.subregions else 0 