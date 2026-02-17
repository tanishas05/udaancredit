import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import extract_features
from scoring import calculate_credit_score, risk_category

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="UdaanCredit", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.title("🔐 UdaanCredit Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Please enter email and password")

    st.button("Create new account", on_click=go, args=("signup",))

# ---------------- SIGNUP PAGE ----------------
elif st.session_state.page == "signup":
    st.title("📝 Create UdaanCredit Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            st.success("Account created successfully")
            go("login")
        else:
            st.error("All fields are required")

    st.button("Back to login", on_click=go, args=("login",))

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":
    st.title("📊 UdaanCredit Dashboard")
    st.caption("Turning cashflow into creditworthiness for informal workers")

    st.button("Logout", on_click=go, args=("login",))

    uploaded_file = st.file_uploader("Upload UPI CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("Raw Data")
        st.dataframe(df)

        # Convert date
        df["date"] = pd.to_datetime(df["date"])

        # ---------------- CASHFLOW GRAPH ----------------
        st.subheader("Cashflow Over Time")
        daily = df.groupby("date")["amount"].sum()
        st.line_chart(daily)

        # ---------------- INFLOW VS OUTFLOW ----------------
        st.subheader("Inflow vs Outflow")
        credit = df[df["type"] == "CREDIT"]["amount"].sum()
        debit = df[df["type"] == "DEBIT"]["amount"].sum()

        bar_df = pd.DataFrame({
            "Type": ["Inflow", "Outflow"],
            "Amount": [credit, debit]
        })

        st.bar_chart(bar_df.set_index("Type"))

        # ---------------- FEATURE EXTRACTION ----------------
        features = extract_features(df)

        st.subheader("Extracted Features")
        st.json(features)

        # ---------------- CREDIT SCORE ----------------
        score = calculate_credit_score(features)
        risk = risk_category(score)

        st.subheader("Credit Score")
        st.metric("Score", score)

        st.subheader("Risk Category")
        st.success(risk)

        # ---------------- AML CHECK ----------------
        st.subheader("🚨 AML Risk Check")

        avg_amt = df["amount"].mean()
        suspicious = df[df["amount"] > 2 * avg_amt]

        if not suspicious.empty:
            st.error("Unusual transaction detected")
            st.dataframe(suspicious)
        else:
            st.success("No AML anomalies detected")

        # ---------------- LOAN RECOMMENDATION ----------------
        st.subheader("🏦 Loan Recommendation")

        eligible_loan = int(features["total_credit"] * 0.3)
        st.write(f"Eligible Loan Amount: ₹{eligible_loan}")

        if score >= 700:
            st.success("Eligible for Micro-loan")
        else:
            st.warning("Not eligible yet")

    else:
        st.info("Upload sample_upi.csv to test")
