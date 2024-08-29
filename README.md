# Survey Results Analyser

View the Live App [here](https://survey-results-analyser-1-d3cc473f48c0.herokuapp.com/)


The **Survey Results Analyser** is a Python-based application designed to streamline the collection, processing, and analysis of survey data. This application integrates with Google Sheets, ensuring that all survey data is securely stored and easily accessible. It allows users to input survey data, calculate monthly satisfaction averages, track trends over time, and generate feature improvement recommendations based on user feedback.

![App Screenshot](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Application.png)


## Table of Contents
- [User Expectations](#user-expectations)
- [Flow Chart](#flow-chart)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Python Libraries](#python-libraries)
- [Testing](#testing)
- [Deployment](#deployment)
- [How to Clone the Project](#how-to-clone-the-project)
- [How to Fork the Repository](#how-to-fork-the-repository)
- [Credits and References](#credits-and-references)

## User Expectations

### Ease of Use
The application offers a user-friendly interface, guiding users through the process of inputting survey data. Clear prompts and immediate feedback ensure that data is entered correctly and efficiently.

### Accurate Calculations
Users can trust the app to process survey data accurately, producing precise calculations related to satisfaction scores and trends. The results are displayed in a clear and understandable format.

### Data Security
The application ensures that all survey data is securely stored in Google Sheets, with access limited to authorized users.

## Flow Chart

This flow chart provides a high-level overview of how the application operates, showing the flow of data from input to analysis and user interactions throughout the process.

![Flow Chart](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Flow%20chart.png)

## Features

### Start of the App
- **Welcome Message**: Users are greeted with a friendly welcome message and instructions on how to input their survey data.

  ![Welcome message](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Welcome%20message.png)

### Data Validation
- **Input Validation**: The app checks the validity of survey data upon entry. If any data is incorrect or incomplete, the user is notified immediately and prompted to correct the issue.

### Data Processing and Analysis
- **Data Grouping**: The app groups survey responses by the month they were received, facilitating the calculation of monthly averages.
- **Monthly Satisfaction Differences**: The app calculates the difference in satisfaction scores between months, allowing users to track trends over time.
-   ![Data updates](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Monthly%20averages.png)


### Feature Improvement Recommendations
- **Recommendations**: Based on the survey data, the app identifies which features need improvement. These recommendations are added to the "feature_recommendations" worksheet.

  ![Feature recommendation](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Feature%20recommendation.png)

### Google Sheets Integration
- **Data Storage**: All processed data, including survey responses, calculated averages, and feature recommendations, is stored in Google Sheets for easy access and review.

### Final Message
- **Completion Message**: After processing and updating the data, the app displays a final message confirming the successful completion of the task and thank you message for using services.
  ![Thank you message](https://github.com/alexkalisz/survey-results-analyser/blob/main/Images/Thank%20you.png)


## Technologies Used

- **Python**: Core programming language used to build the application.
- **GitHub**: Platform used for version control, code storage, and collaboration.
- **Gitpod**: Cloud-based development environment used for coding and testing.
- **Heroku**: Platform used for deploying and hosting the application online.
- **Microsoft Powerpoint**: Tool used for designing flowcharts and diagrams to map out project logic.
- **Google Sheets**: Used to store and manage survey data for the application.
- **Google Cloud**: Platform for accessing APIs and managing cloud resources.

## Python Libraries

- **Gspread**: A library used to interact with Google Sheets, enabling the reading and writing of data programmatically.
- **google.oauth2.service_account**: Used for authentication and authorization with Google APIs using service account credentials.
- **Datetime**: Standard Python library used to work with dates and times, including parsing, formatting, and manipulating date-related data.

## Testing

### Validator Testing
The application code was validated using Code Institute’s Python Linter, ensuring that it adheres to best practices. No errors were found during validation.

  ![Thank you message](

### Manual Testing

| Test Case | Input Scenario | Actual Result | Pass / Fail |
| --------- | -------------- | ------------- | ----------- |
| Application Loads without Any Error Messages | N/A | No error messages displayed | Pass |
| Welcome Message Displayed | N/A | Welcome message displayed and awaiting user input | Pass |
| Survey Data Input Validation | Invalid Input (e.g., wrong format or missing values) | Displays invalid input message and prompts user for correct input | Pass |
| Monthly Differences Calculation | Incorrect Data (e.g., incorrect date format) | Displays error message and skips the incorrect row | Pass |
| Feature Recommendation Update | Valid Input | Correctly identifies and updates the recommended feature | Pass |

## Deployment

### How to Deploy the Project

1. **Create a Heroku Account and Log In**:
   - If you don’t already have a Heroku account, sign up at [Heroku](https://www.heroku.com/). Log in if you have an existing account.

2. **Create a New App**:
   - Go to your Heroku dashboard and click on “New,” then select “Create new app.”
   - Provide a name for your app and choose a region, then click on “Create app.”

3. **Configure Settings**:
   - Navigate to the “Settings” tab at the top of the page.
   - Under “Config Vars,” set your Key/Value pairs as needed.

4. **Add Buildpacks**:
   - In the “Buildpacks” section, add the required buildpacks in the following order:
     - Click the Python icon and select “Add Buildpack.”
     - Next, click the Node.js icon and select “Add Buildpack.”

5. **Set Up Deployment**:
   - Go to the “Deployment” tab.
   - Under “Deployment method,” choose “GitHub” if your repository is hosted there.
   - In the “Connect to GitHub” section, find your repository and click “Connect.”
   - To enable automatic deployments, click “Enable Automatic Deploys.” For a one-time deployment, go to the “Manual Deploy” section and click “Deploy Manually.”

## How to Clone the Project

1. **Log into GitHub**:
   - Visit [GitHub](https://github.com/) and log in to your account.

2. **Navigate to the Project Repository**:
   - Go to the repository at [Survey Results Analyser](https://github.com/alexkalisz/survey-results-analyser).

3. **Copy the Repository Link**:
   - Click the “Code” button and copy your preferred link (either HTTPS or SSH).

4. **Clone the Repository**:
   - Open the terminal in your code editor.
   - Change the working directory to the location where you want to clone the repository.
   - Type `git clone` followed by the link you copied and press Enter.

## How to Fork the Repository

1. **Log into GitHub**:
   - Visit [GitHub](https://github.com/) and log in to your account.

2. **Navigate to the Project Repository**:
   - Go to the repository at [Survey Results Analyser](https://github.com/alexkalisz/survey-results-analyser).

3. **Fork the Repository**:
   - Click the “Fork” button in the top right corner of the page.

## Credits and References

### API Creation, Encryption Key, and Google Cloud Integration:
This project uses concepts and techniques from the Code Institute: "Love Sandwiches" project.

### References
Some codes were researched in Stack Overflow, Particular code of the welcome message and feature recommendation data calculation was requested from ChatGPT, open AI.

