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

# ================= LOGIN =================
if st.session_state.page == "login":
    st.title("UdaanCredit")
    st.caption("UPI-based micro-credit evaluation for informal workers")

    st.subheader("User Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Email and password required")

    st.button("Create New Account", on_click=go, args=("signup",))

# ================= SIGNUP =================
elif st.session_state.page == "signup":
    st.title("UdaanCredit")
    st.subheader("Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            st.success("Account created. Please login.")
            go("login")
        else:
            st.error("All fields required")

    st.button("Back to Login", on_click=go, args=("login",))

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":

    # ---------- HEADER ----------
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("UdaanCredit")
        st.caption("UPI-based micro-credit evaluation for informal workers")
    with col2:
        st.button("Logout", on_click=go, args=("login",))

    st.divider()

    # ---------- UPLOAD ----------
    st.subheader("Transaction Data Upload")
    uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].str.upper().str.strip()
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        # ---------- OVERVIEW ----------
        st.subheader("Transaction Overview")
        st.dataframe(df, use_container_width=True)

        st.divider()

        # ---------- CASHFLOW ----------
        st.subheader("Cashflow Analysis")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Daily Cashflow**")
            daily = df.groupby("date")["amount"].sum()
            st.line_chart(daily)

        with c2:
            st.markdown("**Income vs Expense**")
            credit = df[df["type"] == "CREDIT"]["amount"].sum()
            debit = df[df["type"] == "DEBIT"]["amount"].sum()

            bar_df = pd.DataFrame(
                {"Amount": [credit, debit]},
                index=["Income", "Expense"]
            )
            st.bar_chart(bar_df)

        st.divider()

        # ---------- FEATURES ----------
        st.subheader("Derived Financial Features")
        features = extract_features(df)
        st.json(features)

        st.divider()

        # ---------- CREDIT EVALUATION ----------
        st.subheader("Credit Evaluation")

        score = calculate_credit_score(features)
        risk = risk_category(score)

        b1, b2 = st.columns(2)

        with b1:
            st.metric("Credit Score", score)

        with b2:
            st.metric("Risk Category", risk)

        st.divider()

        # ---------- LOAN ----------
        st.subheader("Loan Recommendation")

        eligible_loan = int(features["total_credit"] * 0.3)
        st.write(f"**Recommended Loan Amount:** ₹{eligible_loan}")

        if score >= 700:
            st.success("Eligible for micro-loan")
        else:
            st.warning("Currently not eligible for micro-loan")

    else:
        st.info("Please upload a UPI CSV file to begin analysis")



