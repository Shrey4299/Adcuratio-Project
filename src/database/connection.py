from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.common.configuration import DATABASE_URI
from src.database.schema import Base

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
