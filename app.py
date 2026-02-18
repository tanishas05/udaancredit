import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score, risk_category

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UdaanCredit",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.title("UdaanCredit")

    st.subheader("User Login")
    st.write("Access your credit assessment dashboard")

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Email and password are required")

    st.button("Create New Account", on_click=go, args=("signup",))

# ---------------- SIGNUP PAGE ----------------
elif st.session_state.page == "signup":
    st.title("UdaanCredit")

    st.subheader("Account Registration")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            st.success("Account created successfully. Please login.")
            go("login")
        else:
            st.error("All fields must be filled")

    st.button("Back to Login", on_click=go, args=("login",))

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":
    st.title("Credit Assessment Dashboard")
    st.caption("UPI-based micro-credit evaluation for informal workers")

    st.button("Logout", on_click=go, args=("login",))
    st.divider()

    # ---------------- DATA UPLOAD ----------------
    with st.container():
        st.subheader("Transaction Data Upload")
        uploaded_file = st.file_uploader(
            "Upload UPI Transaction CSV",
            type=["csv"]
        )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Data cleaning
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].astype(str).str.strip().str.upper()
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        # ---------------- DATA PREVIEW ----------------
        with st.container():
            st.subheader("Transaction Overview")
            st.dataframe(df, use_container_width=True)

        # ---------------- FEATURE EXTRACTION ----------------
        with st.container():
            features = extract_features(df)
            score = calculate_credit_score(features)
            risk = risk_category(score)
            eligible_loan = int(features["total_credit"] * 0.3)

        # ---------------- SUMMARY METRICS ----------------
        with st.container():
            st.subheader("Financial Summary")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Total Income (₹)", int(features["total_credit"]))
            with c2:
                st.metric("Total Expense (₹)", int(features["total_debit"]))
            with c3:
                st.metric("Credit Score", score)
            with c4:
                st.metric("Risk Category", risk)

        # ---------------- CASHFLOW & INFLOW-OUTFLOW ----------------
        with st.container():
            st.subheader("Cashflow Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Cashflow Over Time")
                daily = df.groupby("date")["amount"].sum()
                st.line_chart(daily, use_container_width=True)

            with col2:
                st.write("Income vs Expense")

                credit = df[df["type"] == "CREDIT"]["amount"].sum()
                debit = df[df["type"] == "DEBIT"]["amount"].sum()

                bar_df = pd.DataFrame({
                    "Category": ["Income", "Expense"],
                    "Amount": [credit, debit]
                }).set_index("Category")

                if credit == 0 and debit == 0:
                    st.warning("No valid income or expense data available.")
                else:
                    st.bar_chart(bar_df, use_container_width=True)

        # ---------------- AML MONITORING ----------------
        with st.container():
            st.subheader("Transaction Risk Monitoring")

            avg_amt = df["amount"].mean()
            suspicious = df[df["amount"] > 2 * avg_amt]

            if suspicious.empty:
                st.success("No anomalous transactions detected")
            else:
                st.warning("Potential anomalous transactions identified")
                st.dataframe(suspicious, use_container_width=True)

        # ---------------- LOAN RECOMMENDATION ----------------
        with st.container():
            st.subheader("Loan Recommendation")
            st.write(f"Recommended Loan Amount: ₹{eligible_loan}")

            if score >= 700:
                st.success("Eligible for micro-loan")
            else:
                st.warning("Currently not eligible for micro-loan")

    else:
        st.info("Please upload a sample UPI CSV file to begin analysis")

