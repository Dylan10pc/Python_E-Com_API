"""
This file defines a Pydantic model for input validation.
"""
from pydantic import BaseModel

# Response Model for summary statistics 
class summaryResponse(BaseModel):
    user_id: int
    min_transaction_amount: float
    max_transaction_amount: float
    average_transaction_amount: float