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
import logging
from schemas.city import CityCreate, CityUpdate, CityResponse, CitySearchParams, CitySearchResponse, StateSearchResponse, StateResponse

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
        logger = logging.getLogger(__name__)
        logger.info("Starting city initialization process")
        
        # Get the path to the cities.csv file
        base_path = Path(__file__).parent.parent.parent
        cities_file = base_path / "dump" / "cities.csv"
        logger.info(f"Looking for cities data file at: {cities_file}")
        
        if not cities_file.exists():
            logger.error(f"Cities data file not found at {cities_file}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cities data file not found"
            )
        
        # Read CSV file using pandas
        try:
            logger.info("Reading cities data from CSV file...")
            df = pd.read_csv(cities_file)
            logger.info(f"Successfully loaded CSV file with {len(df)} rows")
        except Exception as e:
            logger.error(f"Failed to read cities file: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading cities file: {str(e)}"
            )
        
        total_cities = len(df)
        added_cities = 0
        updated_cities = 0
        skipped_cities = 0
        error_cities = 0
        batch_size = 100
        
        logger.info(f"Found {total_cities} cities in the CSV file")
        
        # Process cities in batches
        for batch_start in range(0, total_cities, batch_size):
            batch_end = min(batch_start + batch_size, total_cities)
            logger.info(f"Processing batch {batch_start//batch_size + 1} (cities {batch_start+1} to {batch_end})")
            
            try:
                # Process each city in the batch
                for _, row in df.iloc[batch_start:batch_end].iterrows():
                    try:
                        city_name = str(row[1])
                        country_id = int(row[5])
                        city_id = int(row[0])
                        logger.debug(f"Processing city: {city_name} (Country ID: {country_id}, City ID: {city_id})")
                        
                        # Get country by ID
                        country = self.db.query(Country).filter(
                            Country.country_id == country_id
                        ).first()
                        
                        if not country:
                            skipped_cities += 1
                            logger.warning(f"Skipping city {city_name}: Country with ID {country_id} not found")
                            continue  # Skip if country doesn't exist
                        
                        # Parse coordinates
                        latitude = self._parse_coordinates(row[8])
                        longitude = self._parse_coordinates(row[9])
                        
                        # Check if city already exists by city_id and country_id (composite key)
                        existing_city = self.db.query(City).filter(
                            City.city_id == city_id,
                            City.country_id == country_id
                        ).first()
                        
                        if existing_city:
                            # Update existing city
                            logger.info(f"Updating existing city: {existing_city.name}")
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
                            logger.debug(f"Successfully updated city: {existing_city.name}")
                        else:
                            # Create new city
                            logger.info(f"Creating new city: {str(row[1])}")
                            new_city = City(
                                city_id=city_id,
                                name=str(row[1]),
                                state_id=str(row[2]) if pd.notna(row[2]) else None,
                                state_code=str(row[3]) if pd.notna(row[3]) else None,
                                state_name=str(row[4]) if pd.notna(row[4]) else None,
                                country_id=country.id,
                                country_code=str(row[6]),
                                country_name=str(row[7]),
                                latitude=latitude,
                                longitude=longitude,
                                wikiDataId=str(row[10]) if pd.notna(row[10]) else None
                            )
                            self.db.add(new_city)
                            added_cities += 1
                            logger.debug(f"Successfully created new city: {new_city.name}")
                    except Exception as e:
                        error_cities += 1
                        logger.error(f"Error processing city {row[1]}: {str(e)}", exc_info=True)
                        continue
                
                # Commit changes for this batch
                logger.info(f"Committing changes for batch {batch_start//batch_size + 1}...")
                self.db.commit()
                logger.info(f"Successfully committed batch {batch_start//batch_size + 1}")
                
            except Exception as e:
                logger.error(f"Failed to process batch {batch_start//batch_size + 1}", exc_info=True)
                self.db.rollback()
                error_cities += (batch_end - batch_start)
                continue
        
        # Prepare and log final statistics
        stats = {
            "total_cities": total_cities,
            "added_cities": added_cities,
            "updated_cities": updated_cities,
            "skipped_cities": skipped_cities,
            "error_cities": error_cities
        }
        
        logger.info(
            "City initialization completed with statistics:\n"
            f"Total cities processed: {total_cities}\n"
            f"Cities added: {added_cities}\n"
            f"Cities updated: {updated_cities}\n"
            f"Cities skipped: {skipped_cities}\n"
            f"Cities with errors: {error_cities}"
        )
        
        return stats

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


    def search_cities(self, params: CitySearchParams) -> CitySearchResponse:
        """
        Search for cities with various filters and pagination.
        
        Args:
            params (CitySearchParams): Search parameters including name, country_id, state_id, etc.
            
        Returns:
            CitySearchResponse: Search results with pagination info
        """
        query = self.db.query(City)
        
        # Apply filters
        if params.name:
            query = query.filter(func.lower(City.name).like(f"%{params.name.lower()}%"))
        if params.country_id:
            query = query.filter(City.country_id == params.country_id)
        if params.state_id:
            query = query.filter(City.state_id == params.state_id)
        if params.state_code:
            query = query.filter(City.state_code == params.state_code.upper())
        if params.state_name:
            query = query.filter(func.lower(City.state_name).like(f"%{params.state_name}%"))
        if params.country_code:
            query = query.filter(City.country_code == params.country_code.upper())
        if params.wikiDataId:
            query = query.filter(City.wikiDataId == params.wikiDataId)
        
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

    def search_states_by_country(self, country_id: int) -> StateSearchResponse:
        """
        Search for states in a country, grouped by state_name.
        
        Args:
            country_id (int): Country ID to filter by
            
        Returns:
            StateSearchResponse: List of unique states in the country
        """
        # Query to get unique states for the country
        query = self.db.query(
            City.state_id,
            City.state_name,
            City.state_code,
            City.country_id,
            City.country_code,
            City.country_name
        ).filter(
            City.country_id == country_id
        ).distinct(
            City.state_id
        ).order_by(
            City.state_name
        )
        
        # Execute query
        states = query.all()
        
        return StateSearchResponse(
            message="States found successfully",
            status="success",
            data=[StateResponse(
                state_id=state.state_id,
                state_name=state.state_name,
                state_code=state.state_code,
                country_id=state.country_id,
                country_code=state.country_code,
                country_name=state.country_name
            ) for state in states],
            total=len(states)
        ) 