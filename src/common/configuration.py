from starlette.config import Config

# Load environment variables from .env file
config = Config(".env")

# Retrieve environment variables
SECRET_KEY = config(
    "SECRET_KEY",
    default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
)
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_DAYS = config(
    "ACCESS_TOKEN_EXPIRE_DAYS", cast=int, default=7
)
DATABASE_URI = config(
    "DATABASE_URI", default="postgresql://shrey:Sonu619@localhost:5432/Ecommerce"
)
