# 1 Good (lower risk) 0 bad (Higher risk)

import streamlit as st
import pandas as pd 
import joblib
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:8U8T5K8U@localhost:5432/German_Credit_Risk')
model = joblib.load("best_extra_trees_model.pkl")
encoders = {col: joblib.load(f"{col}_encoder.pkl") for col in ["Sex","Housing","Saving accounts","Checking account"]}

st.title("Credit Risk Prediction App")
st.write("Enter applicant information to predict if the credit risk is good or bad: ")

age = st.number_input("Age", min_value=18, max_value=80, value=30)
sex = st.selectbox("Sex", options=["male", "female"])
job = st.number_input("Job (0-3)", min_value=0, max_value=3, value=1)
housing = st.selectbox("Housing", options=["own", "rent", "free"])
saving_accounts = st.selectbox("Saving accounts", options=["little", "moderate", "rich", "quite rich"])
checking_account = st.selectbox("Checking account", options=["little", "moderate", "rich"])
credit_amount = st.number_input("Credit amount", min_value=0, value=1000)
duration = st.number_input("Duration (months)", min_value=1, value=12)

input_data = pd.DataFrame({
    "Age": [age],
    "Sex": [encoders["Sex"].transform([sex])[0]],
    "Job": [job],
    "Housing": [encoders["Housing"].transform([housing])[0]],
    "Saving accounts": [encoders["Saving accounts"].transform([saving_accounts])[0]],
    "Checking account": [encoders["Checking account"].transform([checking_account])[0]],
    "Credit amount": [credit_amount],
    "Duration": [duration]
})


def log_prediction_to_db(input_data, result):
    try:
        # Add the infomation to a DataFrame for logging
        log_df = input_data.copy()
        log_df['prediction_result'] = "Risky"if result == 1 else "Riskless"
        # Send information to SQL 
        log_df.to_sql('prediction_logs',engine,if_exists = 'append', index=False, schema='public')
        return True
    except Exception as e:
        st.error(f"Error logging prediction to database: {e}")
        return False
    

if st.button("Predict Risk"):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.success("Predicted Risk: **Good (Lower Risk)**")

    else:
        st.error("Predicted Risk: **Bad (Higher Risk)**")

    with st.spinner("Logging prediction to database..."):
        if log_prediction_to_db(input_data, prediction):
            st.success("Prediction logged successfully!")
        else:
            st.error("Failed to log prediction.")



