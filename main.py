"""
Provides endpoints for uploading transaction data from CSV files and retrieving summary statistics.
The summary statistics include minimum, maximum, and average transaction amounts for a user within a specified date range.
It uses FastAPI for the web framework, SQLAlchemy for database interactions, and Pydantic for data validation.
"""
from fastapi import FastAPI, HTTPException, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.dialects.sqlite import insert
import pandas as pd
import io
import logging
import models
import summary
import database
import summaryresponse

# This sets up logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.base.metadata.create_all(bind=database.dbengine)

app = FastAPI(title="Transaction Summary API")

# Creates a databse session for each request
def get_database():
    db = database.session()
    
    try:
        yield db
        # This ensures that the database session is closed after the request is completed
    finally:
        db.close()

"""
This function handles the file upload endpoint.
It checks if the uploaded file is a CSV file, reads its content, and validates the required columns.
If valid, it saves the data to the database, handling any conflicts by updating existing records.
Any data in the database gets replaced with the new data from the CSV file.
"""        
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_database)
    ):
    
    # Check if the uploaded file is a CSV file
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
    
    # Read the CSV file content
    # If the file is empty, it raises an HTTPException
    csv_content = await file.read()
    csv_read_content = csv_content.decode()
    
    if not csv_read_content.strip():
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")
    
    # It uses pandas to read the CSV file and checks for required columns
    # If the CSV file is empty, it raises an HTTPException
    try:
        reader = pd.read_csv(io.StringIO(csv_read_content))
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    # Check if the CSV file is empty
    if reader.empty:
        raise HTTPException(status_code=400, detail="CSV file is empty.")
    
    # Check if the CSV file contains the required columns
    # The required columns are transaction_id, user_id, product_id, timestamp, and transaction_amount
    required_columns = {'transaction_id', 'user_id', 'product_id', 'timestamp', 'transaction_amount'}
    missing_columns = required_columns - set(reader.columns)
    if missing_columns:
        raise HTTPException(
            status_code=400, detail=f"CSV file is missing required columns: {sorted(missing_columns)}"
    )
    
    # If the timestamp column is not present or cannot be converted, it raises an HTTPException
    # Convert the timestamp column to datetime format
    # The expected format is YYYY-MM-DD HH:MM:SS if not a HTTPException is raised
    if 'timestamp' not in reader.columns:
        raise HTTPException(status_code=400, detail="CSV file must contain a 'timestamp' column.")
    try:
        reader["timestamp"] = pd.to_datetime(reader["timestamp"])
    except Exception as e:
        logger.error(f"Error converting timestamp: {e}")
        raise HTTPException(status_code=400, detail="Invalid Timestamp. Use YYYY-MM-DD")
    
    # The data is prepared for saving to the database 
    # It creates a list of Transaction objects from the CSV data
    # It loops through each row in the DataFrame
    save_data = [models.Transaction(
        transaction_id=row['transaction_id'],
        user_id=row['user_id'],
        product_id=row['product_id'],
        timestamp=row['timestamp'],
        transaction_amount=row['transaction_amount']
    ) for index, row in reader.iterrows()] 
    
    # A loop to insert or update each transaction in the database
    for obj in save_data:
        
        # Validates the product_id, and user_id making sure they are integers
        if not isinstance(obj.product_id, int):
            raise HTTPException(status_code=400, detail="product_id must be integers.")
        if not isinstance(obj.user_id, int):
            raise HTTPException(status_code=400, detail="user_id must be integers.")
        
        # Creates an insert statement for the Transaction model
        # This is for inserting or updating the transaction data in the database
        replace = insert(models.Transaction).values(
            transaction_id=obj.transaction_id,
            user_id=obj.user_id,
            product_id=obj.product_id,
            timestamp=obj.timestamp,
            transaction_amount=obj.transaction_amount
        )
        
        # If a transaction with the same transaction_id already exists, it updates the existing record
        # It uses transaction_id as the unique identifier for conflicts
        # Fields user_id, product_id, timestamp, and transaction_amount are updated
        replace = replace.on_conflict_do_update(
            index_elements=['transaction_id'],
            set_={
                'user_id': obj.user_id,
                'product_id': obj.product_id,
                'timestamp': obj.timestamp,
                'transaction_amount': obj.transaction_amount
            }
        )
    
    # Executes the insert statement and commits the changes to the database
        db.execute(replace)
        # Commits the changes to the database
    db.commit()
    
    # Logs the successful data saving
    logger.info("Data saved successfully.")
    logger.info(f"Number of records saved: {len(save_data)}")
    
    # Returns a success message
    return {"message": "Data saved succesfully."}

"""
This function handles the summary statistics endpoint.
It retrieves the minimum, maximum, and average transaction amounts for a user within a specified date range.
The user_id, start_date, and end_date are provided as query parameters.
"""
@app.get("/summary/{user_id}", response_model=summaryresponse.summaryResponse)
def get_CSV_summary(
    user_id: int,
    start_date: datetime = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_database)
):
    # Validates the user_id, start_date, and end_date
    if not start_date:
        raise HTTPException(status_code=400, detail="Start date is required.")
    if not end_date:
        raise HTTPException(status_code=400, detail="End date is required.")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date.")
    if not isinstance(user_id, int):
        raise HTTPException(status_code=400, detail="user_id must be an integer.")
    
    # Calls the get_CSV_summary function to retrieve the summary statistics
    summary_data = summary.get_CSV_summary(db, user_id, start_date, end_date)
    return summary_data

    