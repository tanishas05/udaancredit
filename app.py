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

elif st.session_state.page == "dashboard":
    st.title("Credit Assessment Dashboard")
    st.caption("UPI-based micro-credit evaluation for informal workers")

    top_col1, top_col2 = st.columns([6, 1])
    with top_col2:
        st.button("Logout", on_click=go, args=("login",))

    st.divider()

    # ---------------- DATA UPLOAD ----------------
    st.subheader("Upload Transaction Data")
    uploaded_file = st.file_uploader(
        "Upload UPI Transaction CSV",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])

        # ---------------- OVERVIEW ----------------
        with st.container():
            st.subheader("Transaction Overview")
            st.dataframe(df, use_container_width=True)

        # ---------------- CASHFLOW ----------------
        with st.container():
            st.subheader("Cashflow Analysis")

            col1, col2 = st.columns(2)

            daily = df.groupby("date")["amount"].sum()
            with col1:
                st.caption("Daily Net Cashflow")
                st.line_chart(daily)

            credit = df[df["type"] == "CREDIT"]["amount"].sum()
            debit = df[df["type"] == "DEBIT"]["amount"].sum()

            bar_df = pd.DataFrame(
                {"Amount": [credit, debit]},
                index=["Income", "Expense"]
            )

            with col2:
                st.caption("Income vs Expense")
                st.bar_chart(bar_df)

        # ---------------- FEATURES ----------------
        with st.container():
            st.subheader("Derived Financial Features")
            features = extract_features(df)
            st.json(features)

        # ---------------- CREDIT SCORE ----------------
        with st.container():
            st.subheader("Credit Evaluation")

            score = calculate_credit_score(features)
            risk = risk_category(score)

            m1, m2, m3 = st.columns(3)
            m1.metric("Credit Score", score)
            m2.metric("Risk Category", risk)
            m3.metric("Total Income", f"₹{int(features['total_credit'])}")

        # ---------------- AML ----------------
        with st.container():
            st.subheader("Transaction Risk Monitoring")

            avg_amt = df["amount"].mean()
            suspicious = df[df["amount"] > 2 * avg_amt]

            if suspicious.empty:
                st.success("No anomalous transactions detected")
            else:
                st.warning("Potential anomalous transactions detected")
                st.dataframe(suspicious)

        # ---------------- LOAN ----------------
        with st.container():
            st.subheader("Loan Recommendation")

            eligible_loan = int(features["total_credit"] * 0.3)
            st.write(f"Recommended Loan Amount: ₹{eligible_loan}")

            if score >= 700:
                st.success("Eligible for micro-loan")
            else:
                st.warning("Currently not eligible for micro-loan")

    else:
        st.info("Please upload a UPI transaction CSV to begin analysis.")
