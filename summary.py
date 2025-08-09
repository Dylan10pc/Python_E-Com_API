"""
This file contains the logic to generate a summary of transaction data for a user.
It queries the database for the min, max, and average transaction amounts
within a specified date range and returns the results in a structured format.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models import Transaction

# This function queries the database to get summary statistics for a user's transactions6
# It calculates the minimum, maximum, and average transaction amounts within a specified date range.
def get_CSV_summary(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    
    result = db.query(
        func.min(Transaction.transaction_amount).label("min_transaction_amount"),
        func.max(Transaction.transaction_amount).label("max_transaction_amount"),
        func.avg(Transaction.transaction_amount).label("average_transaction_amount"),
        
    # Filters transactions by user_id and within the specified date range
    ).filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= start_date,
        Transaction.timestamp <= end_date
    ).first()
    
    # Returns the summary statistics
    # If no transactions are found, default values are returned
    return{
        "user_id": user_id,
        "min_transaction_amount": result.min_transaction_amount or 0,
        "max_transaction_amount": result.max_transaction_amount or 0,
        "average_transaction_amount": result.average_transaction_amount or 0
    }