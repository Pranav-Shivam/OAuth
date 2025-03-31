# /api/procurement.py
import json
from functools import lru_cache
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.auth import get_current_active_user  
from app.databases import get_db
from app.models import User
from pathlib import Path

procurement_router = APIRouter(prefix="/api")

# Path to the JSON file
DATA_FILE = Path("procurement/dummy.json")

@lru_cache(maxsize=1)
def load_data(file_path: Path = DATA_FILE) -> List[Dict[str, Any]]:
    """Load procurement data from JSON file with caching"""
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Procurement data file not found"
        )
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Invalid JSON format in procurement data"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to load procurement data: {str(e)}"
        )

@procurement_router.get(
    "/procurement", 
    response_model=List[Dict[str, Any]],
    summary="Get procurement data",
    response_description="List of procurement records"
)
async def get_procurement_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: Optional[int] = Query(None, ge=1, description="Limit the number of results"),
    offset: int = Query(0, ge=0, description="Skip the first N results"),
    search: Optional[str] = Query(None, description="Search term in procurement data")
):
    try:
        data = load_data()
        
        # Apply filtering if search parameter is provided
        if search:
            search = search.lower()
            filtered_data = [
                item for item in data 
                if any(search in str(value).lower() for value in item.values())
            ]
            data = filtered_data
            
        # Apply pagination
        if offset > 0:
            data = data[offset:]
        if limit:
            data = data[:limit]
            
        return data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing procurement data: {str(e)}"
        )