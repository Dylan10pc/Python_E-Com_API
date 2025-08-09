Created using Python 3.13.4.

# How to run:

1. Clone the repo

2. Please create a virtual environment with **Python 3.13.4**

3. Gather all libraries and dependencies by running: **pip install -r requirements.txt**

4. Run **main.py** to create the database.

5. If you'd like to create a dummy CSV please run **suade_generic_test.py**

# Running The Server:

1. To run the server, please add this to your Python terminal **uvicorn main:app --reload**

2. You will receive a URL. Please run it and then add **/docs** at the end of the URL. 

3. You'll see something that looks like this:

<img width="1893" height="992" alt="image" src="https://github.com/user-attachments/assets/6c21b996-e16e-4c3e-96f4-cdf441ccaf0f" />

4. Press **try it out** and next to the file, please click on **choose file** and upload your file, then finally please press **execute**. Let the file be read and added to the database. The bigger the file, the longer it will take. While running tests, it took about 8 minutes to run a size of 1mil transactions

5. After it is done loading. You should be able to receive a summary. To receive a summary, you must scroll down to where it says **GET** to the right, please press **try it out**. Add the user_id and a start and end date. Then press **execute**, assuming your CSV file was successful you should be able to get a summary of the users' transactions.

# Running Tests

**Info:**
These Unit tests were tested on each part of the API end points. They all have their separate files for a clean Code. These were tested to make sure that they met all the requirements.

1. To run tests all at the same time, please do **pytest** in the Python terminal

2. After it has run, you should see which tests have failed. Although all my tests passed and had all their expected outcomes.

# Approach:

This project was done with careful planning. At first, I was going to run this project without a persistent storage system. I realised it would be impractical if we want to make sure it runs a file with a 1mil transactions.
I ultimately decided to use SQLAlchemy to make a SQLite database, as it would be able to hold 1mil transactions. 

As for the files, I needed a model for my database table that would be able to store all the data in the correct columns. Which is why I created a model.py

I also wanted to structure the summary output that the API endpoint would provide. To give a readable output. I did this by creating a model in summaryresponse.py

I also needed to create a file that would be able to calculate the min, max, and average of a user in a specified time range. This file would query the database and filter the transactions to get the info from the users' transactions for a specified time range, and then calculate the min, max, and avg.
This would return the summary. 

The database was created in a separate file to create a SQLite database, so it could hold all the contents provided.

The test folder was created to hold all the test files in one place. The tests were there to see if all thought-out errors were correctly managed.

The main.py held the rest of the API endpoints, such as **POST** and **GET**. These were split into two methods. The post method I included several checks for errors to make sure that all errors were given details in case an error arose.
The post method would read the CSV file and decode it so that pandas could read it and create a pandas dataframe. This would ensure the file could be read. Before proceeding, I check if all columns are provided to not cause any errors with a specific check for the timestamp column. This is due to making sure the format of the date is correct.
The data is then prepared to be saved in the database. I added a feature that would overwrite any old data in the database with the new data from a different file, as it was causing errors beforehand. This is done by using the transaction_id to identify the conflicts; those with the same ID were updated.

The summary method had several error checks before the data was sent. The method used the response model from the summaryresponse.py. The summary method in the main method calls the summary.py method to calculate and retrieve the summary.

# Improvements: 

Although the project works as intended. There were still several flaws that I think could have been changed, such as making the main.py neater. I could have added several methods for different functions to simplify the main methods.
The main method could have had more detailed logging and error handling.
The test files could have been more thorough with more tests on different sections, such as looking to see if more numbers were added into the dates when retrieving the summary or seeing of it could handle multiple files at once.
