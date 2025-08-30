# 💊 Medicine Recommendation System  

A **Flask-based web application** that recommends medicines, shows precautions, diets, and workout suggestions based on symptoms.  
It also integrates **Twilio API** for SMS reminders.  

---

## 🚀 Features
- ✅ Medicine recommendation based on symptoms  
- ✅ Search medicines with details (uses CSV dataset)  
- ✅ Precautions, diets, and workout suggestions  
- ✅ User-friendly web interface (HTML + CSS + Flask templates)  
- ✅ SMS reminders using **Twilio**  

---

🔹 Step 1: Create a Virtual Environment
------>
python -m venv venv

🔹 When it’s activated, you’ll see (venv) before your path, like:
------>
(venv) C:\Users\YourName\Desktop\medicine>

🔹 This command installs everything you need to run your Medicine Recommendation & Reminder System 
   (web app, dataset handling, machine learning, and SMS notifications).
------>
pip install flask pandas numpy twilio scikit-learn




## 📂 Project Structure
medicine/
│
├── config.py
├── db.py
├── main.py
├── README.md
│
├── dataset/
│   ├── Medicine_Details.csv
│   ├── Symptom-severity.csv
│   ├── Training.csv
│   ├── description.csv
│   ├── diets.csv
│   ├── medications.csv
│   ├── precautions_df.csv
│   ├── symtoms_df.csv
│   └── workout_df.csv
│
├── models/
│   ├── Medicine Recommendation System.ipynb
│   └── svc.pkl
│
├── static/
│   └── img.png
│
├── templates/
│   ├── about.html
│   ├── blog.html
│   ├── bmi.html
│   ├── contact.html
│   ├── developer.html
│   ├── index.html
│   ├── medicine_search.html
│   └── reminder.html
│
└── venv/   (🚫 GitHub )






