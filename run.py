import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import csv

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Survey Results Analyser')



def get_survey_data():
    """
    Get survey data input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of values separated
    by commas.
    """
    while True:
        print("Please enter survey data.")
        print("Data should be in the format: value1,value2,value3,...,value10")
        print("Example: 01/08/2024,Female,45,4,Yes,Price,Reasonably priced for what it offers.\n")

        data_str = input("Enter your data here:\n")

        f = StringIO(data_str)
        reader = csv.reader(f, skipinitialspace=True)
        survey_data = next(reader)

       
        print(f"Survey data split into list: {survey_data}")
        
        if validate_data(survey_data):
            print("Data is valid!")
            break 

    return survey_data

def validate_data(values):
    try:
        if len(values) != 7:
            raise ValueError(
                f"Exactly 7 values required, you provided {len(values)}"
            )
        
        int(values[3])

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def process_survey_data(data):
    return [
        data[0],  # Timestamp (string)
        data[1],  # Gender (string)
        data[2],  # Age Group (string)
        int(data[3]),  # Satisfaction (integer)
        data[4],  # Recommend (string)
        data[5],  # Favorite Feature (string)
        data[6]   # Comments (string)
    ]

def update_survey_worksheet(data):
    """
    Updates the survey worksheet with a new row of data.
    """
    print("Updating survey worksheet...\n")
    survey_worksheet = SHEET.worksheet("survey") 
    survey_worksheet.append_row(data)
    print("Survey worksheet updated successfully.\n")


def main():
    """
    Run all program functions.
    """
    data = get_survey_data()
    processed_data = process_survey_data(data)
    update_survey_worksheet(processed_data)

print("Welcome to Survey Data Analysis")
main()