import streamlit as st
from services.segmentation_service import run_segmentation_pipeline


def show_segmentation_page():

    st.title("👥 Customer Segmentation Dashboard")

    if st.button("Run Segmentation"):

        df, comparison = run_segmentation_pipeline()

        # -------------------------
        # METRICS
        # -------------------------
        st.subheader("📊 Model Comparison")

        col1, col2, col3 = st.columns(3)

        col1.metric("KMeans Score", round(comparison["KMeans_Silhouette"], 3))
        col2.metric("DBSCAN Score", round(comparison["DBSCAN_Silhouette"], 3))
        col3.metric("Best Model", comparison["Best_Model"])

        # -------------------------
        # BUSINESS LABELS (KMEANS)
        # -------------------------
        st.subheader("🧠 Customer Segments (Business View)")

        # Create readable labels based on clusters
        df["Segment"] = df["KMeans_Cluster"]

        # Simple interpretation (you can refine later)
        segment_map = {}

        for cluster in df["KMeans_Cluster"].unique():
            avg_spent = df[df["KMeans_Cluster"] == cluster]["Total_Spent"].mean()

            if avg_spent > df["Total_Spent"].quantile(0.75):
                segment_map[cluster] = "VIP Customers 🔥"
            elif avg_spent > df["Total_Spent"].quantile(0.40):
                segment_map[cluster] = "Regular Customers 🟡"
            else:
                segment_map[cluster] = "Low Value Customers 🔴"

        df["Segment_Label"] = df["KMeans_Cluster"].map(segment_map)

        # -------------------------
        # SHOW SEGMENT COUNTS
        # -------------------------
        st.subheader("📦 Segment Distribution")

        st.dataframe(df["Segment_Label"].value_counts())

        st.bar_chart(df["Segment_Label"].value_counts())

        # -------------------------
        # VISUALIZATION 1 (KMEANS)
        # -------------------------
        st.subheader("🔵 KMeans Segmentation")

        st.scatter_chart(
            df,
            x="Total_Spent",
            y="Frequency",
            color="KMeans_Cluster"
        )

        # -------------------------
        # VISUALIZATION 2 (DBSCAN)
        # -------------------------
        st.subheader("🟢 DBSCAN Segmentation")

        st.scatter_chart(
            df,
            x="Total_Spent",
            y="Frequency",
            color="DBSCAN_Cluster"
        )

        # -------------------------
        # FINAL TABLE
        # -------------------------
        st.subheader("📋 Full Customer View")

        st.dataframe(df[[
            "Client_Key",
            "Total_Spent",
            "Frequency",
            "KMeans_Cluster",
            "Segment_Label"
        ]])