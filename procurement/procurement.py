# /api/procurement.py
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import get_current_user  # JWT authentication
from app.databases import get_db
from app.models import User
from pathlib import Path

procurement_router = APIRouter(prefix="/api")

# OAuth2 bearer scheme for security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Path to the JSON file
DATA_FILE = Path("procurement/dummy.json")

def load_data(file_path: Path) -> list:

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@procurement_router.get("/procurement", response_model=list)
async def get_procurement_data(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    try:
        data = load_data(DATA_FILE)
        return data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading procurement data: {str(e)}"
        )
