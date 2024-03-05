from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.schema import Base


DATABASE_URI = "postgresql://shrey:Sonu619@localhost:5432/Ecommerce"

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
