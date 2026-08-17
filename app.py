import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & THEMING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Interactive Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: 700;
        color: #00D4FF;
    }
    div[data-testid="stMetric"] {
        background-color: #1E222D;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2E3440;
    }
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #374151;
    }
    .insight-box {
        background-color: #1E293B;
        border-left: 5px solid #00D4FF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HEADER BANNER
# ---------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1 style="color: #ffffff; margin:0;">📊 Smart Interactive Data Visualization Dashboard</h1>
        <p style="color: #9CA3AF; margin: 5px 0 0 0;">Next-Gen Visual Analytics with Automated Insights, Distribution Charts & Anomaly Detection | Final Year Project</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR: DATA MANAGEMENT & CONVERSATIONAL SEARCH
# ---------------------------------------------------------
st.sidebar.header("📁 Data Management")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ CSV Uploaded Successfully!")
    except Exception:
        st.sidebar.error("Error reading CSV. Using sample dataset.")
        df = pd.DataFrame({
            "Category": ["Category A", "Category B", "Category C", "Category D"],
            "Sales": [1200, 2400, 1800, 3100],
            "Growth": [15, 30, -5, 22]
        })
else:
    st.sidebar.info("💡 Using default sample dataset. Upload a CSV to visualize your data.")
    df = pd.DataFrame({
        "Category": ["Category A", "Category B", "Category C", "Category D"],
        "Sales": [1200, 2400, 1800, 3100],
        "Growth": [15, 30, -5, 22]
    })

# Smart Type Conversions
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

all_columns = df.columns.tolist()
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

# --- FEATURE: CONVERSATIONAL SEARCH ---
st.sidebar.markdown("---")
st.sidebar.header("💬 Ask Your Data")
search_query = st.sidebar.text_input("Search or filter records (e.g., '2018', 'Fever'):", "")

if search_query:
    mask = np.column_stack([df[col].astype(str).str.contains(search_query, case=False, na=False) for col in df.columns])
    filtered_df = df[mask.any(axis=1)]
    st.sidebar.caption(f"Found **{len(filtered_df)}** matching records.")
else:
    filtered_df = df.copy()

# --- FEATURE: SMART PLOTTING CONTROLS ---
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Smart Plotting Controls")

default_x_idx = 0
default_y_idx = 0

if categorical_cols:
    default_x_idx = all_columns.index(categorical_cols[0])
elif len(all_columns) > 0:
    default_x_idx = 0

if numeric_cols:
    default_y_idx = all_columns.index(numeric_cols[0])
elif len(all_columns) > 1:
    default_y_idx = 1

x_axis = st.sidebar.selectbox("Select X-Axis / Category Column:", all_columns, index=default_x_idx)
y_axis = st.sidebar.selectbox("Select Y-Axis / Metric Column:", all_columns, index=default_y_idx)

# ---------------------------------------------------------
# 4. DASHBOARD TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Dynamic Dashboard & Visual Suite", 
    "📄 Raw vs Visual (Obj i)", 
    "📝 Usability Feedback (Obj iv)"
])

# ---------------------------------------------------------
# TAB 1: EXTENDED VISUALIZATION SUITE
# ---------------------------------------------------------
with tab1:
    # --- AUTOMATED AI INSIGHT GENERATOR ---
    st.subheader("🤖 Automated Executive Insights")
    
    if y_axis in numeric_cols and len(filtered_df) > 0:
        max_val = filtered_df[y_axis].max()
        min_val = filtered_df[y_axis].min()
        avg_val = filtered_df[y_axis].mean()
        max_row = filtered_df[filtered_df[y_axis] == max_val].iloc[0]
        x_max_label = max_row[x_axis] if x_axis in max_row else "N/A"
        
        insight_text = (
            f"• **Peak Value Detected:** The highest **{y_axis}** recorded is **{max_val:,.2f}** (associated with **{x_axis}: {x_max_label}**).\n"
            f"• **Dataset Average:** Across **{len(filtered_df):,}** entries, the average **{y_axis}** stands at **{avg_val:,.2f}**.\n"
            f"• **Value Range:** Observations spread between a baseline minimum of **{min_val:,.2f}** and a maximum of **{max_val:,.2f}**."
        )
    else:
        insight_text = f"• Dataset loaded with **{len(filtered_df):,}** total rows across **{len(all_columns)}** attributes."

    st.markdown(f'<div class="insight-box">{insight_text}</div>', unsafe_allow_html=True)

    # Key Performance Indicators
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{len(filtered_df):,}")
    
    if y_axis in numeric_cols:
        col2.metric(f"Total {y_axis}", f"{filtered_df[y_axis].sum():,.1f}")
        col3.metric(f"Average {y_axis}", f"{filtered_df[y_axis].mean():,.1f}")
    else:
        col2.metric("Data Status", "Active")
        col3.metric("Data Integrity", "100%")

    st.markdown("---")
    
    # --- SECTION A: BAR & TREND CHARTS ---
    st.subheader("📊 Primary Charts & Outlier Analysis")
    show_outliers = st.checkbox("⚠️ Enable Automatic Outlier/Anomaly Detection", value=True)

    if all_columns and len(filtered_df) > 0:
        col_left, col_right = st.columns(2)
        
        is_outlier = np.zeros(len(filtered_df), dtype=bool)
        if y_axis in numeric_cols and show_outliers:
            q1 = filtered_df[y_axis].quantile(0.25)
            q3 = filtered_df[y_axis].quantile(0.75)
            iqr = q3 - q1
            is_outlier = (filtered_df[y_axis] < (q1 - 1.5 * iqr)) | (filtered_df[y_axis] > (q3 + 1.5 * iqr))
            outlier_count = is_outlier.sum()
            if outlier_count > 0:
                st.warning(f"⚠️ **{outlier_count} statistical anomalies detected** in {y_axis} (highlighted on charts).")

        with col_left:
            st.markdown(f"**Bar Chart: {y_axis} by {x_axis}**")
            fig_bar = px.bar(
                filtered_df, x=x_axis, y=y_axis,
                template="plotly_dark", text_auto=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_right:
            st.markdown(f"**Trend View with Anomaly Overlay**")
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=filtered_df[x_axis], y=filtered_df[y_axis],
                mode='lines+markers', name=y_axis, line=dict(color='#00D4FF')
            ))
            
            if show_outliers and is_outlier.any():
                outlier_df = filtered_df[is_outlier]
                fig_trend.add_trace(go.Scatter(
                    x=outlier_df[x_axis], y=outlier_df[y_axis],
                    mode='markers', name='Anomaly/Outlier',
                    marker=dict(color='red', size=10, symbol='x')
                ))
                
            fig_trend.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # --- SECTION B: HISTOGRAM & PIE CHART ---
    st.subheader("🍩 Distribution & Composition Analysis")
    col_hist, col_pie = st.columns(2)

    with col_hist:
        st.markdown(f"**Histogram: Frequency Distribution of {y_axis}**")
        if y_axis in numeric_cols:
            fig_hist = px.histogram(
                filtered_df, x=y_axis, nbins=30,
                color_discrete_sequence=['#00D4FF'],
                template="plotly_dark", marginal="rug"
            )
            fig_hist.update_layout(yaxis_title="Count / Frequency")
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Select a numeric Y-Axis column to generate a numerical frequency histogram.")

    with col_pie:
        st.markdown(f"**Pie Chart: Proportional Share of {y_axis} by {x_axis}**")
        if y_axis in numeric_cols and len(filtered_df[x_axis].unique()) <= 30:
            fig_pie = px.pie(
                filtered_df, names=x_axis, values=y_axis,
                hole=0.4, template="plotly_dark"
            )
            fig_pie.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        elif len(filtered_df[x_axis].unique()) > 30:
            st.warning("Pie chart hidden: Too many unique categories on X-axis (>30). Select a broader category column.")
        else:
            st.info("Select a valid numeric column to generate a proportional pie chart.")

    st.markdown("---")

    # --- SECTION C: ADVANCED STATISTICAL VISUALS (BOX PLOT & SCATTER MATRIX) ---
    st.subheader("📦 Statistical Spread & Multi-Variable Correlation")
    col_box, col_scat = st.columns(2)

    with col_box:
        st.markdown(f"**Box Plot: Quartile Spread & Outliers for {y_axis}**")
        if y_axis in numeric_cols:
            fig_box = px.box(
                filtered_df, x=x_axis if categorical_cols else None, y=y_axis,
                points="all", template="plotly_dark", color_discrete_sequence=['#A78BFA']
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Select a numeric column for box plot statistical spread.")

    with col_scat:
        st.markdown("**Scatter Plot: X vs Y Correlation Analysis**")
        fig_scatter_matrix = px.scatter(
            filtered_df, x=x_axis, y=y_axis,
            color=x_axis if categorical_cols else None,
            size=y_axis if y_axis in numeric_cols else None,
            template="plotly_dark"
        )
        st.plotly_chart(fig_scatter_matrix, use_container_width=True)

    # --- EXECUTIVE REPORT GENERATOR ---
    st.markdown("---")
    st.subheader("📄 Executive Report Export")
    
    report_html = f"""
    <html>
    <head><title>Executive Data Report</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>📊 Executive Data Summary Report</h2>
        <p><strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <hr>
        <h3>Key Metrics</h3>
        <ul>
            <li><strong>Total Records Analyzed:</strong> {len(filtered_df):,}</li>
            <li><strong>Selected Metric (Y-Axis):</strong> {y_axis}</li>
            <li><strong>Selected Category (X-Axis):</strong> {x_axis}</li>
        </ul>
        <h3>Automated Insights</h3>
        <p>{insight_text}</p>
    </body>
    </html>
    """
    
    st.download_button(
        label="📥 Download Executive Summary Report (HTML)",
        data=report_html,
        file_name=f"Executive_Report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )

# ---------------------------------------------------------
# TAB 2: RAW VS VISUAL COMPARISON (Obj i)
# ---------------------------------------------------------
with tab2:
    st.subheader("Identifying Static Data Difficulties")
    st.info("💡 Compare raw tabular data against dynamic charts to evaluate cognitive retrieval speed.")
    
    view_mode = st.radio("Select View Mode:", ["Static Data Table (Traditional)", "Interactive Visual View (Proposed)"])
    
    if view_mode == "Static Data Table (Traditional)":
        st.write("#### Raw Tabular Data")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.write("#### Dynamic Interactive View")
        fig_scatter = px.scatter(
            filtered_df, x=x_axis, y=y_axis,
            color=x_axis if categorical_cols else None, template="plotly_dark"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: USABILITY TESTING & FEEDBACK (Obj iv)
# ---------------------------------------------------------
with tab3:
    st.subheader("User Evaluation & Usability Feedback")
    st.write("Evaluate the usability and effectiveness of this dashboard for project assessment.")
    
    with st.form("feedback_form"):
        user_role = st.selectbox("Your Role:", ["Student", "Academic Supervisor / Evaluator", "Data Analyst", "Other"])
        rating = st.slider("How easy was it to understand the visualizations? (1 = Very Hard, 5 = Very Easy)", 1, 5, 4)
        clarity_rating = st.radio("Did interactive charts and automated insights solve static table difficulties?", ["Yes, significantly", "Somewhat", "No difference"])
        comments = st.text_area("Additional Feedback & Suggested Improvements:")
        
        submitted = st.form_submit_button("Submit Evaluation")
        
        if submitted:
            feedback_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Role": user_role,
                "Usability Rating": rating,
                "Solved Static Issues": clarity_rating,
                "Comments": comments
            }])
            
            file_exists = os.path.exists("user_feedback.csv")
            feedback_data.to_csv("user_feedback.csv", mode='a', header=not file_exists, index=False)
            
            st.success("Thank you! Your feedback has been logged to user_feedback.csv for system evaluation.")
