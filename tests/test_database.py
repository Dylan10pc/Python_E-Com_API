"""
Thi file contains the test cases for the database summary functionality.
It tests the logic to generate a summary of transaction data for a user,
ensuring that it correctly queries the database and returns the expected results.
"""
from database import session
from models import Transaction
from summary import get_CSV_summary
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.testclient import TestClient
from main import app

# This sets up a test client for the FastAPI application
client = TestClient(app)

# This test checks if the summary function returns the correct summary statistics
# expected: HTTP 200 status code
def test_get_user_summary():
    # Checks the endpoint responds with a 200 status code
    db = session()
    user_id = 1
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    # Sends a GET request to the summary endpoint
    response = client.get(f"/summary/{user_id}", params={
        "start_date": start_date,
        "end_date": end_date
    })
    
    # Checks if the response status code is 200
    assert response.status_code == 200
    db.close()

# This test checks if the summary function handles invalid user IDs  
# expected: HTTP 422 status code   
def test_get_user_summary_invalid_user():
    # Checks the endpoint responds with a 422 status code for invalid user ID
    db = session()
    user_id = "invalid"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    # Sends a GET request to the summary endpoint
    response = client.get(f"/summary/{user_id}", params={
        "start_date": start_date,
        "end_date": end_date
    })
    
    # Checks if the response status code is 422
    assert response.status_code == 422
    db.close()
