import pandas as pd
import numpy as np
from datetime import datetime
import importlib.util

# Dynamically import the function from FirebaseGetValues.py
spec = importlib.util.spec_from_file_location("FirebaseGetValues", "FirebaseGetValues.py")  # Update with correct file path
FirebaseGetValues = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FirebaseGetValues)

# Get the moisture value from FirebaseGetValues module
moisture = FirebaseGetValues.moisture
temperature = FirebaseGetValues.temperature
ph = FirebaseGetValues.ph
humidity = FirebaseGetValues.humidity

# Load the dataset
df = pd.read_excel('agriV.xlsx')  # Update with the correct file path and name

# Get the current month
current_month = datetime.now().strftime("%B")  # Full month name, e.g., April

# Convert month name to title case
current_month = current_month.capitalize()

# Function to process temperature ranges
def process_temperature_range(temp_range):
    if '-' in temp_range:
        lower, upper = map(float, temp_range.split('-'))
        return (lower + upper) / 2  # Calculate average for the range
    else:
        return float(temp_range)  # Convert single value to float

# Clean and convert temperature strings to float for comparison
df['Temperature(in Cel)'] = df['Temperature(in Cel)'].apply(process_temperature_range)

# Calculate differences for each column
diff_moisture = np.abs(df['Soil Moisture (%)'] - moisture)
diff_temperature = np.abs(df['Temperature(in Cel)'] - temperature)
diff_humidity = np.abs(df['Humidity (%)'] - humidity)
diff_ph = np.abs(df['PH Value'] - ph)

# Find index of minimum difference for temperature column
index_temperature = diff_temperature.idxmin()
# index_humidity = diff_humidity.idxmin()
# Check if the nearest values match the current month

if df.loc[index_temperature, 'India Growing Season'].find(current_month) != -1:
    print(f"Nearest values from the dataset for the entered data:")
    print("\nAccording to the Temperature\n")
    print(df.loc[index_temperature, ['Crops', 'Temperature(in Cel)', 'India Growing Season', 'Days to Maturity', 'Humidity (%)', 'PH Value', 'Soil Moisture (%)']])
else:
    print("No harvestable crops available for the Season.")