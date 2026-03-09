import streamlit as st

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def hero_section():
    st.markdown("""
    <div class="hero-box">
        <h1>🏦 German Credit Risk AI</h1>
        <p>AI based credit risk analysis dashboard</p>
    </div>
    """, unsafe_allow_html=True)


def good_result():
    st.markdown("""
    <div class="result-good">
    ✅ GOOD CUSTOMER<br>
    Low credit risk detected
    </div>
    """, unsafe_allow_html=True)


def bad_result():
    st.markdown("""
    <div class="result-bad">
    ⚠️ HIGH RISK CUSTOMER
    </div>
    """, unsafe_allow_html=True)