"""
This file contains tests for the summary endpoint of the FastAPI application.
It tests the functionality of the summary endpoint, ensuring that it correctly
returns transaction summaries for a user within a specified date range.
"""
from fastapi.testclient import TestClient
from main import app

# This sets up a test client for the FastAPI application
client = TestClient(app)

# This test checks if the user ID is an integer
# expected: HTTP 422 status code
def test_summary_user_id_integer():
    # It sends a GET request to the summary endpoint with a non-integer user_id
    response = client.get("/summary/non_integer", params={
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    })
    # It checks if the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    errors = response.json().get("detail", [])
    
    # Ensures that the error message shows that user_id must be an int
    assert any(
        err.get("loc", [])[0] == "path" and
        err.get("loc", [])[1] == "user_id" and
        "integer" in err.get("msg", "").lower()
        for err in errors
    )

# This test checks if the start date is before the end date
# expected: HTTP 400 status code And an error message    
def test_summary_date_range():
    # It sends a GET request to the summary endpoint with an end date before the start date
    response = client.get("/summary/1", params={
        "start_date": "2023-12-31",
        "end_date": "2023-01-01"
    })
    # It checks if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Start date must be before end date."}

# This test checks if the start date are provided
# expected: HTTP 422 status code and an error message    
def test_summary_missing_start_date():
    # It sends a GET request to the summary endpoint without the start_date parameter
    response = client.get("/summary/1", params={
        "end_date": "2023-12-31"
    })
    # It checks if the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "start_date"
    assert response.json()["detail"][0]["msg"] == "Field required"

# This test checks if the end date is provided
# expected: HTTP 422 status code and an error message
def test_summary_missing_end_date():
    # It sends a GET request to the summary endpoint without the end_date parameter
    response = client.get("/summary/1", params={
        "start_date": "2023-01-01"
    })
    # It checks if the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "end_date" 
    assert response.json()["detail"][0]["msg"] == "Field required"

# This test checks if the summary endpoint returns a valid response
# expected: HTTP 200 status code and a valid summary response
def test_summary_valid_request():
    # It sends a GET request to the summary endpoint with valid parameters
    response = client.get("/summary/1", params={
        "user_id": 1,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    })
    # It checks if the response status code is 200 (OK)
    assert response.status_code == 200