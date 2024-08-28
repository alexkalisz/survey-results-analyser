import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import csv
from pprint import pprint

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

def fetch_latest_survey_data():
    """
    Fetches the latest survey data entry for analysis.
    """
    print("Fetching latest survey data...\n")
    survey_worksheet = SHEET.worksheet("survey")
    all_survey_data = survey_worksheet.get_all_values()
    pprint(all_survey_data)
    latest_survey_data = all_survey_data[-1]
    print(f"Latest survey data: {latest_survey_data}")
    return latest_survey_data

def calculate_average_satisfaction():
    """
    Calculate the average satisfaction score from the survey data.
    """
    print("Calculating average satisfaction...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()
    
    satisfaction_scores = [int(row[3]) for row in survey_worksheet[1:]]  # Skip the header row
    average_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
    
    print(f"Average satisfaction score: {average_satisfaction:.2f}")
    return average_satisfaction

def calculate_satisfaction_trend():
    """
    Compare the latest satisfaction score with the previous score
    and identify if there's an upward or downward trend.
    """
    print("Calculating satisfaction trend...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()
    
    latest_score = int(survey_worksheet[-1][3])
    previous_score = int(survey_worksheet[-2][3])
    
    trend = latest_score - previous_score
    
    if trend > 0:
        print(f"Satisfaction is improving by {trend} points.")
    elif trend < 0:
        print(f"Satisfaction is declining by {abs(trend)} points.")
    else:
        print("Satisfaction is stable.")

    return trend

def main():
    print("Welcome to Survey Data Analysis")
    survey_data = get_survey_data()
    processed_data = process_survey_data(survey_data)
    update_survey_worksheet(processed_data)
    latest_survey_data = fetch_latest_survey_data()

    calculate_average_satisfaction()
    calculate_satisfaction_trend()




main()