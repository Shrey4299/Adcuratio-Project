import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from src.common.configuration import DATABASE_URI
from src.endpoints.user.user_endpoints import user_router
from src.endpoints.user.user_extra import user_router_extra
from src.endpoints.webscrap.hackernews import hacker_news_router

app = FastAPI(title="User Project")


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
app.include_router(user_router_extra, prefix="/api")
app.include_router(hacker_news_router, prefix="/api")
