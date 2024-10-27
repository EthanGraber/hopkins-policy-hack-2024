#!/bin/bash

# Database name
DB_NAME="nudge_results.db"

# Table name
TABLE_NAME="feedback"

# User ID to use for all records
USER_ID=1503960366

# Sample messages
MESSAGES=(
  "Make time for your physical therapy session today."
  "Remember to move around every hour to stay healthy."
  "Your body is recovering. Keep up the good work with your physical therapy."
)

# Sample increase boolean values
INCREASE_VALUES=("false" "true" "true")

# Create the table if it doesn't exist
sqlite3 "$DB_NAME" "
  CREATE TABLE IF NOT EXISTS $TABLE_NAME (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    increase BOOLEAN NOT NULL
  );
"

# Insert sample data into the table
for i in "${!MESSAGES[@]}"; do
  MESSAGE=${MESSAGES[$i]}
  INCREASE=${INCREASE_VALUES[$i % ${#INCREASE_VALUES[@]}]}
  sqlite3 "$DB_NAME" "INSERT INTO $TABLE_NAME (user_id, message, increase) VALUES ($USER_ID, '$MESSAGE', '$INCREASE');"
done

echo "Sample data inserted into $DB_NAME"
