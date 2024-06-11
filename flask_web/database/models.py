from sqlalchemy import ForeignKey, Column, String, Integer, Date, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# defines the models to be used for queries, for query example visit datareader/SQLAlchemyAdapter.py
# Each class directly corresponds to a table, defined in database/schema.sql


class Listing(Base):
    __tablename__ = 'Listing'

    ListingID = Column(Integer, primary_key=True, unique=True, nullable=False)
    region = Column(String(100))
    suburb = Column(String(100))
    salary = Column(String(100))
    jobType = Column(String(100))
    company = Column(String(100))
    listingDate = Column(Date)
    isActive = Column(Boolean)

    languages = relationship('Language', secondary='ListingLanguage', back_populates='listings')
    frameworks = relationship('Framework', secondary='ListingFramework', back_populates='listings')


class Language(Base):
    __tablename__ = 'Language'

    LanguageID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    listings = relationship('Listing', secondary='ListingLanguage', back_populates='languages')


class ListingLanguage(Base):
    __tablename__ = 'ListingLanguage'

    LanguageID = Column(Integer, ForeignKey('Language.LanguageID'), primary_key=True, nullable=False)
    ListingID = Column(Integer, ForeignKey('Listing.ListingID'), primary_key=True, nullable=False)


class Framework(Base):
    __tablename__ = 'Framework'

    FrameworkID = Column(Integer, primary_key=True, unique=True, nullable=False)
    LanguageID = Column(Integer, ForeignKey('Language.LanguageID'), nullable=False)
    name = Column(String(100), nullable=False)

    listings = relationship('Listing', secondary='ListingFramework', back_populates='frameworks')


class ListingFramework(Base):
    __tablename__ = 'ListingFramework'

    FrameworkID = Column(Integer, ForeignKey('Framework.FrameworkID'), primary_key=True, nullable=False)
    ListingID = Column(Integer, ForeignKey('Listing.ListingID'), primary_key=True, nullable=False)