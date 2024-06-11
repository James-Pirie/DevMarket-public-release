from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# establishes the connection to the database

connection_url = "mssql+pyodbc://DB_ID:DB_PASSWORD@DB_IP/DB_NAME?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_url, echo=True)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
