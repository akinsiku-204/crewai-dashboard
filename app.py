import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="PixelPro Digital Dashboard", page_icon="🔮", layout="wide")

# --- AUTHENTICATION & LOGIN UI ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Custom CSS to replicate the purple card UI
    st.markdown("""
        <style>
        /* Background Styling */
        .stApp {
            background-color: #f3f0ff;
        }
        
        /* Card Container */
        div[data-testid="stForm"] {
            background: linear-gradient(180deg, #A78BFA 0%, #818CF8 50%, #60A5FA 100%);
            border-radius: 28px;
            padding: 35px 30px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border: none;
            max-width: 420px;
            margin: auto;
        }
        
        /* Heading and Subtext */
        .login-header {
            color: white;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 26px;
            margin-bottom: 2px;
        }
        .login-sub {
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 18px;
            margin-bottom: 25px;
        }

        /* Input Fields */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 12px !important;
            color: white !important;
        }
        div[data-baseweb="input"] input {
            color: white !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: rgba(255, 255, 255, 0.75) !important;
        }
        
        /* Login Button */
        div[data-testid="stForm"] button {
            background-color: white !important;
            color: #4F46E5 !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border: none !important;
            width: 100% !important;
            padding: 10px !important;
            margin-top: 15px !important;
        }
        div[data-testid="stForm"] button:hover {
            background-color: #f8fafc !important;
            color: #3730A3 !important;
        }

        /* Divider & Links */
        .divider-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 13px;
            margin: 20px 0 15px 0;
        }
        .signup-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            font-size: 13px;
            margin-top: 20px;
        }
        .signup-text a {
            color: white;
            font-weight: bold;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Centered Card Layout
    _, col2, _ = st.columns([1, 1.2, 1])

    with col2:
        with st.form("login_form"):
            # Logo & Greeting
            st.markdown("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <div style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 28px;">🔮</div>
                    <div style="color: white; font-weight: bold; font-size: 16px; margin-top: 5px;">PixelPro Digital</div>
                </div>
                <div class="login-header">Welcome,</div>
                <div class="login-sub">Glad to see you!</div>
            """, unsafe_allow_html=True)

            username = st.text_input("Email / Username", placeholder="Email Address", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

            st.markdown("<div style='text-align: right; margin-top:-10px;'><a href='#' style='color: rgba(255,255,255,0.8); font-size: 12px; text-decoration: none;'>Forgot Password?</a></div>", unsafe_allow_html=True)

            submit = st.form_submit_button("Login")

            st.markdown("""
                <div class="divider-text">─── Or Login with ───</div>
                <div style="display: flex; gap: 10px; justify-content: center;">
                    <button type="button" style="flex:1; background:white; border:none; border-radius:10px; padding:8px; font-weight:bold; cursor:pointer;">G</button>
                    <button type="button" style="flex:1; background:white; border:none; border-radius:10px; padding:8px; color:#1877F2; font-weight:bold; cursor:pointer;">f</button>
                </div>
                <div class="signup-text">Don't have an account? <a href="#">Sign Up Now</a></div>
            """, unsafe_allow_html=True)

            if submit:
                # Default credentials: admin / supervisor2026
                if username == "admin" and password == "supervisor2026":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect Username or Password")

    return False

if not check_password():
    st.stop()

# --- SIDEBAR LOGOUT BUTTON ---
st.sidebar.markdown("### 👤 User Session")
st.sidebar.write("Logged in as: **admin**")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.rerun()

# --- MAIN DASHBOARD CODE STARTS BELOW ---
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.title("📊 PixelPro Digital Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("insurance.csv")
    except FileNotFoundError:
        df = pd.DataFrame({
            "age": [19, 18, 28, 33, 32],
            "sex": ["female", "male", "male", "male", "male"],
            "bmi": [27.9, 33.77, 33.0, 22.705, 28.88],
            "children": [0, 1, 3, 0, 0],
            "smoker": ["yes", "no", "no", "no", "no"],
            "region": ["southwest", "southeast", "southeast", "northwest", "northwest"],
            "charges": [16884.92, 1725.55, 4449.46, 21984.47, 3866.86]
        })
    return df

df = load_data()

# Tabs Interface
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualizations", "🔍 Outliers", "📝 Executive Report", "⭐ Evaluation Form"])

with tab1:
    st.subheader("Interactive Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        metric = st.selectbox("Select Metric to Plot", ["age", "bmi", "charges"])
        fig_hist = px.histogram(df, x=metric, title=f"Distribution of {metric.upper()}")
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        cat_var = st.selectbox("Select Categorical Variable", ["sex", "smoker", "region"])
        fig_bar = px.bar(df, x=cat_var, y="charges", color=cat_var, title=f"Charges by {cat_var.upper()}")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    fig_scatter_matrix = px.scatter_matrix(df, dimensions=["age", "bmi", "charges"], color="smoker")
    st.plotly_chart(fig_scatter_matrix, use_container_width=True)

with tab2:
    st.subheader("IQR Outlier Detection")
    num_col = st.selectbox("Select Numerical Column for Outlier Analysis", ["age", "bmi", "charges"])
    Q1 = df[num_col].quantile(0.25)
    Q3 = df[num_col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[num_col] < lower_bound) | (df[num_col] > upper_bound)]
    st.write(f"**Identified {len(outliers)} outliers in `{num_col}` (IQR threshold: [{lower_bound:.2f}, {upper_bound:.2f}])**")
    st.dataframe(outliers)

with tab3:
    st.subheader("📄 Executive Data Summary Report")
    report_html = f"""
    <html>
    <head><title>Executive Data Report</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>📊 Executive Data Summary Report</h2>
        <p><strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <hr>
        <h3>Key Metrics</h3>
        <ul>
            <li>Total Records: {len(df)}</li>
            <li>Average Age: {df['age'].mean():.1f} years</li>
            <li>Average BMI: {df['bmi'].mean():.2f}</li>
            <li>Average Charges: ${df['charges'].mean():,.2f}</li>
        </ul>
    </body>
    </html>
    """
    st.download_button("📥 Download Executive Report", data=report_html, file_name="executive_report.html", mime="text/html")

with tab4:
    st.subheader("⭐ System Usability Evaluation Form")
    with st.form("eval_form"):
        role = st.selectbox("Evaluator Role", ["Supervisor", "Student", "External Evaluator"])
        ease = st.slider("Ease of Use (1-5)", 1, 5, 5)
        resp = st.slider("System Responsiveness (1-5)", 1, 5, 5)
        util = st.slider("Feature Utility (1-5)", 1, 5, 5)
        comments = st.text_area("Feedback Comments")
        
        if st.form_submit_button("Submit Feedback"):
            new_data = pd.DataFrame([{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "evaluator_role": role,
                "ease_of_use": ease,
                "responsiveness": resp,
                "feature_utility": util,
                "comments": comments
            }])
            try:
                existing = pd.read_csv("user_feedback.csv")
                updated = pd.concat([existing, new_data], ignore_index=True)
            except FileNotFoundError:
                updated = new_data
            updated.to_csv("user_feedback.csv", index=False)
            st.success("✅ Feedback saved successfully to `user_feedback.csv`!")
