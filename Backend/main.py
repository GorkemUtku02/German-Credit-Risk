from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from sqlalchemy import create_engine, text
import os
from typing import Dict

app = FastAPI()

@app.on_event("startup")
def create_tables():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS prediction_logs (
                id SERIAL PRIMARY KEY,
                age INT,
                sex TEXT,
                job INT,
                housing TEXT,
                saving_accounts TEXT,
                checking_account TEXT,
                credit_amount INT,
                duration INT,
                result TEXT
            )
        """))

@app.get("/stats", response_model=Dict[str, int])
def get_stats():
    try:
        with engine.connect() as conn:
            query = text("SELECT result, COUNT(*) as count FROM prediction_logs GROUP BY result")
            result_set = conn.execute(query)
            
            # Veriye ._mapping kullanarak erişmek KeyError hatasını kesin bitirir
            stats = {str(row._mapping['result']): int(row._mapping['count']) for row in result_set}
            
            return {"Good": stats.get("Good", 0), "Bad": stats.get("Bad", 0)}
    except Exception as e:
        print(f"DB Read Error (stats): {e}")
        return {"Good": 0, "Bad": 0}

# --- 1. Database and Model Loading ---
# Database connection string for PostgreSQL
engine = create_engine('postgresql://postgres:8U8T5K8U@db:5432/german_credit_risk')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Load the trained model and label encoders
model = joblib.load(os.path.join(MODELS_DIR, "best_extra_trees_model.pkl"))
encoders = {
    "Sex": joblib.load(os.path.join(MODELS_DIR, "Sex_encoder.pkl")),
    "Housing": joblib.load(os.path.join(MODELS_DIR, "Housing_encoder.pkl")),
    "Saving accounts": joblib.load(os.path.join(MODELS_DIR, "Saving accounts_encoder.pkl")),
    "Checking account": joblib.load(os.path.join(MODELS_DIR, "Checking account_encoder.pkl"))
}

# --- 2. Data Structure (Handling spaces with Field aliases) ---
class CreditInput(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    Saving_accounts: str = Field(alias="Saving accounts")
    Checking_account: str = Field(alias="Checking account")
    Credit_amount: int = Field(alias="Credit amount")
    Duration: int

    class Config:
        populate_by_name = True

@app.get("/")
def home():
    return {"status": "API is running"}

# --- 3. Statistics Endpoint for Streamlit Chart ---
# --- 3. Statistics Endpoint (Reading from prediction_logs) ---
@app.get("/stats", response_model=Dict[str, int])
def get_stats():
    try:
        with engine.connect() as conn:
            query = text("SELECT result, COUNT(*) as count FROM prediction_logs GROUP BY result")
            result_set = conn.execute(query)
            
          
            stats = {str(row.result): int(row.count) for row in result_set}
            
            
            if not stats:
                return {"Good": 0, "Bad": 0}
            
            return stats
    except Exception as e:
        print(f"DB Read Error (stats): {e}")
        return {"Good": 0, "Bad": 0}

# --- 4. Prediction and Database Insertion (Writing to prediction_logs) ---
@app.post("/predict")
def predict(request: CreditInput):
    try:
        # --- 1. PREPARE DATA ---
        input_data = request.dict(by_alias=True)
        encoded_data = input_data.copy()
        
        # --- 2. ENCODING ---
        for col, encoder in encoders.items():
            encoded_data[col] = encoder.transform([input_data[col]])[0]

        # --- 3. CREATE FEATURES ---
        features = [
            encoded_data["Age"], encoded_data["Sex"], encoded_data["Job"],
            encoded_data["Housing"], encoded_data["Saving accounts"],
            encoded_data["Checking account"], encoded_data["Credit amount"],
            encoded_data["Duration"]
        ]
        
        # --- 4. PREDICT ---
        prediction_idx = model.predict([features])[0]
        prediction_result = "Good" if prediction_idx == 0 else "Bad"

        # --- 5. DATABASE INSERT 
        try:
            with engine.begin() as conn:
                sql_query = text("""
                    INSERT INTO prediction_logs (
                        age, sex, job, housing, saving_accounts, 
                        checking_account, credit_amount, duration, result
                    ) 
                    VALUES (:a, :s, :j, :h, :sa, :ca, :cam, :d, :r)
                """)
                
                conn.execute(sql_query, {
                    "a": int(request.Age),
                    "s": str(request.Sex),
                    "j": int(request.Job),
                    "h": str(request.Housing),
                    "sa": str(request.Saving_accounts),
                    "ca": str(request.Checking_account),
                    "cam": int(request.Credit_amount),
                    "d": int(request.Duration),
                    "r": str(prediction_result)
                })
                print(f"✅ DB SUCCESS: Full log recorded.")
        except Exception as db_error:
            print(f"❌ DB INSERT ERROR: {db_error}")

        return {"result": prediction_result}

    except Exception as e:
        print(f"🔥 GENERAL ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# to run the API: python -m uvicorn main:app --reload