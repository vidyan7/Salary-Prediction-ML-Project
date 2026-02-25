# Salary-Prediction-ML-Project

A Machine Learning–based Salary Prediction web application built using Flask.  
The system predicts employee salaries based on age, gender, education level, job title, and years of experience using a trained Random Forest model.

---

## Project Overview

This project is designed to demonstrate the practical integration of a Machine Learning model into a web application.  
It allows users to register, log in securely, and predict salaries by providing relevant employee details.

The backend uses a Random Forest regression model trained on historical salary data, while the frontend is built using Flask templates for a clean and simple user interface.

---

## Features

- Salary prediction using Machine Learning
- Random Forest regression model
- User authentication (Registration & Login)
- Secure access using Flask-Login
- Flask-based web application
- Modular and clean project structure

---

## Technologies Used

- Python
- Flask
- Scikit-learn
- Random Forest Algorithm
- HTML / CSS
- SQLite
- Pickle

---

## Project Structure

```
Salary-Prediction-ML-Project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   ├── salary_rf_model.pkl
│   └── lb_Job_Title.pkl
│
├── dataset/
│   └── salary_data.csv
│
├── training/
│   └── training.ipynb
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── predict.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── lib/
│   └── scss/
│
└── instance/
    └── README.md

```

---

## How to Run the Project

1. Install required libraries:
   ```bash
   pip install -r requirements.txt


2.Run the Flask application:
  ```bash
   python app.py
  ```
3. Open your browser and go to:
   http://127.0.0.1:5000/
