import streamlit as st
import pandas as pd
from services.churn_service import run_churn_pipeline


def show_churn_page():

    st.title("⚠️ Customer Churn Prediction Dashboard")

    # -------------------------
    # LOAD DATA
    # -------------------------
    @st.cache_data
    def load_data():
        return run_churn_pipeline()

    df, comparison = load_data()

    # -------------------------
    # MODEL PERFORMANCE
    # -------------------------
    st.subheader("📊 Model Comparison")

    col1, col2, col3 = st.columns(3)

    col1.metric("Logistic Regression", round(comparison["Logistic_Accuracy"], 3))
    col2.metric("Random Forest", round(comparison["RandomForest_Accuracy"], 3))
    col3.metric("Best Model", comparison["Best_Model"])

    # -------------------------
    # RISK FILTER
    # -------------------------
    st.subheader("🎯 Customer Risk Segmentation")

    risk_filter = st.selectbox(
        "Select Risk Level",
        ["All", "High Risk", "Safe"]
    )

    filtered_df = df.copy()

    # High risk = churn = 1
    if risk_filter == "High Risk":
        filtered_df = filtered_df[filtered_df["Churn_Risk"] == 1]

    elif risk_filter == "Safe":
        filtered_df = filtered_df[filtered_df["Churn_Risk"] == 0]

    # -------------------------
    # RISK DISTRIBUTION
    # -------------------------
    st.subheader("📉 Churn Distribution")

    churn_counts = df["Churn_Risk"].value_counts()

    st.bar_chart(churn_counts)

    # -------------------------
    # KPI METRICS
    # -------------------------
    st.subheader("📌 Key Insights")

    total_clients = len(df)
    churned = df["Churn_Risk"].sum()
    churn_rate = churned / total_clients * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", total_clients)
    col2.metric("Churned Customers", churned)
    col3.metric("Churn Rate %", round(churn_rate, 2))

    # -------------------------
    # CUSTOMER TABLE
    # -------------------------
    st.subheader("📋 Customer Risk Table")

    st.dataframe(
        filtered_df[[
            "Client_Key",
            "Frequency",
            "Total_Spent",
            "Recency",
            "Churn_Risk"
        ]].sort_values(by="Churn_Risk", ascending=False)
    )

    # -------------------------
    # BUSINESS INTERPRETATION
    # -------------------------
    st.subheader("🧠 Business Insight")

    st.info("""
    🔴 High Risk customers = likely to stop buying soon  
    🟢 Safe customers = active and loyal  
    🎯 Use this to target discounts, retention campaigns, and VIP offers
    """)