import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score

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

/* ---------- Login ---------- */
.login-card {
    max-width: 420px;
    margin: auto;
    margin-top: 12vh;
    padding: 32px;
    border-radius: 18px;
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(148,163,184,0.12);
}
.brand {
    font-size: 30px;
    font-weight: 700;
    color: #6366f1;
    text-align: center;
}
.tagline {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 24px;
}

/* ---------- Cards ---------- */
.section {
    margin-top: 42px;
}
.card {
    background: linear-gradient(
        180deg,
        rgba(2,6,23,0.95),
        rgba(2,6,23,0.80)
    );
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 16px;
    padding: 22px 26px;
}
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #c7d2fe;
    margin-bottom: 14px;
}

/* ---------- Risk Colors ---------- */
.risk-low { color: #22c55e; }
.risk-medium { color: #facc15; }
.risk-high { color: #f43f5e; }

/* ---------- Badges ---------- */
.badge {
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 600;
    display: inline-block;
}
.badge-success {
    background: rgba(34,197,94,0.15);
    color: #22c55e;
}
.badge-warning {
    background: rgba(250,204,21,0.15);
    color: #facc15;
}
.badge-danger {
    background: rgba(244,63,94,0.15);
    color: #f43f5e;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ================= LOGIN =================
if st.session_state.page == "login":
    st.markdown("""
    <div class="login-card">
        <div class="brand">UdaanCredit</div>
        <div class="tagline">UPI-based Micro Credit Intelligence</div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if email and password:
            st.session_state.user = email
            go("dashboard")
        else:
            st.error("Please enter email and password")

    st.caption("🔐 Secure • RBI-aligned • Encrypted data")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":

    # Header
    h1, h2 = st.columns([8, 1])
    with h1:
        st.markdown("## UdaanCredit")
        st.caption("Smart credit evaluation for informal workers")
    with h2:
        st.button("Logout", on_click=go, args=("login",))

    # Upload Section
    st.markdown('<div class="section card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📤 Upload Transactions</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload UPI CSV", type=["csv"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].str.upper()
        df["amount"] = pd.to_numeric(df["amount"])

        # Snapshot
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Financial Snapshot</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Income", f"₹{df[df.type=='CREDIT'].amount.sum():,.0f}")
        c2.metric("Total Expense", f"₹{df[df.type=='DEBIT'].amount.sum():,.0f}")
        c3.metric("Transactions", len(df))

        st.markdown('</div>', unsafe_allow_html=True)

        # Cashflow
        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Cashflow Pattern</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            daily = df.groupby("date")["amount"].sum()
            st.line_chart(daily)
        with col2:
            credit = df[df["type"]=="CREDIT"]["amount"].sum()
            debit = df[df["type"]=="DEBIT"]["amount"].sum()
            st.bar_chart({"Income": credit, "Expense": debit})

        st.markdown('</div>', unsafe_allow_html=True)

        # Credit Intelligence
        features = extract_features(df)
        score = calculate_credit_score(features)

        ratio = features["credit_debit_ratio"]
        freq = features["txn_frequency"]

        if score >= 720 and ratio > 1.2 and freq > 20:
            risk = "Low Risk"
            risk_class = "risk-low"
        elif score >= 620 and ratio > 0.9:
            risk = "Moderate Risk"
            risk_class = "risk-medium"
        else:
            risk = "High Risk"
            risk_class = "risk-high"

        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧠 Credit Intelligence</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Credit Score", score)
        with c2:
            st.markdown(f"<h2 class='{risk_class}'>{risk}</h2>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Loan Recommendation
        eligible = int(features["total_credit"] * 0.3)

        st.markdown('<div class="section card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💸 Loan Recommendation</div>', unsafe_allow_html=True)

        st.write(f"**Recommended Loan Amount:** ₹{eligible:,}")

        if risk == "Low Risk":
            st.markdown('<div class="badge badge-success">Approved for Instant Micro-Loan</div>', unsafe_allow_html=True)
        elif risk == "Moderate Risk":
            st.markdown('<div class="badge badge-warning">Eligible with Conditions</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge badge-danger">Loan Not Recommended</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


