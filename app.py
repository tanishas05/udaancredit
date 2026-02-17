import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score, risk_category

st.set_page_config(page_title="UdaanCredit", layout="wide")

st.title("UdaanCredit — UPI Based Micro-Credit Scoring")
st.caption("Turning cashflow into creditworthiness for informal workers")

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

    pie_df = pd.DataFrame({
        "Type": ["Inflow", "Outflow"],
        "Amount": [credit, debit]
    })

    st.bar_chart(pie_df.set_index("Type"))

    # ---------------- FEATURE EXTRACTION ----------------
    features = extract_features(df)

    st.subheader("Extracted Features")
    st.json(features)

    # ---------------- CREDIT SCORE ----------------
    score = calculate_credit_score(features)
    risk = risk_category(score)

    st.subheader("Credit Score")
    st.metric(label="Score", value=score)

    st.subheader("Risk Category")
    st.success(risk)

    # ---------------- AML CHECK ----------------
    st.subheader("AML Risk Check")

    avg_amt = df["amount"].mean()
    suspicious = df[df["amount"] > 2 * avg_amt]

    if not suspicious.empty:
        st.error("⚠️ Unusual transaction detected")
        st.write(suspicious)
    else:
        st.success("No AML anomalies detected")

    # ---------------- LOAN RECOMMENDATION ----------------
    st.subheader("Loan Recommendation")

    eligible_loan = features["total_credit"] * 0.3
    st.write(f"Eligible Loan Amount: ₹{int(eligible_loan)}")

    if score >= 700:
        st.success("Eligible for Micro-loan")
    else:
        st.error("Not eligible yet")

else:
    st.info("Upload sample_upi.csv to test")