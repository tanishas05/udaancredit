import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score, risk_category

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UdaanCredit",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #020617, #000);
    color: #e5e7eb;
}
.section { margin-top: 28px; }
.card {
    background: rgba(2,6,23,0.85);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 22px 26px;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 16px;
}
.risk-low { color: #4ade80; }
.risk-medium { color: #facc15; }
.risk-high { color: #fb7185; }
.badge {
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 500;
}
.badge-danger {
    background: rgba(251,113,133,0.12);
    color: #fb7185;
}
.badge-success {
    background: rgba(74,222,128,0.12);
    color: #4ade80;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ================= LOGIN =================
if st.session_state.page == "login":
    st.markdown("<h2>UdaanCredit</h2>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Please enter email and password")

    if st.button("Create New Account", use_container_width=True):
        go("signup")

# ================= SIGNUP =================
elif st.session_state.page == "signup":
    st.title("Create Account")

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

    h1, h2 = st.columns([8, 1])
    with h1:
        st.markdown("## UdaanCredit")
        st.caption("UPI-based micro-credit evaluation")
    with h2:
        st.button("Logout", on_click=go, args=("login",))

    st.markdown("<hr>", unsafe_allow_html=True)

    # UPLOAD
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Transaction Data Upload")
    uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].str.upper()
        df["amount"] = pd.to_numeric(df["amount"])

        # TRANSACTION OVERVIEW
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Transaction Overview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # CASHFLOW
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cashflow Analysis</div>', unsafe_allow_html=True)

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

        if score >= 700:
            risk_class = "risk-low"
        elif score >= 600:
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"

        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Credit Evaluation</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Credit Score", score)
        with c2:
            st.markdown(
                f'<div class="{risk_class}" style="font-size:24px;">{risk}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # LOAN RECOMMENDATION
        eligible = int(features["total_credit"] * 0.3)

        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Loan Recommendation</div>', unsafe_allow_html=True)

        st.write(f"**Recommended Loan Amount:** ₹{eligible}")

        if score >= 700:
            st.markdown('<div class="badge badge-success">Eligible for micro-loan</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge badge-danger">High risk — loan not recommended</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

