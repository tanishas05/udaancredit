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

.login-card {
    max-width: 420px;
    margin: 8vh auto;
    padding: 32px;
    border-radius: 20px;
    background: #020617;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 25px 60px rgba(0,0,0,0.7);
}

.brand {
    font-size: 32px;
    font-weight: 700;
    color: #22c55e;
}

.tagline {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 28px;
}

.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: black;
    font-weight: 600;
    border-radius: 12px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #16a34a, #15803d);
}

input {
    border-radius: 10px !important;
}

.card {
    background: #020617;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
}

.risk-low { color: #22c55e; font-weight: 700; }
.risk-medium { color: #facc15; font-weight: 700; }
.risk-high { color: #ef4444; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ================= LOGIN =================
if st.session_state.page == "login":

    st.markdown("""
    <div class="login-card">
        <div class="brand">UdaanCredit</div>
        <div class="tagline">UPI-based micro-credit evaluation</div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Please enter email and password")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create New Account", use_container_width=True):
        go("signup")

    st.markdown("</div>", unsafe_allow_html=True)

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

    # HEADER
    h1, h2 = st.columns([8, 1])
    with h1:
        st.markdown("## UdaanCredit")
        st.caption("UPI-based micro-credit evaluation for informal workers")
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

        # OVERVIEW
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Transaction Overview")
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # CASHFLOW
        st.markdown('<div class="card">', unsafe_allow_html=True)
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

        if score >= 700:
            risk_class = "risk-low"
        elif score >= 600:
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Credit Evaluation")

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Credit Score", score)

        with m2:
            st.markdown(
                f"""
                <div class="{risk_class}" style="font-size:22px;">
                    Risk Category<br>
                    <span style="font-size:28px;">{risk}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # LOAN
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Loan Recommendation")

        eligible = int(features["total_credit"] * 0.3)
        st.write(f"**Recommended Loan Amount:** ₹{eligible}")

        if score >= 700:
            st.success("Eligible for micro-loan")
        else:
            st.warning("High risk — loan not recommended")

        st.markdown('</div>', unsafe_allow_html=True)
