import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==== PAGE CONFIGURATION ==== #
st.set_page_config(
    page_title="ClaimWatch AI", layout="wide", initial_sidebar_state="expanded"
)

# ---- CUSTOM STYLING ---- #
st.markdown(
    """
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    /* Overall dark background and font */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* hide default Streamlit header */
    header .css-1v3fvcr {
        visibility: hidden;
    }

    /* Titles */
    .big-font {
        font-size:2.5rem !important;
        font-weight: 700;
        color: #fff;
    }
    .sub-header {
        font-size:1.25rem !important;
        color: #bbb;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(90deg, #6200ea 0%, #3700b3 100%);
        padding: 2rem 0;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1, .hero p {
        color: #fff;
        margin: 0;
    }

    /* Buttons */
    .stButton>button {
        color: #ffffff;
        background-color: #6200ea;
        border: none;
        border-radius: 5px;
        padding: 0.65rem 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Input widgets text color fix */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div>div {
        color: #e0e0e0 !important;
        background-color: #1e1e1e !important;
    }

    /* Label styling for inputs */
    .stNumberInput>div>label,
    .stTextInput>div>label,
    .stSelectbox>div>label,
    /* generic catch-all for any label elements */
    label {
        font-weight: 600;
        font-size: 1.1rem;
        color: #ffffff !important;
        margin-bottom: 0.25rem;
    }

    /* Risk card style */
    .risk-card {
        background-color: #1e1e1e;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
    }

    /* Sidebar dark fixes */
    .css-1aumxhk {
        background-color: #181818;
    }
    .css-1d391kg {
        color: #e0e0e0;
    }

    /* Metrics card appearances */
    .stMetric {
        background-color: #333333 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
    }
    /* force all text inside metrics to be white */
    .stMetric * {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- HEADER SECTION / HERO ---- #
st.markdown(
    """
    <div class='hero'>
        <h1>🚨 ClaimWatch AI</h1>
        <p>Fraud Detection System</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<p class='sub-header'>Smart Insurance Claim Risk Analyzer</p>", unsafe_allow_html=True)
st.write("Enter claim details below to predict fraud risk and explore results in a clean, modern layout.")

# ---- SIDEBAR INFO ---- #
with st.sidebar:
    st.header("ℹ️ About ClaimWatch")
    st.markdown(
        """
    - **ClaimWatch AI** is a simple demo to estimate the likelihood of a fraudulent insurance claim.
    - Enter realistic information and click **Predict Fraud Risk** to see the result.
    - The system uses straightforward scoring rules, not a real ML model.
    """
    )
    st.markdown("---")
    st.markdown("💡 *Tip: Try different values to see how the risk changes.*")

# ---- INPUT FIELDS (columns) ---- #
col1, col2, col3 = st.columns(3)
with col1:
    claim_amount = st.number_input("Claim Amount (₹)", min_value=0, value=50000, step=1000)
    customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
with col2:
    num_previous_claims = st.number_input("Number of Previous Claims", min_value=0, value=0)
    days_since_last_claim = st.number_input("Days Since Last Claim", min_value=0, value=365)
with col3:
    policy_duration = st.number_input("Policy Duration (Years)", min_value=0, value=1)
    claim_type = st.selectbox("Claim Type", ["health", "vehicle"])

# ---- PREDICTION LOGIC ---- #
import plotly.express as px
import plotly.graph_objects as go

if st.button("Predict Fraud Risk"):
    # encode claim type
    claim_type_encoded = 0 if claim_type == "health" else 1

    input_data = pd.DataFrame([[
        claim_amount,
        customer_age,
        num_previous_claims,
        days_since_last_claim,
        policy_duration,
        claim_type_encoded
    ]], columns=[
        "claim_amount",
        "customer_age",
        "num_previous_claims",
        "days_since_last_claim",
        "policy_duration",
        "claim_type"
    ])

    # simple scoring rules
    risk_score = 0
    components = {}
    if claim_amount > 80000:
        risk_score += 2
        components["High Amount"] = 2
    else:
        components["High Amount"] = 0
    if num_previous_claims >= 3:
        risk_score += 2
        components["Previous Claims"] = 2
    else:
        components["Previous Claims"] = 0
    if days_since_last_claim < 30:
        risk_score += 2
        components["Recent Claim"] = 2
    else:
        components["Recent Claim"] = 0
    if policy_duration < 2:
        risk_score += 1
        components["Short Policy"] = 1
    else:
        components["Short Policy"] = 0
    if customer_age < 25:
        risk_score += 1
        components["Young Customer"] = 1
    else:
        components["Young Customer"] = 0

    # classify
    if risk_score <= 2:
        risk_level = "LOW RISK"
        probability = 20
        emoji = "✅"
        color_fn = st.success
    elif risk_score <= 5:
        risk_level = "MEDIUM RISK"
        probability = 55
        emoji = "⚠️"
        color_fn = st.warning
    else:
        risk_level = "HIGH RISK"
        probability = 85
        emoji = "🚨"
        color_fn = st.error

    # display metrics & charts
    with st.container():
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Risk Level", risk_level, f"{probability}%")
        mcol2.metric("Score", risk_score)
        mcol3.metric("Amount", f"₹{claim_amount:,}")

    # pie chart of components
    comp_df = pd.DataFrame({"component": list(components.keys()), "score": list(components.values())})
    fig = px.pie(comp_df, names="component", values="score",
                 title="🔍 Risk Factors Contribution",
                 color_discrete_sequence=px.colors.qualitative.Dark2)
    st.plotly_chart(fig, use_container_width=True)

    # gauge for probability
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#6200ea"}},
        title={'text': "Fraud Probability"}
    ))
    st.plotly_chart(gauge, use_container_width=True)

    # styled result card
    st.markdown(
        f"<div class='risk-card'><h2>{emoji} {risk_level}</h2><h3>Fraud Probability: {probability}%</h3></div>",
        unsafe_allow_html=True,
    )
    st.progress(probability)

    st.markdown("---")
    with st.expander("📊 Claim Data Used for Analysis"):
        st.dataframe(input_data)