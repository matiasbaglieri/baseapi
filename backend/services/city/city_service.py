from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.city import City
from models.country import Country
from sqlalchemy import or_, and_, func
from typing import List, Optional
import json
import os
from pathlib import Path

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

    async def initialize_cities(self) -> dict:
        """
        Initialize cities in the database from a JSON file.
        
        Returns:
            dict: Statistics about the initialization process
        """
        # Get the path to the cities.json file
        base_path = Path(__file__).parent.parent.parent
        cities_file = base_path / "data" / "cities.json"
        
        if not cities_file.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cities data file not found"
            )
        
        # Read and parse the JSON file
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        
        total_cities = len(cities_data)
        added_cities = 0
        updated_cities = 0
        
        # Process each city
        for city_data in cities_data:
            # Get country by ISO2 code
            country = self.db.query(Country).filter(
                Country.iso2 == city_data['country_code']
            ).first()
            
            if not country:
                continue  # Skip if country doesn't exist
            
            # Check if city already exists
            existing_city = self.db.query(City).filter(
                City.name == city_data['name'],
                City.country_id == country.id
            ).first()
            
            if existing_city:
                # Update existing city
                existing_city.name = city_data['name']
                existing_city.latitude = city_data.get('latitude')
                existing_city.longitude = city_data.get('longitude')
                existing_city.state = city_data.get('state')
                existing_city.state_code = city_data.get('state_code')
                existing_city.population = city_data.get('population')
                existing_city.timezone = city_data.get('timezone')
                updated_cities += 1
            else:
                # Create new city
                new_city = City(
                    name=city_data['name'],
                    country_id=country.id,
                    latitude=city_data.get('latitude'),
                    longitude=city_data.get('longitude'),
                    state=city_data.get('state'),
                    state_code=city_data.get('state_code'),
                    population=city_data.get('population'),
                    timezone=city_data.get('timezone')
                )
                self.db.add(new_city)
                added_cities += 1
        
        # Commit changes
        self.db.commit()
        
        return {
            "total_cities": total_cities,
            "added_cities": added_cities,
            "updated_cities": updated_cities
        } 