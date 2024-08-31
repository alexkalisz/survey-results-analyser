import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import datetime
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


def display_welcome_message():
    """
    Display a welcome message with a border and color to make it stand out.
    """
    print("\n" + "=" * 50)
    print(
        "\033[1;32m" +
        "Welcome to Survey Results Analyser for Airfryier Pro" + "\033[0m"
    )
    print("=" * 50 + "\n")


def get_survey_data():
    """
    Ask the user to input survey data.
    This function will keep asking until valid data is provided.
    """
    while True:
        display_welcome_message()
        print("Please enter survey data.\n")
        print(
            "The data should be in the format: "
            "value1,value2,value3,...value7\n"
        )
        print(
            "Example: 01/08/2024,Female,45,4,Yes,Price,"
            "Reasonably priced for what it offers.\n"
        )

        data_str = input("Enter your data here:\n")

        try:
            f = StringIO(data_str)
            reader = csv.reader(f, skipinitialspace=True)
            survey_data = next(reader)
        except StopIteration:
            print("Error: No data entered. Please try again.\n")
            continue

        if validate_data(survey_data):
            print("The data is valid!\n")
            break
        else:
            print("Data invalid. Please try again.\n")

    return survey_data


def validate_data(values):
    """
    Check that the survey data is valid.
    Ensures there are exactly values and
    that the satisfaction score is a number.
    """
    try:
        if len(values) != 7:
            raise ValueError(
                f"Exactly 7 values are required; {len(values)} provided")
        int(values[3])
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def process_survey_data(data):
    """
    Prepare the survey data for updating the worksheet.
    Converts the satisfaction score to a number.
    """
    return [
        data[0],
        data[1],
        data[2],
        int(data[3]),
        data[4],
        data[5],
        data[6]
    ]


def update_worksheet(worksheet_name, data, clear=False):
    """
    Update the specified worksheet with new data.
    Optionally, clear the worksheet before adding the new data.
    """
    print(f"Updating the {worksheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(worksheet_name)

    if clear:
        worksheet.clear()

    if isinstance(data, list) and isinstance(data[0], list):
        worksheet.append_rows(data)
    else:
        worksheet.append_row(data)

    print(f"The {worksheet_name.capitalize(
    )} worksheet has been updated successfully.\n")


def fetch_latest_survey_data():
    """
    Retrieve the most recent survey data entry.
    """
    print("Fetching the latest survey data...\n")
    survey_worksheet = SHEET.worksheet("survey")
    all_survey_data = survey_worksheet.get_all_values()
    latest_survey_data = all_survey_data[-1]
    print(f"Latest survey data: {latest_survey_data}\n")
    return latest_survey_data


def calculate_average_satisfaction():
    """
    Work out the average satisfaction score from the survey data.
    Any invalid or missing satisfaction scores are skipped.
    """
    print("Calculating the average satisfaction...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()

    satisfaction_scores = []

    for row in survey_worksheet[1:]:
        try:
            score = int(row[3])
            satisfaction_scores.append(score)
        except (ValueError, IndexError):
            continue

    if satisfaction_scores:
        average_satisfaction = sum(
            satisfaction_scores) / len(satisfaction_scores)
        print(f"Average satisfaction score: {average_satisfaction:.2f}\n")
        return average_satisfaction
    else:
        print("No valid satisfaction scores found.")
        return None


def group_data_by_month():
    """
    Organize the survey data by month and calculate the average satisfaction
    for each month.
    """
    print("Grouping data by month...\n")
    survey_worksheet = SHEET.worksheet("survey").get_all_values()

    monthly_data = {}

    for row in survey_worksheet[1:]:
        date_str = row[0]

        if not date_str or date_str.lower() == "timestamp":
            print(f"Skipping row with invalid or missing date: {row}")
            continue

        try:
            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            month_year = date_obj.strftime("%Y-%m")

            satisfaction_score = int(row[3])

            if month_year not in monthly_data:
                monthly_data[month_year] = []

            monthly_data[month_year].append(satisfaction_score)
        except ValueError as e:
            print(f"Skipping row due to error: {e}, Row data: {row}")
            continue

    monthly_averages = {
        month: sum(scores) / len(
            scores) for month, scores in monthly_data.items()
    }
    print("Monthly averages:", monthly_averages)
    print()
    return monthly_averages


def calculate_monthly_satisfaction_difference(monthly_averages):
    """
    Work out the difference in satisfaction between consecutive months.
    """
    print("Calculating monthly satisfaction differences...\n")

    sorted_months = sorted(monthly_averages.keys())
    differences = {}

    if len(sorted_months) < 2:
        print("Not enough data to calculate differences.")
        return differences

    for i in range(1, len(sorted_months)):
        current_month = sorted_months[i]
        previous_month = sorted_months[i - 1]
        difference = (
            monthly_averages[current_month] - monthly_averages[previous_month]
        )
        differences[current_month] = difference
        print(f"Difference between {previous_month} and {
            current_month}: {difference} points")

    return differences


def analyze_feature_recommendations():
    """
    Analyze the survey data to determine which
    feature needs improvement based on recommendations.
    """
    worksheet = SHEET.worksheet("survey")
    data = worksheet.get_all_values()[1:]

    feature_recommendations = {
        "Customer Support": 0,
        "Price": 0,
        "Functionality": 0,
        "Ease of Use": 0,
        "Design": 0
    }

    for row in data:
        if len(row) < 6:
            print(f"Skipping incomplete row: {row}")
            continue

        recommend = row[4].strip().lower()
        favourite_feature = row[5].strip()

        if recommend == "no":
            if favourite_feature in feature_recommendations:
                feature_recommendations[favourite_feature] += 1

    recommended_feature = max(
        feature_recommendations, key=feature_recommendations.get
    )

    if feature_recommendations[recommended_feature] > 0:
        return f"Recommended Improvement: Improve {recommended_feature}\n"
    else:
        return None


def update_feature_recommendations(recommendation_text):
    """
    Update the feature recommendations worksheet with the latest suggestion.
    """
    worksheet = SHEET.worksheet("feature_recommendations")
    worksheet.append_row([recommendation_text])
    print(f"Feature Recommendation added successfully: {recommendation_text}.")


def display_thank_you_message():
    """
    Display a thank you message to the user after the survey data is processed.
    """
    print("=" * 50)
    print("Thank you for using Survey Results Analyser!")
    print("=" * 50)
    print("\nYour responses have been successfully recorded.\n")
    print("Worksheet has been updated successfully")
    print("Have a great day!\n")
    print("=" * 50)


def main():
    survey_data = get_survey_data()
    processed_data = process_survey_data(survey_data)
    update_worksheet("survey", processed_data, clear=False)

    latest_survey_data = fetch_latest_survey_data()

    average_satisfaction = calculate_average_satisfaction()
    if average_satisfaction is not None:
        monthly_averages = group_data_by_month()
        if monthly_averages:
            differences = calculate_monthly_satisfaction_difference(
                monthly_averages)
            if differences:
                update_worksheet(
                    "monthly_differences",
                    [[month, diff] for month, diff in differences.items()],
                    clear=True
                )
            else:
                print("No differences to update.")
        else:
            print("No monthly averages to calculate.")
    else:
        print("No valid satisfaction scores to calculate.")

    recommended_feature = analyze_feature_recommendations()

    if recommended_feature:
        update_feature_recommendations(recommended_feature)

    display_thank_you_message()


main()
