import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score, risk_category

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UdaanCredit",
    layout="wide"
)

# ---------------- DARK MODE CSS ----------------
st.markdown("""
<style>
    body {
        background-color: #0f172a;
        color: #e5e7eb;
    }
    .main-title {
        font-size: 28px;
        font-weight: 600;
        color: #f8fafc;
    }
    .subtitle {
        color: #94a3b8;
        margin-bottom: 12px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 24px;
        margin-bottom: 10px;
        color: #e5e7eb;
    }
    .thin-line {
        height: 1px;
        background-color: #334155;
        margin: 20px 0;
    }
    .card {
        background-color: #020617;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.markdown("<div class='main-title'>UdaanCredit</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>UPI-based micro-credit evaluation platform</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>User Login</div>", unsafe_allow_html=True)

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
    st.markdown("<div class='main-title'>UdaanCredit</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Create your account</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Account Registration</div>", unsafe_allow_html=True)

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

    # -------- HEADER --------
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("<div class='main-title'>UdaanCredit</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>UPI-based micro-credit evaluation for informal workers</div>", unsafe_allow_html=True)
    with col2:
        st.button("Logout", on_click=go, args=("login",))

    st.markdown("<div class='thin-line'></div>", unsafe_allow_html=True)

    # -------- DATA UPLOAD --------
    st.markdown("<div class='section-title'>Transaction Data Upload</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload UPI Transaction CSV",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])

        # -------- TRANSACTION OVERVIEW --------
        st.markdown("<div class='section-title'>Transaction Overview</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        st.markdown("<div class='thin-line'></div>", unsafe_allow_html=True)

        # -------- CASHFLOW (SIDE BY SIDE) --------
        st.markdown("<div class='section-title'>Cashflow Analysis</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>Daily Cashflow</div>", unsafe_allow_html=True)
            daily = df.groupby("date")["amount"].sum()
            st.line_chart(daily)

        with col2:
            st.markdown("<div class='card'>Income vs Expense</div>", unsafe_allow_html=True)
            credit = df[df["type"] == "CREDIT"]["amount"].sum()
            debit = df[df["type"] == "DEBIT"]["amount"].sum()

            bar_df = pd.DataFrame({
                "Amount": [credit, debit]
            }, index=["Income", "Expense"])

            st.bar_chart(bar_df)

        st.markdown("<div class='thin-line'></div>", unsafe_allow_html=True)

        # -------- FEATURES --------
        st.markdown("<div class='section-title'>Derived Financial Features</div>", unsafe_allow_html=True)
        features = extract_features(df)
        st.json(features)

        st.markdown("<div class='thin-line'></div>", unsafe_allow_html=True)

        # -------- CREDIT SCORE & RISK (SEPARATE BOXES) --------
        st.markdown("<div class='section-title'>Credit Evaluation</div>", unsafe_allow_html=True)

        score = calculate_credit_score(features)
        risk = risk_category(score)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("Credit Score", score)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("Risk Category", risk)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='thin-line'></div>", unsafe_allow_html=True)

        # -------- LOAN RECOMMENDATION --------
        st.markdown("<div class='section-title'>Loan Recommendation</div>", unsafe_allow_html=True)

        eligible_loan = int(features["total_credit"] * 0.3)
        st.markdown(f"**Recommended Loan Amount:** ₹{eligible_loan}")

        if score >= 700:
            st.success("Eligible for micro-loan")
        else:
            st.warning("Currently not eligible for micro-loan")

    else:
        st.info("Please upload a sample UPI CSV file to begin analysis")



