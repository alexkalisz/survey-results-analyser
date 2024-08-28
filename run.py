import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import csv
from pprint import pprint
import datetime

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

def update_worksheet(worksheet_name, data):
    """
    Updates the specified worksheet with the provided data.
    """
    print(f"Updating {worksheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(worksheet_name)
    if isinstance(data, list) and isinstance(data[0], list):
        worksheet.append_rows(data)
    else:
        worksheet.append_row(data)
    print(f"{worksheet_name.capitalize()} worksheet updated successfully.\n")

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

def group_data_by_month():
    """
    Groups survey data by month and calculates the average satisfaction for each month.
    """
    print("Grouping data by month...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()

    monthly_data = {}
    
    for row in survey_worksheet[1:]:
        date_str = row[0]
        date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        month_year = date_obj.strftime("%Y-%m")

        satisfaction_score = int(row[3])  
        if month_year not in monthly_data:
            monthly_data[month_year] = []

        monthly_data[month_year].append(satisfaction_score)

   
    monthly_averages = {month: sum(scores) / len(scores) for month, scores in monthly_data.items()}

    print("Monthly averages:", monthly_averages)
    return monthly_averages

def calculate_monthly_satisfaction_difference(monthly_averages):
    """
    Calculate the difference in satisfaction between each month.
    """
    print("Calculating monthly satisfaction differences...\n")
    
    sorted_months = sorted(monthly_averages.keys())
    differences = {}

    for i in range(1, len(sorted_months)):
        current_month = sorted_months[i]
        previous_month = sorted_months[i - 1]

        difference = monthly_averages[current_month] - monthly_averages[previous_month]
        differences[current_month] = difference

        print(f"Difference between {previous_month} and {current_month}: {difference} points")

    return differences

def get_last_5_entries_survey():
    """
    Collects columns of data from the survey worksheet, collecting
    the last 5 entries for each relevant column and returns the data
    as a list of lists.
    """
    survey = SHEET.worksheet("survey")

    columns = []
    for ind in range(1, 7):
        column = survey.col_values(ind)
        columns.append(column[-5:])

    return columns

def analyze_feature_recommendations(survey_data):
    print("Analyzing feature recommendations...\n")
    feature_counts = {
        "Improve Customer Support": 0,
        "Improve Price": 0,
        "Improve Functionality": 0,
        "Improve Ease of Use": 0,
        "Improve Design": 0
    }
    for row in survey_data:
        if len(row) < 6:
            print(f"Skipping incomplete row: {row}")
            continue
        feature = row[5]
        if feature in feature_counts:
            feature_counts[feature] += 1
    recommended_feature = max(feature_counts, key=feature_counts.get)
    print(f"Feature to focus on for improvements: {recommended_feature}")
    return recommended_feature

def main():
    survey_data = get_survey_data()
    processed_data = process_survey_data(survey_data)
    update_worksheet("survey", processed_data)
    latest_survey_data = fetch_latest_survey_data()
    calculate_average_satisfaction()
    monthly_averages = group_data_by_month()
    differences = calculate_monthly_satisfaction_difference(monthly_averages)
    update_worksheet("monthly_differences", [[month, diff] for month, diff in differences.items()])

last_5_entries = get_last_5_entries_survey()
   





main()

