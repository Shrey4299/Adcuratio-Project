from typing import Annotated, Optional
from fastapi import FastAPI, Header
from fastapi_sqlalchemy import DBSessionMiddleware
from src.database.schema import Base
from src.endpoints.user.user_endpoints import user_router
from decouple import config

app = FastAPI()

# Retrieve database URI from environment variable or use a default value
DATABASE_URI = config(
    "DATABASE_URI", default="postgresql://shrey:Sonu619@localhost:5432/Ecommerce"
)

# Middleware for FastAPI to handle database sessions
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URI)


# Include the router from your endpoint file
app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
