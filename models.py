"""
This file defines the table named 'transactions' in the database.
It uses SQLAlchemy to define the structure of the table using columns and their data types.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import base

# This is the model for the transactions table
# This table will store transaction data including transaction ID, user ID, product ID, timestamp, and transaction amount.
class Transaction(base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer)
    timestamp = Column(DateTime, index=True)
    transaction_amount = Column(Float)
