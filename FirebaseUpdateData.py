import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from datetime import datetime
import importlib.util
spec = importlib.util.spec_from_file_location("ProcessData", "ProcessData.py")  # Update with correct file path
ProcessData = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ProcessData)

df = ProcessData.df
index_temperature = ProcessData.index_temperature
month = ProcessData.current_month

try:
    app = firebase_admin.get_app(name="myApp")
except ValueError:
    cred = credentials.Certificate("agribot-d56f2-firebase-adminsdk-2g95k-faf737f0b4.json")
    app = firebase_admin.initialize_app(cred, name="myApp")

db = firestore.client(app=app)

# Assuming index_temperature is the index of the row for the entered month
if df.loc[index_temperature, 'India Growing Season'].find(month) != -1: 
    data = {
        "Crops": df.loc[index_temperature, 'Crops'],
        "Temperature(in Cel)": df.loc[index_temperature, 'Temperature(in Cel)'],
        "India Growing Season": df.loc[index_temperature, 'India Growing Season'],
        "Days to Maturity": df.loc[index_temperature, 'Days to Maturity'],
        "Humidity (%)": df.loc[index_temperature, 'Humidity (%)'],
        "PH Value": df.loc[index_temperature, 'PH Value'],
        "Soil Moisture (%)": df.loc[index_temperature, 'Soil Moisture (%)']
    }
    
    document_id = "AgriBotDataUpdate1"
    db.collection("AgriBot").document(document_id).set(data)
    print("Data added/updated successfully!")
else:
    print("No harvestable crops available for the Season.")

    # Upload "No crops to harvest" to Firestore
    no_crops_data = {"Message": "No harvestable crops available for the Season."}
    document_id = "AgriBotDataUpdate1"
    db.collection("AgriBot").document(document_id).set(no_crops_data)
    print("No crops data added/updated successfully!")
