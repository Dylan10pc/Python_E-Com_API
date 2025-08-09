"""
This is a test file for the FastAPI application.
It tests the file upload functionality, ensuring that the uploaded CSV file is valid,
contains the required columns, and handles various error cases.
"""
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pathlib import Path
from main import app
import io

# This sets up a test client for the FastAPI application
client = TestClient(app)

# This test checks if the file upload endpoint works correctly
# Expected: HTTP 200 status code and a success message
def test_upload_file():
    # Create a dummy CSV file in memory
    csv_content = io.StringIO("transaction_id,user_id,product_id,timestamp,transaction_amount\n"
                               "1,100,200,2023-01-01 12:00:00,50.0\n"
                               "2,101,201,2023-01-02 13:00:00,75.0\n")
    file_path = Path("test_upload.csv")
    file_path.write_text(csv_content.getvalue())
    
    # Send a POST request to the upload endpoint
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": ("test_upload.csv", file, "text/csv")})
        
    # Check if the response status code is 200 and the message is as expected
    assert response.status_code == 200
    assert response.json() == {"message": "Data saved succesfully."}

# This test checks if the uploaded file is a valid CSV file
# Expected: HTTP 400 status code and an error message
def test_upload_invalid_file():
    wrongfile = client.post("/upload/", files={"file": ("test_upload.txt", io.BytesIO(b"Invalid content"), "text/plain")})
    assert wrongfile.status_code == 400
    assert wrongfile.json() == {"detail": "Please upload a CSV file."}

# This test checks if the uploaded CSV file is empty
# Expected: HTTP 400 status code and an error message
def test_upload_empty_file():
    emptyfile = client.post("/upload/", files={"file": ("empty.csv", io.BytesIO(b""), "text/csv")})
    assert emptyfile.status_code == 400
    assert emptyfile.json() == {"detail": "Uploaded CSV file is empty."}


# This test checks if the CSV file is missing required columns
# Expected: HTTP 400 status code and an error message('Product_id' is missing)
def test_upload_missing_columns():
    missingcolumns = io.StringIO("transaction_id,user_id,timestamp,transaction_amount\n"
                               "1,100,2023-01-01 12:00:00,50.0\n")
    file_path = Path("test_missing_columns.csv")
    file_path.write_text(missingcolumns.getvalue())
    
    # Send a POST request to the upload endpoint
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": ("test_missing_columns.csv", file, "text/csv")})
        
    # Check if the response status code is 400 and the message is as expected
    assert response.status_code == 400
    assert response.json() == {"detail": "CSV file is missing required columns: ['product_id']"}

# This test checks if the timestamp is in the correct format
# Expected: HTTP 400 status code and an error message
def test_upload_invalid_timestamp():
    wrong_timestamp = io.StringIO("transaction_id,user_id,product_id,timestamp,transaction_amount\n"
                               "1,100,200,invalid_timestamp,50.0\n")
    file_path = Path("test_invalid_timestamp.csv")
    file_path.write_text(wrong_timestamp.getvalue())
    
    # Send a POST request to the upload endpoint
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": ("test_invalid_timestamp.csv", file, "text/csv")})
        
    # Check if the response status code is 400 and the message is as expected
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid Timestamp. Use YYYY-MM-DD"}

# This test checks if the user_id is an integer
# Expected: HTTP 400 status code and an error message
def test_upload_non_integer_User_id():
    non_integer_user_id = io.StringIO("transaction_id,user_id,product_id,timestamp,transaction_amount\n"
                               "1,non_integer,200,2023-01-01 12:00:00,50.0\n")
    file_path = Path("test_non_integer_user_id.csv")
    file_path.write_text(non_integer_user_id.getvalue())
    
    # Send a POST request to the upload endpoint
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": ("test_non_integer_user_id.csv", file, "text/csv")})
    # Check if the response status code is 400 and the message is as expected
    assert response.status_code == 400
    assert response.json() == {"detail": "user_id must be integers."}

# This test checks if the product_id is an integer  
# Expected: HTTP 400 status code and an error message  
def test_upload_non_integer_product_id():
    non_integer_product_id = io.StringIO("transaction_id,user_id,product_id,timestamp,transaction_amount\n"
                               "1,100,non_integer,2023-01-01 12:00:00,50.0\n")
    file_path = Path("test_non_integer_product_id.csv")
    file_path.write_text(non_integer_product_id.getvalue())
    
    # Send a POST request to the upload endpoint
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": ("test_non_integer_product_id.csv", file, "text/csv")})
    # Check if the response status code is 400 and the message is as expected
    assert response.status_code == 400
    assert response.json() == {"detail": "product_id must be integers."}
    
# This test checks the performance of uploading a large CSV file
# Expected: HTTP 200 status code
def test_performance_large_file():
    # Create a large CSV file in memory
    # We also write the CSV headers with the required columns
    large_file_content = io.StringIO()
    large_file_content.write("transaction_id,user_id,product_id,timestamp,transaction_amount\n")
    
    # Generate 1,000,000 rows of dummy data
    # This simulates a large file upload scenario
    for i in range(1000000):
        large_file_content.write(f"{i},1000,2000,2023-01-01 12:00:00,{i % 100}\n")
    
    # Reset the StringIO object to the beginning 
    # This is necessary to read the content from the start
    large_file_content.seek(0)
    
    # Write the content to a file
    # This is to simulate a real file upload scenario
    large_file_path = Path("large_test_upload.csv")
    
    # Write the CSV contnent to the file using UTF-8 encoding
    with open(large_file_path, "w", encoding="utf-8") as f:
        f.write(large_file_content.getvalue())
    
    # Send a POST request to the upload endpoint with the large file   
    with open(large_file_path, "rb") as f:
        response = client.post("/upload/", files={"file": ("large_test.csv", f, "text/csv")})

    # Check if the response status code is 200
    assert response.status_code == 200
    

    
    
    