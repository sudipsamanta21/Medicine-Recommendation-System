
from flask import Flask, render_template, request, redirect, session, flash ,jsonify
from db import get_db
from twilio.rest import Client
import pandas as pd
import numpy as np
import pickle
import os



app = Flask(__name__)
app.secret_key = "12345"


# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
TWILIO_PHONE = os.getenv('TWILIO_PHONE', '+1234567890')  # Your Twilio phone number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

df = pd.read_csv('./dataset/Medicine_Details.csv', dtype=str)
df.columns = df.columns.str.strip()
df = df.fillna('')   # so blanks show as "" instead of NaN


# MongoDB setup


collection = get_db()

# Load datasets
dataset     = pd.read_csv('./dataset/Training.csv')
description = pd.read_csv("./dataset/description.csv")
precautions = pd.read_csv("./dataset/precautions_df.csv")
medications = pd.read_csv("./dataset/medications.csv")
diets       = pd.read_csv("./dataset/diets.csv")
workout     = pd.read_csv("./dataset/workout_df.csv")

# Load model
svc = pickle.load(open("./models/svc.pkl", "rb"))

# Symptom and disease dictionaries
symptoms_dict = {symptom: idx for idx, symptom in enumerate(dataset.columns[:-1])}
diseases_list = {idx: disease for idx, disease in enumerate(sorted(dataset['prognosis'].unique()))}

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

def helper(dis):
    desc = " ".join(description[description['Disease']==dis]['Description'].values)
    pre = precautions[precautions['Disease']==dis][['Precaution_1','Precaution_2','Precaution_3','Precaution_4']].values.tolist()
    med = medications[medications['Disease']==dis]['Medication'].tolist()
    die = diets[diets['Disease']==dis]['Diet'].tolist()
    wrk = workout[workout['disease']==dis]['workout'].tolist()
    return desc, pre[0] if pre else [], med, die, wrk






# ---------------- ROUTES ---------------- #

@app.route('/about')
def about():
    return render_template("about.html")




@app.route('/developer')
def developer():
    return render_template("developer.html")




@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/medicine_search.html', methods=['GET', 'POST'])
def medicine_search():
    medicine = None
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip().lower()
        # Search in your dataframe (df) for medicine name case-insensitive
        result = df[df['Medicine Name'].str.lower() == name]
        if not result.empty:
            medicine = result.iloc[0].to_dict()
        else:
            error = f"No medicine found with name '{name}'."
    return render_template('medicine_search.html', medicine=medicine, error=error)



# @app.route('/medicine_suggestions')
# def medicine_suggestions():
#     query = request.args.get('q', '').strip().lower()
#     if not query:
#         return jsonify([])
#     # Find medicine names that start with or contain the query (case-insensitive)
#     matches = df[df['Medicine Name'].str.lower().str.contains(query)]['Medicine Name'].unique()
#     suggestions = matches[:10].tolist()  # limit to 10 suggestions
#     return jsonify(suggestions)


@app.route('/medicine_suggestions')
def medicine_suggestions():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])
    matches = df[df['Medicine Name'].str.lower().str.contains(query)]['Medicine Name'].unique()
    suggestions = matches[:10].tolist()
    print(f"Suggestions: {suggestions}")
    return jsonify(suggestions)





@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and email and message:
            contact_data = {
                "name": name,
                "email": email,
                "message": message
            }
            collection.insert_one(contact_data)
            flash("Your message has been sent successfully!", "success")
            return redirect("/contact")
        else:
            flash("All fields are required!", "danger")
            return redirect("/contact")

    return render_template("contact.html")




@app.route("/bmi.html", methods=["GET", "POST"])
def bmi():
    bmi_value = None
    category = None
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"]) / 100  # convert cm to meters
            bmi_value = round(weight / (height ** 2), 2)
            if bmi_value < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi_value < 24.9:
                category = "Normal"
            elif 25 <= bmi_value < 29.9:
                category = "Overweight"
            else:
                category = "Obese"
        except (ValueError, ZeroDivisionError):
            bmi_value = None
            category = "Invalid input. Please enter valid numbers."
    return render_template("bmi.html", bmi_value=bmi_value, category=category)





@app.route("/reminder.html", methods=["GET", "POST"])
def reminder():
    reminder_text = None
    if request.method == "POST":
        medicine = request.form["medicine"]
        time = request.form["time"]
        phone = request.form["phone"]

        reminder_text = f"Reminder: Take your medicine '{medicine}' at {time} ⏰"

        # Send SMS
        try:
            message = client.messages.create(
                body=reminder_text,
                from_=TWILIO_PHONE,
                to=f"+91{phone}"  # India number example
            )
            print("SMS Sent! SID:", message.sid)
        except Exception as e:
            reminder_text = f"Error: {e}"

    return render_template("reminder.html", reminder_text=reminder_text)






@app.route('/')
def home():
    return render_template("index.html",
                           step2=False,
                           predicted_disease=None,
                           dis_desc="",
                           dis_pre=[],
                           dis_med=[],
                           dis_die=[],
                           dis_workout=[])




@app.route('/step1_post', methods=['POST'])
def step1_post():
    session['name'] = request.form.get('name')
    session['mobile'] = request.form.get('mobile')
    session['age'] = request.form.get('age')
    
    return render_template("index.html",
                           step2=True,
                           predicted_disease=None,
                           dis_desc="",
                           dis_pre=[],
                           dis_med=[],
                           dis_die=[],
                           dis_workout=[])





@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.get('symptoms')
    user_symptoms = [s.strip().lower().replace(" ", "_") for s in symptoms.split(',')]
    predicted_disease = get_predicted_value(user_symptoms)
    desc, pre, med, die, wrk = helper(predicted_disease)

    record = {
        "name": session.get('name'),
        "mobile": session.get('mobile'),
        "age": session.get('age'),
        "symptoms": user_symptoms,
        "predicted_disease": predicted_disease,
        "description": desc,
        "precautions": pre,
        "medications": med,
        "diet": die,
        "workout": wrk
    }
    collection.insert_one(record)

    return render_template("index.html",
                           step2=False,
                           predicted_disease=predicted_disease,
                           dis_desc=desc,
                           dis_pre=pre,
                           dis_med=med,
                           dis_die=die,
                           dis_workout=wrk)

if __name__ == "__main__":
    app.run(debug=True)

