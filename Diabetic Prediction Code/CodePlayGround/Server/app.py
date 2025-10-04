from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import pickle
import os

load_dotenv()

app = Flask(__name__)

CORS(app)
model = pickle.load(open("adaboost_model.pkl", 'rb'))
scaler = pickle.load(open("scaler.pkl", 'rb'))
# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database("Diebeties")  # Make sure this matches your DB name
people_collection = db.peoples

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    print(name)
    print(email)
    print(password)
    print("Request JSON:", request.json)
    print("Parsed email:", email)

    if people_collection.find_one({"email": email}):
        print(f"Checking for email: {email}")
        user = people_collection.find_one({"email": email})
        print("MongoDB returned:", user)
        return jsonify("exist")
    else:
         people_collection.insert_one({
            "name": name,
            "email": email,
            "password": password
        })
    return jsonify("Success")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = people_collection.find_one({"email": email})
    if user:
        if user["password"] == password:
            return jsonify("Success")
        else:
            return jsonify("Incorrect password")
    else:
        return jsonify("Please create an account first")
    


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    print("Received JSON:", data)  # Debug log

    input_data = data.get("input_data")
    input_data = input_data = [
    int(data["Pregnancies"]),
    float(data["Glucose"]),
    float(data["BloodPressure"]),
    float(data["SkinThickness"]),
    float(data["Insulin"]),
    float(data["BMI"]),
    float(data["DiabetesPedigreeFunction"]),
    int(data["Age"])
]
    print(input_data)
    ans1=not input_data
    print(ans1)
    # if not input_data or len(input_data) != 8:
    #     print("not 8")
    #     return jsonify({"error": "Invalid input data"}), 400


    # Define column names
    columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 
               'BMI', 'DiabetesPedigreeFunction', 'Age']
    input_df = pd.DataFrame([input_data], columns=columns)

    # Required dummy columns
    required_dummies = [
        'NewBMI_Obesity 1', 'NewBMI_Obesity 2', 'NewBMI_Obesity 3', 'NewBMI_Overweight',
        'NewBMI_Underweight', 'NewInsulinScore_Normal', 'NewGlucose_Low', 
        'NewGlucose_Normal', 'NewGlucose_Overweight', 'NewGlucose_Secret', 
        'NewBMI_Normal', 'NewInsulinScore_Abnormal', 'NewGlucose_High'
    ]

    for col in required_dummies:
        input_df[col] = False

    # BMI Category
    bmi = input_df.at[0, "BMI"]
    if bmi < 18.5:
        input_df.at[0, "NewBMI_Underweight"] = True
    elif 18.5 < bmi <= 24.9:
        input_df.at[0, "NewBMI_Normal"] = True
    elif 24.9 < bmi <= 29.9:
        input_df.at[0, "NewBMI_Overweight"] = True
    elif 29.9 < bmi <= 34.9:
        input_df.at[0, "NewBMI_Obesity 1"] = True
    elif 34.9 < bmi <= 39.9:
        input_df.at[0, "NewBMI_Obesity 2"] = True
    elif bmi > 39.9:
        input_df.at[0, "NewBMI_Obesity 3"] = True

    # Insulin Score
    insulin = input_df.at[0, "Insulin"]
    if 16 <= insulin <= 166:
        input_df.at[0, "NewInsulinScore_Normal"] = True
    else:
        input_df.at[0, "NewInsulinScore_Abnormal"] = True

    # Glucose Category
    glucose = input_df.at[0, "Glucose"]
    if glucose <= 70:
        input_df.at[0, "NewGlucose_Low"] = True
    elif 70 < glucose <= 99:
        input_df.at[0, "NewGlucose_Normal"] = True
    elif 99 < glucose <= 126:
        input_df.at[0, "NewGlucose_Overweight"] = True
    elif 126 < glucose <= 200:
        input_df.at[0, "NewGlucose_Secret"] = True
    else:
        input_df.at[0, "NewGlucose_High"] = True

    # Scale numerical data
    numerical_df = input_df[columns]
    scaled_numerical = scaler.transform(numerical_df)
    scaled_df = pd.DataFrame(scaled_numerical, columns=columns)

    # Get dummy columns
    categorical_df = input_df[required_dummies]

    # Merge for final input
    final_input = pd.concat([scaled_df, categorical_df], axis=1)

    # Make prediction
    prediction = model.predict(final_input)[0]
    result = "Positive" if prediction == 1 else "Negative"
    print(result)
    return jsonify({"prediction": result})




if __name__ == '__main__':
    app.run(port=3001, debug=True)
