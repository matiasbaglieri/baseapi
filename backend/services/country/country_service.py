from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.country import Country
from sqlalchemy import or_, func
from typing import List, Optional
import json
import os,re
from pathlib import Path
import pandas as pd
import ast
from schemas.country import CountrySearchParams, CountrySearchResponse, CountryResponse

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

    def search_countries(self, params: CountrySearchParams) -> CountrySearchResponse:
        """
        Search for countries with various filters and pagination.
        
        Args:
            params (CountrySearchParams): Search parameters including name, iso2, iso3, region, etc.
            
        Returns:
            CountrySearchResponse: Search results with pagination info
        """
        query = self.db.query(Country)
        
        # Apply filters
        if params.name:
            query = query.filter(func.lower(Country.name).like(f"%{params.name.lower()}%"))
        if params.iso2:
            query = query.filter(Country.iso2 == params.iso2.upper())
        if params.iso3:
            query = query.filter(Country.iso3 == params.iso3.upper())
        if params.region:
            query = query.filter(func.lower(Country.region).like(f"%{params.region.lower()}%"))
        if params.subregion:
            query = query.filter(func.lower(Country.subregion).like(f"%{params.subregion.lower()}%"))
        if params.currency:
            query = query.filter(func.lower(Country.currency).like(f"%{params.currency.lower()}%"))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        countries = query.order_by(Country.name).offset(params.offset).limit(params.limit).all()
        
        return CountrySearchResponse(
            message="Countries found successfully",
            status="success",
            data=[CountryResponse.from_orm(country) for country in countries],
            total=total
        )

    def _parse_timezones(self, timezones_str: str) -> Optional[List[dict]]:
        """Parse timezones string to JSON list."""
        if not timezones_str or timezones_str == '[]':
            return None
        try:
            # Convert string representation of list to actual list
            timezones_list = ast.literal_eval(timezones_str)
            return timezones_list
        except (ValueError, SyntaxError):
            return None

    def _parse_coordinates(self, value: str) -> Optional[float]:
        """Parse coordinate string to float."""
        if not value or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def initialize_countries(self) -> dict:
        """
        Initialize countries in the database from a CSV file using pandas.
        id,name,iso3,iso2,numeric_code,phonecode,capital,currency,currency_name,currency_symbol,tld,native,region,region_id,subregion,subregion_id,nationality,timezones,latitude,longitude,emoji,emojiU
        
        Returns:
            dict: Statistics about the initialization process
        """
        # Get the path to the countries.csv file
        base_path = Path(__file__).parent.parent.parent
        countries_file = base_path / "dump" / "countries.csv"
        
        if not countries_file.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Countries data file not found"
            )
        
        # Read CSV file using pandas
        try:
            df = pd.read_csv(countries_file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading countries file: {str(e)}"
            )
        
        total_countries = len(df)
        added_countries = 0
        updated_countries = 0
        error_countries = 0
        
        # Process each country
        for _, row in df.iterrows():
            try:
                # Check if country already exists
                existing_country = self.db.query(Country).filter(
                    Country.country_id == int(row[0])
                ).first()
                
                # Parse timezones
                timezones = self._parse_timezones(row[17])
                
                # Parse coordinates
                latitude = self._parse_coordinates(row[18])
                longitude = self._parse_coordinates(row[19])
                
                # Format phonecode: prepend '+' if not empty and doesn't start with it
                phonecode = str(row[5]) if pd.notna(row[5]) else None
                if phonecode and not phonecode.startswith('+'):
                    phonecode = f'+{phonecode}'
                
                # Format numeric_code: always 3 digits, zero-padded
                raw_numeric_code = row[4]
                numeric_code = None
                if pd.notna(raw_numeric_code):
                    try:
                        numeric_code = f"{int(raw_numeric_code):03d}"
                    except Exception:
                        numeric_code = str(raw_numeric_code)
                
                # Format iso2: strip whitespace and uppercase
                iso2 = str(row[3]).strip().upper() if pd.notna(row[3]) else None
                if iso2:
                    # Remove any non-alphabetic characters
                    iso2 = ''.join(c for c in iso2 if c.isalpha())
                    # Validate the ISO2 code
                    if not re.match(r'^[A-Z]{2}$', iso2):
                        print(f"WARNING: Country {row[1]} has invalid ISO2 code: '{iso2}'")
                        iso2 = None
                
                if existing_country:
                    # Update existing country with type validation
                    existing_country.country_id = int(row[0])
                    existing_country.name = str(row[1])
                    existing_country.iso3 = str(row[2])
                    existing_country.iso2 = iso2
                    existing_country.numeric_code = numeric_code
                    existing_country.phonecode = phonecode
                    existing_country.capital = str(row[6]) if pd.notna(row[6]) else None
                    existing_country.currency = str(row[7]) if pd.notna(row[7]) else None
                    existing_country.currency_name = str(row[8]) if pd.notna(row[8]) else None
                    existing_country.currency_symbol = str(row[9]) if pd.notna(row[9]) else None
                    existing_country.tld = str(row[10]) if pd.notna(row[10]) else None
                    existing_country.native = str(row[11]) if pd.notna(row[11]) else None
                    existing_country.region = str(row[12]) if pd.notna(row[12]) else None
                    existing_country.subregion = str(row[14]) if pd.notna(row[14]) else None
                    existing_country.nationality = str(row[16]) if pd.notna(row[16]) else None
                    existing_country.timezones = timezones
                    existing_country.latitude = latitude
                    existing_country.longitude = longitude
                    existing_country.emoji = str(row[20]) if pd.notna(row[20]) else None
                    existing_country.emojiU = str(row[21]) if pd.notna(row[21]) else None
                    updated_countries += 1
                else:
                    # Create new country with type validation
                    new_country = Country(
                        country_id=int(row[0]),
                        name=str(row[1]),
                        iso3=str(row[2]),
                        iso2=iso2,
                        numeric_code=numeric_code,
                        phonecode=phonecode,
                        capital=str(row[6]) if pd.notna(row[6]) else None,
                        currency=str(row[7]) if pd.notna(row[7]) else None,
                        currency_name=str(row[8]) if pd.notna(row[8]) else None,
                        currency_symbol=str(row[9]) if pd.notna(row[9]) else None,
                        tld=str(row[10]) if pd.notna(row[10]) else None,
                        native=str(row[11]) if pd.notna(row[11]) else None,
                        region=str(row[12]) if pd.notna(row[12]) else None,
                        subregion=str(row[14]) if pd.notna(row[14]) else None,
                        nationality=str(row[16]) if pd.notna(row[16]) else None,
                        timezones=timezones,
                        latitude=latitude,
                        longitude=longitude,
                        emoji=str(row[20]) if pd.notna(row[20]) else None,
                        emojiU=str(row[21]) if pd.notna(row[21]) else None
                    )
                    self.db.add(new_country)
                    added_countries += 1
            except Exception as e:
                error_countries += 1
                print(f"Error processing country {row[1]}: {str(e)}")
                continue
        
        # Commit changes
        self.db.commit()
        
        return {
            "total_countries": total_countries,
            "added_countries": added_countries,
            "updated_countries": updated_countries,
            "error_countries": error_countries
        } 