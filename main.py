import time

from decouple import config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from src.database.schema import Base
from src.endpoints.user.user_endpoints import user_router
from src.common.config import DATABASE_URI

app = FastAPI(title="User Project")

# Retrieve database URI from environment variable or use a default value
# DATABASE_URI = config(
#     "DATABASE_URI", default="postgresql://shrey:Sonu619@localhost:5432/Ecommerce"
# )

# Middleware for FastAPI to handle database sessions
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URI)


# Middleware for logging requests
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Middleware for FastAPI to handle CORS
origins = [
    # "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the router from your endpoint file
app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
