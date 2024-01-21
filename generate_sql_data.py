import sqlite3
from datetime import datetime, timedelta

# Function to generate dummy temperature data
def generate_dummy_data(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield (current_date.strftime('%Y-%m-%d'),
               round(20 + 10 * (current_date.day % 31), 2),  # Dummy temperature for t1
               round(15 + 8 * (current_date.day % 31), 2),   # Dummy temperature for t2
               round(25 + 5 * (current_date.day % 31), 2))   # Dummy temperature for t3
        current_date += timedelta(days=1)

# Connect to SQLite database (creates a new one if not exists)
conn = sqlite3.connect('temperature_data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temperature_data (
        Date DATE PRIMARY KEY,
        t1 REAL,
        t2 REAL,
        t3 REAL
    )
''')

# Generate dummy data for the entire month of December 2023
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 31)
dummy_data = generate_dummy_data(start_date, end_date)

# Insert dummy data into the table
cursor.executemany('INSERT INTO temperature_data VALUES (?, ?, ?, ?)', dummy_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("SQLite database created with dummy data.")
