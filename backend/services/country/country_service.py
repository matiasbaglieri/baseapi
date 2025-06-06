from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.country import Country
from sqlalchemy import or_, func
from typing import List, Optional
import json
import os
from pathlib import Path

class CountryService:
    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, name: str) -> Country:
        """
        Find a country by its name.
        
        Args:
            name (str): Name of the country to find
            
        Returns:
            Country: The found country
            
        Raises:
            HTTPException: If country is not found
        """
        country = self.db.query(Country).filter(Country.name == name).first()
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country '{name}' not found"
            )
        return country

    def find_by_code(self, code: str) -> Country:
        """
        Find a country by its ISO code (ISO2 or ISO3).
        
        Args:
            code (str): ISO2 or ISO3 country code
            
        Returns:
            Country: The found country
            
        Raises:
            HTTPException: If country is not found
        """
        if len(code) not in [2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Country code must be either 2 or 3 characters"
            )

        country = self.db.query(Country).filter(
            or_(
                Country.iso2 == code.upper(),
                Country.iso3 == code.upper()
            )
        ).first()

        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country with code '{code}' not found"
            )
        return country

    def validate_country(self, country_name: str = None, country_code: str = None) -> Country:
        """
        Validate country by name or code.
        
        Args:
            country_name (str, optional): Name of the country
            country_code (str, optional): ISO2 or ISO3 country code
            
        Returns:
            Country: The found country
            
        Raises:
            HTTPException: If country is not found or validation fails
        """
        if not country_name and not country_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either country name or country code must be provided"
            )

        if country_code:
            return self.find_by_code(country_code)
        return self.find_by_name(country_name)

    def search_countries(
        self,
        name: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Country]:
        """
        Search for countries by name.
        
        Args:
            name (str, optional): Partial name to search for
            limit (int): Maximum number of results to return
            offset (int): Number of results to skip
            
        Returns:
            List[Country]: List of matching countries
        """
        query = self.db.query(Country)

        # Apply name filter if provided
        if name:
            query = query.filter(func.lower(Country.name).like(f"%{name.lower()}%"))
        
        # Add ordering
        query = query.order_by(Country.name)
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        return query.all()

    async def initialize_countries(self) -> dict:
        """
        Initialize countries in the database from a JSON file.
        
        Returns:
            dict: Statistics about the initialization process
        """
        # Get the path to the countries.json file
        base_path = Path(__file__).parent.parent.parent
        countries_file = base_path / "data" / "countries.json"
        
        if not countries_file.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Countries data file not found"
            )
        
        # Read and parse the JSON file
        with open(countries_file, 'r', encoding='utf-8') as f:
            countries_data = json.load(f)
        
        total_countries = len(countries_data)
        added_countries = 0
        updated_countries = 0
        
        # Process each country
        for country_data in countries_data:
            # Check if country already exists
            existing_country = self.db.query(Country).filter(
                or_(
                    Country.iso2 == country_data['iso2'],
                    Country.iso3 == country_data['iso3']
                )
            ).first()
            
            if existing_country:
                # Update existing country
                existing_country.name = country_data['name']
                existing_country.iso2 = country_data['iso2']
                existing_country.iso3 = country_data['iso3']
                existing_country.phone_code = country_data.get('phone_code')
                existing_country.currency = country_data.get('currency')
                existing_country.currency_symbol = country_data.get('currency_symbol')
                existing_country.region = country_data.get('region')
                existing_country.subregion = country_data.get('subregion')
                existing_country.latitude = country_data.get('latitude')
                existing_country.longitude = country_data.get('longitude')
                existing_country.emoji = country_data.get('emoji')
                updated_countries += 1
            else:
                # Create new country
                new_country = Country(
                    name=country_data['name'],
                    iso2=country_data['iso2'],
                    iso3=country_data['iso3'],
                    phone_code=country_data.get('phone_code'),
                    currency=country_data.get('currency'),
                    currency_symbol=country_data.get('currency_symbol'),
                    region=country_data.get('region'),
                    subregion=country_data.get('subregion'),
                    latitude=country_data.get('latitude'),
                    longitude=country_data.get('longitude'),
                    emoji=country_data.get('emoji')
                )
                self.db.add(new_country)
                added_countries += 1
        
        # Commit changes
        self.db.commit()
        
        return {
            "total_countries": total_countries,
            "added_countries": added_countries,
            "updated_countries": updated_countries
        } 