import streamlit as st
import requests
import pandas as pd
import plotly.express as px


#refresh the stats every 30 seconds to keep the dashboard updated with new predictions
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=30000, key="datarefresh")

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="German Credit Risk AI", layout="wide")

# --- CSS INJECTION ---
# Reads the external CSS file and applies it to the app
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# --- SIDEBAR - DATA INPUT ---
st.sidebar.header("Customer Information")
with st.sidebar:
    age = st.slider("Age", 18, 80, 30)
    sex = st.selectbox("Sex", ["male", "female"])
    job = st.radio("Job Level", [0, 1, 2, 3], index=2)
    housing = st.selectbox("Housing Status", ["own", "rent", "free"])
    saving = st.selectbox("Saving Accounts", ["little", "moderate", "rich", "quite rich"])
    checking = st.selectbox("Checking Account", ["little", "moderate", "rich"])
    amount = st.number_input("Credit Amount ($)", value=1000, step=100)
    duration = st.slider("Duration (Month)", 6, 72, 12)

# --- MAIN INTERFACE ---
st.title("🏦 German Credit Risk - AI Dashboard")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔍 Prediction Engine")
    if st.button("Analyze Risk"):
        # Construct payload with aliases to match Backend Pydantic model
        payload = {
            "Age": int(age),
            "Sex": sex,
            "Job": int(job),
            "Housing": housing,
            "Saving accounts": saving,
            "Checking account": checking,
            "Credit amount": int(amount),
            "Duration": int(duration)
        }
        
        try:
            with st.spinner('Calculating risk factors...'):
                response = requests.post("http://backend:8000/predict", json=payload)
            
            if response.status_code == 200:
                prediction = response.json()['result']
                
                # Visual feedback based on prediction
                if prediction == "Good":
                    st.success(f"### Result: {prediction}")
                    st.metric(label="System Verdict", value="LOW RISK", delta="Safe to Proceed")
                else:
                    st.error(f"### Result: {prediction}")
                    st.metric(label="System Verdict", value="HIGH RISK", delta="- Critical Warning", delta_color="inverse")
            else:
                st.warning(f"Backend issue: {response.text}")
        except Exception as e:
            st.error(f"Connection Lost: {e}")


with col2:
    st.subheader("📊 Global Risk Distribution")
    try:
        stats_res = requests.get("http://backend:8000/stats", timeout=5)
        
        if stats_res.status_code == 200:
            stats_data = stats_res.json()
            
            if stats_data and sum(stats_data.values()) > 0:
                labels = list(stats_data.keys())
                values = list(stats_data.values())

                fig = px.pie(
                    names=labels, 
                    values=values, 
                    hole=0.6,
                    color=labels,
                    color_discrete_map={'Good': '#10b981', 'Bad': '#ef4444'}
                )

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=10, b=10, l=10, r=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.write(f"🔍 **Total Processed:** {sum(values)}")
            else:
                st.info("No prediction data yet. Please click 'Analyze Risk' to generate data!")
        else:
            st.error("API Error: Backend unreachable.")
            
    except Exception as e:
        st.error(f"Chart Error: {e}")

st.markdown("---")
st.caption("© 2026 AI Financial Systems | German Credit Risk Project")