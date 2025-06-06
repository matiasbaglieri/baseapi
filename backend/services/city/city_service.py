from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.city import City
from models.country import Country
from sqlalchemy import or_, and_, func
from typing import List, Optional
import json
import os
from pathlib import Path
import pandas as pd
from schemas.city import CityCreate, CityUpdate, CityResponse, CitySearchParams, CitySearchResponse

class CityService:
    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, name: str, country_id: int = None) -> City:
        """
        Find a city by its name and optionally country.
        
        Args:
            name (str): Name of the city to find
            country_id (int, optional): ID of the country to filter by
            
        Returns:
            City: The found city
            
        Raises:
            HTTPException: If city is not found
        """
        query = self.db.query(City).filter(City.name == name)
        if country_id:
            query = query.filter(City.country_id == country_id)
            
        city = query.first()
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{name}' not found"
            )
        return city

    def validate_city(self, city_name: str, country_id: int) -> City:
        """
        Validate city by name and country.
        
        Args:
            city_name (str): Name of the city
            country_id (int): ID of the country
            
        Returns:
            City: The found city
            
        Raises:
            HTTPException: If city is not found or validation fails
        """
        if not city_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City name must be provided"
            )
            
        if not country_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Country must be provided to validate city"
            )

        return self.find_by_name(city_name, country_id)

    def search_cities(
        self,
        name: Optional[str] = None,
        country_id: Optional[int] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[City]:
        """
        Search for cities by name and/or country_id.
        
        Args:
            name (str, optional): Partial name to search for
            country_id (int, optional): Country ID to filter by
            limit (int): Maximum number of results to return
            offset (int): Number of results to skip
            
        Returns:
            List[City]: List of matching cities
        """
        query = self.db.query(City)

        # Apply filters
        if name:
            query = query.filter(func.lower(City.name).like(f"%{name.lower()}%"))
        
        if country_id:
            query = query.filter(City.country_id == country_id)
        
        # Add ordering
        query = query.order_by(City.name)
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        return query.all()

    def _parse_coordinates(self, value: str) -> Optional[float]:
        """Parse coordinate string to float."""
        if not value or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def initialize_cities(self) -> dict:
        """
        Initialize cities in the database from a CSV file using pandas.
        id,name,state_id,state_code,state_name,country_id,country_code,country_name,latitude,longitude,wikiDataId 
        Returns:
            dict: Statistics about the initialization process
        """
        # Get the path to the cities.csv file
        base_path = Path(__file__).parent.parent.parent
        cities_file = base_path / "dump" / "cities.csv"
        
        if not cities_file.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cities data file not found"
            )
        
        # Read CSV file using pandas
        try:
            df = pd.read_csv(cities_file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading cities file: {str(e)}"
            )
        
        total_cities = len(df)
        added_cities = 0
        updated_cities = 0
        skipped_cities = 0
        error_cities = 0
        
        # Process each city
        for _, row in df.iterrows():
            try:
                # Get country by ISO2 code
                country = self.db.query(Country).filter(
                    Country.country_id == int(row[5])
                ).first()
                
                if not country:
                    skipped_cities += 1
                    continue  # Skip if country doesn't exist
                
                # Parse coordinates
                latitude = self._parse_coordinates(row[8])
                longitude = self._parse_coordinates(row[9])
                
                # Check if city already exists
                existing_city = self.db.query(City).filter(
                    City.name == str(row[1]),
                    City.country_id == int(row[5])
                ).first()
                
                if existing_city:
                    # Update existing city with type validation
                    existing_city.city_id = int(row[0])
                    existing_city.name = str(row[1])
                    existing_city.state_id = str(row[2]) if pd.notna(row[2]) else None
                    existing_city.state_code = str(row[3]) if pd.notna(row[3]) else None
                    existing_city.state_name = str(row[4]) if pd.notna(row[4]) else None
                    existing_city.country_id = country.id
                    existing_city.country_code = str(row[6])
                    existing_city.country_name = str(row[7])
                    existing_city.latitude = latitude
                    existing_city.longitude = longitude
                    existing_city.wikiDataId = str(row[10]) if pd.notna(row[10]) else None
                    updated_cities += 1
                else:
                    # Create new city with type validation
                    new_city = City(
                        city_id=int(row[0]),
                        name=str(row[1]),
                        state_id=str(row[2]) if pd.notna(row[2]) else None,
                        state_code=str(row[3]) if pd.notna(row[3]) else None,
                        state_name=str(row[4]) if pd.notna(row[4]) else None,
                        country_id=int(row[5]),
                        country_code=str(row[6]),
                        country_name=str(row[7]),
                        latitude=latitude,
                        longitude=longitude,
                        wikiDataId=str(row[10]) if pd.notna(row[10]) else None
                    )
                    self.db.add(new_city)
                    added_cities += 1
            except Exception as e:
                error_cities += 1
                print(f"Error processing city {row[1]}: {str(e)}")
                continue
        
        # Commit changes
        self.db.commit()
        
        return {
            "total_cities": total_cities,
            "added_cities": added_cities,
            "updated_cities": updated_cities,
            "skipped_cities": skipped_cities,
            "error_cities": error_cities
        }

    def get_city(self, city_id: int) -> Optional[City]:
        """Get a city by ID."""
        return self.db.query(City).filter(City.id == city_id).first()

    def get_cities(
        self,
        skip: int = 0,
        limit: int = 100,
        country_id: Optional[int] = None
    ) -> List[City]:
        """Get a list of cities with optional filtering."""
        query = self.db.query(City)
        
        if country_id is not None:
            query = query.filter(City.country_id == country_id)
        
        return query.offset(skip).limit(limit).all()

    def create_city(self, city: CityCreate) -> City:
        """Create a new city."""
        db_city = City(**city.dict())
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city

    def update_city(self, city_id: int, city: CityUpdate) -> Optional[City]:
        """Update a city."""
        db_city = self.get_city(city_id)
        if db_city:
            for key, value in city.dict(exclude_unset=True).items():
                setattr(db_city, key, value)
            self.db.commit()
            self.db.refresh(db_city)
        return db_city

    def delete_city(self, city_id: int) -> bool:
        """Delete a city."""
        db_city = self.get_city(city_id)
        if db_city:
            self.db.delete(db_city)
            self.db.commit()
            return True
        return False

    def search_cities(self, params: CitySearchParams) -> CitySearchResponse:
        """
        Search for cities with various filters and pagination.
        
        Args:
            params (CitySearchParams): Search parameters including name, country_id, and pagination
            
        Returns:
            CitySearchResponse: Search results with pagination info
        """
        query = self.db.query(City)
        
        # Apply filters
        if params.name:
            query = query.filter(City.name.ilike(f"%{params.name}%"))
        if params.country_id:
            query = query.filter(City.country_id == params.country_id)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        cities = query.order_by(City.name).offset(params.offset).limit(params.limit).all()
        
        return CitySearchResponse(
            message="Cities found successfully",
            status="success",
            data=[CityResponse.from_orm(city) for city in cities],
            total=total
        ) 