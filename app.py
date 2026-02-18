import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score, risk_category

st.markdown("""
<style>

/* Main container width */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    font-weight: 600;
    letter-spacing: -0.3px;
}

/* Card style */
.card {
    background: linear-gradient(180deg, #020617, #020617);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Section spacing */
.section {
    margin-top: 2.5rem;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #9ca3af;
}

/* Upload box */
[data-testid="stFileUploader"] {
    border-radius: 14px;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 2.5rem 0;
}

</style>
""", unsafe_allow_html=True)


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

elif st.session_state.page == "dashboard":

    # HEADER
    h1, h2 = st.columns([8, 1])
    with h1:
        st.markdown("## UdaanCredit")
        st.caption("UPI-based micro-credit evaluation for informal workers")
    with h2:
        st.button("Logout", on_click=go, args=("login",))

    st.markdown("<hr>", unsafe_allow_html=True)

    # UPLOAD CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Transaction Data Upload")
    uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].str.upper()
        df["amount"] = pd.to_numeric(df["amount"])

        # OVERVIEW
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.subheader("Transaction Overview")
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # CASHFLOW
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.subheader("Cashflow Analysis")

        c1, c2 = st.columns(2)
        with c1:
            st.caption("Daily Cashflow")
            daily = df.groupby("date")["amount"].sum()
            st.line_chart(daily)

        with c2:
            st.caption("Income vs Expense")
            credit = df[df["type"] == "CREDIT"]["amount"].sum()
            debit = df[df["type"] == "DEBIT"]["amount"].sum()
            st.bar_chart({"Income": credit, "Expense": debit})

        st.markdown('</div>', unsafe_allow_html=True)

        # CREDIT EVALUATION
        features = extract_features(df)
        score = calculate_credit_score(features)
        risk = risk_category(score)

        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.subheader("Credit Evaluation")

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Credit Score", score)
        with m2:
            st.metric("Risk Category", risk)

        st.markdown('</div>', unsafe_allow_html=True)

        # LOAN
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.subheader("Loan Recommendation")
        eligible = int(features["total_credit"] * 0.3)
        st.write(f"**Recommended Loan Amount:** ₹{eligible}")

        if score >= 700:
            st.success("Eligible for micro-loan")
        else:
            st.warning("High risk — loan not recommended")

        st.markdown('</div>', unsafe_allow_html=True)
