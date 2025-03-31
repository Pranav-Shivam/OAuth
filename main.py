import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.databases import init_db
from app.auth import router as auth_router
from procurement.procurement import procurement_router
from fastapi.middleware.cors import CORSMiddleware



# Define the lifespan context manager for startup and shutdown events.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database (and other resources if needed)
    init_db()
    # Optionally, print or log startup events.
    print("Database initialized and resources loaded.")
    
    # Yield control to let the app run.
    yield
    
    # Shutdown: Clean up resources (if needed)
    print("Application shutting down. Resources cleaned up.")

# Pass the lifespan context manager to FastAPI.
app = FastAPI(title="OAuth2 Authentication with PostgreSQL", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes.
app.include_router(auth_router)
app.include_router(procurement_router, tags=["procurement"])


@app.get("/")
async def root():
    return {"message": "Authentication API is running!"}

# Entry point to run the application using `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
