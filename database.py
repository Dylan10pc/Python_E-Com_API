"""
This File sets up the database engine and session management.
It uses SQLAlchemy to create a session and manage the database interactions.
It connects to a SQLite database named 'transactions.db'.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is the database URL for SQLite
DATABASE_URL = "sqlite:///./transactions.db" 

# Create the database engine using the database URL and set check_same_thread to False for SQLite
dbengine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# This is used to create a database session for each request
session = sessionmaker(autocommit=False, autoflush=False, bind=dbengine)

# This is a base class to create database models
base = declarative_base()

