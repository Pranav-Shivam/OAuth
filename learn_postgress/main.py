from fastapi import FastAPI
from databases import db_router
import uvicorn
app = FastAPI()

app.include_router(db_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)