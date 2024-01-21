import sqlite3
import csv
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('temperature_data.db')
cursor = conn.cursor()

# Fetch data from the table
cursor.execute('SELECT * FROM temperature_data')
data = cursor.fetchall()

# Get column names
columns = [desc[0] for desc in cursor.description]

# Export to CSV
csv_filename = 'temperature_data.csv'
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(columns)
    csv_writer.writerows(data)

# Export to Excel using pandas
excel_filename = 'temperature_data.xlsx'
df = pd.DataFrame(data, columns=columns)
df.to_excel(excel_filename, index=False)

# Close the connection
conn.close()

print(f'Data exported to {csv_filename} and {excel_filename}.')