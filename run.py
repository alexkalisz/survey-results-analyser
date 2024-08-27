import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Survey Results Analyser')
survey = SHEET.worksheet('survey')

data = survey.get_all_values()

print(data)

def get_survey_data():
    """
    Get survey data input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of values separated
    by commas.
    """
    print("Please enter survey data.")
    print("Data should be in the format: value1,value2,value3,...,value10")
    print("Example: 5,Yes,23,Male\n")

    data_str = input("Enter your data here:\n")

    print(f"The data provided is: {data_str}")

def main():
    """
    Run all program functions.
    """
    get_survey_data()
    # Other functions will be added here later

print("Welcome to Survey Data Analysis")
main()