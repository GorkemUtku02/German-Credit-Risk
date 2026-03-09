# 🏦 German Credit Risk Analysis & Prediction System

This is a Full-Stack Machine Learning project that predicts credit risk based on the German Credit dataset. The system features a decoupled architecture using a FastAPI backend, a Streamlit dashboard, and a PostgreSQL database.

## 🏗️ Project Architecture

1. Frontend (Streamlit): Interactive UI for data input and real-time risk visualization.
2. Backend (FastAPI): High-performance API serving the Extra Trees Classifier model.
3. Database (PostgreSQL): Persistent storage for every prediction log.
4. Containerization (Docker): Entire stack orchestrated using Docker Compose.

## 🛠️ Tech Stack

- ML: Scikit-Learn (Extra Trees Classifier), Joblib
- API: FastAPI, Pydantic, SQLAlchemy
- UI: Streamlit, Plotly
- DB: PostgreSQL
- DevOps: Docker, Docker Compose

## 🚀 Quick Start (Docker)

### 1. Clone and Navigate

git clone https://github.com/yourusername/german-credit-risk.git
cd german-credit-risk

### 2. Run with Docker

docker-compose up --build

### 3. Access the Services

- Frontend Dashboard: http://localhost:8501
- Backend API (Swagger): http://localhost:8000/docs

## ✨ Key Features

- Real-time Prediction: Instant "Good" or "Bad" risk assessment.
- Dynamic Analytics: Live Donut Chart reflecting database distribution.
- Automated Schema: Backend initializes the database and tables on startup.
- Robust Data Handling: Pydantic aliases for complex JSON mapping.

## 📊 API Endpoints

| Endpoint | Method | Description                                             |
| :------- | :----- | :------------------------------------------------------ |
| /predict | POST   | Submits user data and returns risk prediction.          |
| /stats   | GET    | Fetches aggregated counts for "Good" and "Bad" results. |
| /        | GET    | Health check for the API.                               |
