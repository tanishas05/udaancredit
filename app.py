import streamlit as st
import pandas as pd
from utils import extract_features
from scoring import calculate_credit_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UdaanCredit",
    page_icon="↑",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
}
.stApp {
    background: #04070f;
    color: #e8eef8;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px;
}

/* ---- Background orbs ---- */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(59,130,246,0.09) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(34,211,238,0.07) 0%, transparent 60%);
}

/* ---- Inputs ---- */
.stTextInput > div > div > input,
.stFileUploader > div {
    background: #0b1120 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8eef8 !important;
    font-family: 'Sora', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}
.stTextInput label, .stFileUploader label {
    color: #7a90b0 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 0 0 24px rgba(59,130,246,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    box-shadow: 0 0 36px rgba(59,130,246,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #7a90b0 !important;
    box-shadow: none !important;
}

/* ---- Metrics ---- */
[data-testid="metric-container"] {
    background: #0b1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px !important;
}
[data-testid="metric-container"] label {
    color: #7a90b0 !important;
    font-size: 0.78rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.06em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e8eef8 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

/* ---- Charts ---- */
[data-testid="stArrowVegaLiteChart"], .stLineChart, .stBarChart {
    background: transparent !important;
    border-radius: 10px;
}

/* ---- Alerts ---- */
.stAlert { border-radius: 10px !important; }

/* ---- Divider ---- */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ---- Custom Components ---- */
.udaan-nav {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 0 24px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 32px;
}
.udaan-logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.2rem; font-weight: 800; color: #e8eef8;
    letter-spacing: -0.02em;
}
.udaan-logo-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #3b82f6, #22d3ee);
    border-radius: 9px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 16px; font-weight: 800;
}
.udaan-user {
    font-size: 0.82rem; color: #7a90b0;
    font-family: 'JetBrains Mono', monospace;
}

.login-wrap {
    max-width: 420px; margin: 10vh auto 0;
}
.login-card {
    background: #0b1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px; padding: 44px 40px;
    box-shadow: 0 0 80px rgba(59,130,246,0.07);
}
.login-brand {
    text-align: center; margin-bottom: 28px;
}
.login-title {
    font-size: 1.55rem; font-weight: 800;
    letter-spacing: -0.02em; text-align: center;
    color: #e8eef8; margin-bottom: 6px;
}
.login-sub {
    color: #7a90b0; font-size: 0.88rem;
    text-align: center; margin-bottom: 28px;
}
.login-footer {
    text-align: center; font-size: 0.74rem;
    color: #3a4f6a; margin-top: 16px;
}

.section-card {
    background: #0b1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 28px;
    margin-bottom: 20px;
}
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 1rem; font-weight: 700; color: #e8eef8;
}
.section-icon {
    font-size: 1.1rem;
}

.score-display {
    display: flex; align-items: center; gap: 32px;
    padding: 24px;
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(34,211,238,0.06));
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px; margin-bottom: 20px;
}
.score-number {
    font-size: 4rem; font-weight: 800;
    background: linear-gradient(135deg, #22d3ee, #3b82f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.score-label {
    font-size: 0.75rem; color: #7a90b0;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em;
    margin-bottom: 6px;
}
.score-desc { font-size: 0.88rem; color: #e8eef8; }
.score-out { font-size: 0.78rem; color: #7a90b0; margin-top: 4px; }

.risk-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 18px; border-radius: 100px;
    font-weight: 700; font-size: 0.9rem;
}
.risk-low { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.25); }
.risk-medium { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.risk-high { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

.loan-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(34,211,238,0.04));
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 16px; padding: 24px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 16px;
}
.loan-amount {
    font-size: 2rem; font-weight: 800; color: #34d399;
    font-family: 'JetBrains Mono', monospace;
}
.loan-label { font-size: 0.75rem; color: #7a90b0; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em; margin-bottom: 4px; }
.loan-rate { font-size: 0.85rem; color: #7a90b0; }

.verdict-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 12px 20px; border-radius: 12px;
    font-weight: 700; font-size: 0.92rem;
}
.verdict-approved { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.25); }
.verdict-conditional { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.verdict-rejected { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

.factor-row {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 12px;
}
.factor-label-text {
    font-size: 0.78rem; color: #7a90b0; width: 160px; flex-shrink: 0;
}
.factor-bar-bg {
    flex: 1; height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 100px; overflow: hidden;
}
.factor-bar-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #3b82f6, #22d3ee);
}
.factor-val-text {
    font-size: 0.75rem; color: #e8eef8;
    font-family: 'JetBrains Mono', monospace;
    width: 44px; text-align: right;
}

.upload-hint {
    font-size: 0.78rem; color: #3a4f6a;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 8px;
}
.mono { font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ================== LOGIN ==================
if st.session_state.page == "login":

    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-card">
        <div class="login-brand">
            <span style="display:inline-flex;align-items:center;gap:10px;font-size:1.15rem;font-weight:800;color:#e8eef8;letter-spacing:-0.02em;">
                <span class="udaan-logo-icon">↑</span>
                UdaanCredit
            </span>
        </div>
        <div class="login-title">Welcome back</div>
        <div class="login-sub">Login to check your credit score and offers</div>
    </div>
    """, unsafe_allow_html=True)

    # Inputs rendered by Streamlit inside the visual card
    with st.container():
        email = st.text_input("EMAIL ADDRESS", placeholder="you@example.com", key="login_email")
        password = st.text_input("PASSWORD", placeholder="••••••••", type="password", key="login_pass")

        if st.button("Login to Dashboard →", use_container_width=True):
            if email and password:
                st.session_state.user = email
                go("dashboard")
                st.rerun()
            else:
                st.error("Please enter your email and password.")

    st.markdown("""
        <div class="login-footer">🔐 Secure · RBI-aligned · Encrypted data</div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================== DASHBOARD ==================
elif st.session_state.page == "dashboard":

    # --- Nav ---
    user_email = st.session_state.get("user", "user@example.com")
    col_logo, col_user, col_logout = st.columns([6, 3, 1])
    with col_logo:
        st.markdown("""
        <div class="udaan-logo">
            <span class="udaan-logo-icon">↑</span>
            UdaanCredit
        </div>
        """, unsafe_allow_html=True)
    with col_user:
        st.markdown(f'<div class="udaan-user" style="padding-top:8px;">👤 {user_email}</div>', unsafe_allow_html=True)
    with col_logout:
        if st.button("Logout", key="logout"):
            go("login")
            st.rerun()

    st.markdown('<hr>', unsafe_allow_html=True)

    # --- Upload ---
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;">📤 UPLOAD UPI TRANSACTIONS</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your UPI statement CSV",
        type=["csv"],
        help="Export CSV from PhonePe, GPay, Paytm, or BHIM"
    )
    st.markdown('<div class="upload-hint">Supported: PhonePe · Google Pay · Paytm · BHIM · Any UPI app CSV export</div>', unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#3a4f6a;">
            <div style="font-size:2.5rem;margin-bottom:12px;">📂</div>
            <div style="font-size:0.9rem;font-family:'JetBrains Mono',monospace;">Upload a CSV to generate your credit score</div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].str.upper()
        df["amount"] = pd.to_numeric(df["amount"])

        features = extract_features(df)
        score = calculate_credit_score(features)

        ratio = features["credit_debit_ratio"] if "credit_debit_ratio" in features else features["total_credit"] / max(features["total_debit"], 1)
        freq = features.get("txn_frequency", len(df))

        if score >= 720 and ratio > 1.2 and freq > 20:
            risk = "Low Risk"
            risk_class = "risk-low"
            risk_icon = "✅"
        elif score >= 620 and ratio > 0.9:
            risk = "Moderate Risk"
            risk_class = "risk-medium"
            risk_icon = "⚠️"
        else:
            risk = "High Risk"
            risk_class = "risk-high"
            risk_icon = "❌"

        eligible = int(features["total_credit"] * 0.3)

        # --- Financial Snapshot ---
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
            <span style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;">📊 FINANCIAL SNAPSHOT</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL INCOME", f"₹{features['total_credit']:,.0f}")
        c2.metric("TOTAL EXPENSE", f"₹{features['total_debit']:,.0f}")
        c3.metric("TRANSACTIONS", len(df))
        net = features['total_credit'] - features['total_debit']
        c4.metric("NET CASHFLOW", f"₹{net:,.0f}", delta=f"{'↑' if net > 0 else '↓'} Net")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Cashflow Charts ---
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
            <span style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;">📈 CASHFLOW PATTERN</span>
        </div>
        """, unsafe_allow_html=True)

        import plotly.graph_objects as go
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Daily Transaction Volume")
            daily = df.groupby("date")["amount"].sum().reset_index()
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=daily["date"], y=daily["amount"],
                mode="lines+markers",
                line=dict(color="#3b82f6", width=2),
                marker=dict(color="#22d3ee", size=5),
                fill="tozeroy", fillcolor="rgba(59,130,246,0.1)"
            ))
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=0,b=0), height=220,
                xaxis=dict(showgrid=False, color="#7a90b0", tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#7a90b0", tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.caption("Income vs Expense")
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=["Income", "Expense"],
                y=[features['total_credit'], features['total_debit']],
                marker_color=["#22d3ee", "#f43f5e"],
                width=0.4
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=0,b=0), height=220,
                xaxis=dict(showgrid=False, color="#7a90b0", tickfont=dict(size=11)),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#7a90b0", tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)


        # --- Credit Score ---
        score_pct = int((score - 300) / 600 * 100)
        inflow_pct = min(int(features['inflow_count'] / max(features['outflow_count'], 1) * 50), 100)
        ticket_pct = min(int(features['avg_ticket_size'] / 1000 * 100), 100)
        stability_pct = min(int(features.get('cashflow_stability', 0.5) * 100), 100)

        if risk == "Low Risk":
            risk_color = "#34d399"; risk_bg = "rgba(16,185,129,0.12)"; risk_border = "rgba(16,185,129,0.25)"
            verdict_icon = "✅"; verdict_text = "Approved for Instant Micro-Loan"
            verdict_color = "#34d399"; verdict_bg = "rgba(16,185,129,0.12)"; verdict_border = "rgba(16,185,129,0.25)"
            rate = "14.5% p.a."
        elif risk == "Moderate Risk":
            risk_color = "#fbbf24"; risk_bg = "rgba(245,158,11,0.12)"; risk_border = "rgba(245,158,11,0.25)"
            verdict_icon = "⚠️"; verdict_text = "Eligible with Conditions"
            verdict_color = "#fbbf24"; verdict_bg = "rgba(245,158,11,0.12)"; verdict_border = "rgba(245,158,11,0.25)"
            rate = "18.0% p.a."
        else:
            risk_color = "#f87171"; risk_bg = "rgba(239,68,68,0.12)"; risk_border = "rgba(239,68,68,0.25)"
            verdict_icon = "❌"; verdict_text = "Loan Not Recommended"
            verdict_color = "#f87171"; verdict_bg = "rgba(239,68,68,0.12)"; verdict_border = "rgba(239,68,68,0.25)"
            rate = "N/A"

        def fbar(label, pct):
            return (
                f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">' +
                f'<span style="font-size:0.76rem;color:#7a90b0;width:148px;flex-shrink:0;">{label}</span>' +
                f'<div style="flex:1;height:5px;background:rgba(255,255,255,0.06);border-radius:100px;overflow:hidden;">' +
                f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#3b82f6,#22d3ee);border-radius:100px;"></div>' +
                f'</div>' +
                f'<span style="font-size:0.72rem;color:#e8eef8;font-family:monospace;width:34px;text-align:right;">{pct}%</span>' +
                f'</div>'
            )

        col_score, col_factors = st.columns([1, 2])

        with col_score:
            st.markdown(
                f'''<div style="background:#0b1120;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:20px;">
                <div style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;margin-bottom:6px;">🧠 AI CREDIT SCORE</div>
                <div style="font-size:3rem;font-weight:800;background:linear-gradient(135deg,#22d3ee,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;font-family:monospace;">{score}</div>
                <div style="font-size:0.75rem;color:#7a90b0;margin-top:4px;margin-bottom:14px;">out of 900</div>
                <div style="display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:100px;background:{risk_bg};border:1px solid {risk_border};color:{risk_color};font-weight:700;font-size:0.82rem;">{risk_icon} {risk}</div>
                </div>''',
                unsafe_allow_html=True
            )

        with col_factors:
            st.markdown(
                f'''<div style="background:#0b1120;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:20px;">
                <div style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;margin-bottom:14px;">SCORING FACTORS</div>
                {fbar("Credit score range", score_pct)}
                {fbar("Inflow / Outflow ratio", inflow_pct)}
                {fbar("Avg ticket size", ticket_pct)}
                {fbar("Cashflow stability", stability_pct)}
                </div>''',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # --- Loan Recommendation ---
        st.markdown(
            f'''<div style="background:rgba(16,185,129,0.05);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:18px 22px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;">
            <div>
                <div style="font-size:0.7rem;color:#7a90b0;font-family:monospace;letter-spacing:0.1em;margin-bottom:5px;">💸 LOAN RECOMMENDATION</div>
                <div style="font-size:1.7rem;font-weight:800;color:#34d399;font-family:monospace;">₹{eligible:,}</div>
                <div style="font-size:0.78rem;color:#7a90b0;margin-top:2px;">Rate: <span style="font-family:monospace;">{rate}</span></div>
            </div>
            <div style="display:inline-flex;align-items:center;gap:7px;padding:9px 16px;border-radius:10px;background:{verdict_bg};border:1px solid {verdict_border};color:{verdict_color};font-weight:700;font-size:0.85rem;">
                {verdict_icon} {verdict_text}
            </div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # --- Raw Data Toggle ---
        with st.expander("🔍 View Raw Transaction Data"):
            st.dataframe(df, use_container_width=True)
