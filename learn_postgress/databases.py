from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text

URL_DATABASE = "postgresql://postgres:root@localhost:5432/Auth"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db_router = APIRouter(prefix="/db")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@db_router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Checks if the database is reachable.
    """
    try:
        # Use text() to explicitly declare the SQL string
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
