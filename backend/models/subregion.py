from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Subregion(Base):
    __tablename__ = "subregions"
    #subregion_id,name,region_id,wikiDataId
    id = Column(Integer, primary_key=True, index=True)
    subregion_id = Column(Integer, index=True)
    name = Column(String(100), nullable=False, index=True)
    region_id = Column(Integer,  nullable=False, index=True)
    wikiDataId = Column(String(50), unique=True, nullable=True, index=True)

    def __repr__(self):
        return f"<Subregion {self.name}>"

    @property
    def country_count(self):
        """Return the number of countries in this subregion"""
        return len(self.countries) if self.countries else 0

    @property
    def full_name(self):
        """Return the full name including region"""
        return f"{self.name}, {self.region.name}" if self.region else self.name 