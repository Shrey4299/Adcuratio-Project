from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password = Column(String)


class WebScraper(Base):
    __tablename__ = "webscraps"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    image = Column(String)
    titles = Column(String)
    url = Column(String)

    generalised_descriptions = relationship(
        "GeneralisedDescription", back_populates="web_scraper"
    )


class GeneralisedDescription(Base):
    __tablename__ = "generalised_descriptions"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    web_scraper_id = Column(Integer, ForeignKey("webscraps.id"))

    web_scraper = relationship("WebScraper", back_populates="generalised_descriptions")
    word_counts = relationship(
        "GeneralisedWordCount",
        back_populates="generalised_description",
        cascade="all, delete-orphan",  # Add cascade option if necessary
    )

    def __repr__(self):
        return f"<GeneralisedDescription(id={self.id}, description={self.description})>"


class GeneralisedWordCount(Base):
    __tablename__ = "generalised_word_counts"

    id = Column(Integer, primary_key=True)
    word_count_desc = Column(String)
    generalised_description_id = Column(
        Integer, ForeignKey("generalised_descriptions.id")
    )

    generalised_description = relationship(
        "GeneralisedDescription", back_populates="word_counts"
    )

    def __repr__(self):
        return f"<GeneralisedWordCount(id={self.id}, word_count_desc={self.word_count_desc})>"
