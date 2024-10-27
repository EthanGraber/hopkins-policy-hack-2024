from pathlib import Path
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


    

def analyze_fitbit_activity(patient_id_directory : Path) -> bool:

    # Initialize lists to hold the data
    all_steps = []
    all_calories = []
    all_dates = []

    # Loop through each date folder within the patient ID directory
    for date_folder in os.listdir(patient_id_directory):
        date_folder_path = os.path.join(patient_id_directory, date_folder)
        if os.path.isdir(date_folder_path):
            for file in os.listdir(date_folder_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(date_folder_path, file)
                    daily_data = pd.read_csv(file_path)
                    if 'StepTotal' in daily_data.columns:
                        total_steps = daily_data['StepTotal'].sum()
                        all_steps.append(total_steps)
                        all_dates.append(pd.to_datetime(date_folder))
                    if 'Calories' in daily_data.columns and 'ActivityHour' in daily_data.columns:
                        total_calories = daily_data['Calories'].sum()
                        all_calories.append(total_calories)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'date': all_dates,
        'steps': all_steps,
        'calories': all_calories
    })

    # Sort data by date descending
    df = df.sort_values(by='date')

    # Take the most recent 8 days (1 day for comparison, 7 days for the previous period)
    df = df.tail(8)
    print(df)
    # Separate the most recent day and the previous 7 days
    recent_week_df = df.head(7)
    most_recent_day_df = df.tail(1)

    # Fit a linear regression model for steps
    X_week = np.arange(len(recent_week_df)).reshape(-1, 1)  # Day indices for the previous week
    y_steps_week = recent_week_df['steps'].values
    y_calories_week = recent_week_df['calories'].values

    # Linear regression for steps
    model_steps = LinearRegression()
    model_steps.fit(X_week, y_steps_week)
    
    # Linear regression for calories
    model_calories = LinearRegression()
    model_calories.fit(X_week, y_calories_week)

    # Predict the steps and calories for the next day (i.e., day 7)
    next_day_index = np.array([[7]])  # The next day to predict for (8th day)
    predicted_steps = model_steps.predict(next_day_index)
    predicted_calories = model_calories.predict(next_day_index)

    # Get the actual steps and calories for the most recent day
    actual_steps = most_recent_day_df['steps'].values[0]
    actual_calories = most_recent_day_df['calories'].values[0]

    # Compare the predicted vs actual
    steps_improved = actual_steps > predicted_steps[0]
    calories_improved = actual_calories > predicted_calories[0]

    
    if steps_improved or calories_improved:
        return True
    else:
        return False

# Example usage:
result = analyze_activity_improvement_with_regression('./1503960366')
print(result)

