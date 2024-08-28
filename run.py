import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import csv
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
        int(values[3])  # Ensure that the satisfaction score is an integer

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
    print(f"Updating {worksheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(worksheet_name)
    
    # Clear the worksheet only if it's the "monthly_differences" sheet
    if worksheet_name == "monthly_differences":
        worksheet.batch_clear(['2:{}'.format(worksheet.row_count)])

    if isinstance(data, list) and isinstance(data[0], list):
        worksheet.append_rows(data)
    else:
        worksheet.append_row(data)

    print(f"{worksheet_name.capitalize()} worksheet updated successfully.\n")


def fetch_latest_survey_data():
    print("Fetching latest survey data...\n")
    survey_worksheet = SHEET.worksheet("survey")
    all_survey_data = survey_worksheet.get_all_values()
    latest_survey_data = all_survey_data[-1]
    print(f"Latest survey data: {latest_survey_data}")
    return latest_survey_data

def calculate_average_satisfaction():
    print("Calculating average satisfaction...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()
    
    satisfaction_scores = []
    for row in survey_worksheet[1:]:
        try:
            score = int(row[3])
            satisfaction_scores.append(score)
        except (ValueError, IndexError):
            print(f"Skipping invalid or missing satisfaction score: {row}")
    
    if satisfaction_scores:
        average_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
        print(f"Average satisfaction score: {average_satisfaction:.2f}")
        return average_satisfaction
    else:
        print("No valid satisfaction scores found.")
        return None

def group_data_by_month():
    print("Grouping data by month...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()

    monthly_data = {}
    
    for row in survey_worksheet[1:]:
        date_str = row[0]
        date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        month_year = date_obj.strftime("%Y-%m")

        try:
            satisfaction_score = int(row[3])
        except ValueError:
            continue

        if month_year not in monthly_data:
            monthly_data[month_year] = []

        monthly_data[month_year].append(satisfaction_score)

    monthly_averages = {month: sum(scores) / len(scores) for month, scores in monthly_data.items()}
    print("Monthly averages:", monthly_averages)
    return monthly_averages

def calculate_monthly_satisfaction_difference(monthly_averages):
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
    survey = SHEET.worksheet("survey")

    columns = []
    for ind in range(1, 7):
        column = survey.col_values(ind)
        columns.append(column[-5:])

    return columns

def analyze_feature_recommendations(survey_data):
    print("Analyzing feature recommendations...\n")
    feature_counts = {
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

def update_feature_recommendations(recommended_feature):
    worksheet = SHEET.worksheet("feature_recommendations")
    existing_recommendations = worksheet.col_values(1)
    recommendation_text = f"Recommended Improvement: {recommended_feature}"

    if recommendation_text not in existing_recommendations:
        worksheet.append_row([recommendation_text])
        print("Feature Recommendations updated successfully.\n")
    else:
        print("This recommendation already exists in the worksheet.\n")

def main():
    survey_data = get_survey_data()
    processed_data = process_survey_data(survey_data)
    update_worksheet("survey", processed_data)

    latest_survey_data = fetch_latest_survey_data()

    average_satisfaction = calculate_average_satisfaction()
    if average_satisfaction is not None:
        monthly_averages = group_data_by_month()
        if monthly_averages:
            differences = calculate_monthly_satisfaction_difference(monthly_averages)
            if differences:
                update_worksheet("monthly_differences", [[month, diff] for month, diff in differences.items()])
            else:
                print("No differences to update.")
        else:
            print("No monthly averages to calculate.")
    else:
        print("No valid satisfaction scores to calculate.")

    recommended_feature = analyze_feature_recommendations(survey_data)
    update_feature_recommendations(recommended_feature)

main()
