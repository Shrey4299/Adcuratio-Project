from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.schema import Base
from src.common.config import DATABASE_URI



engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
