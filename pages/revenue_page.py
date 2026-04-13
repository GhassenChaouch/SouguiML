import streamlit as st
from services.revenue_service import run_revenue_pipeline


def show_revenue_page():

    st.title("📊 Revenue Forecast Dashboard")

    # -------------------------
    # LOAD DATA (CACHED)
    # -------------------------
    @st.cache_data
    def load_data():
        return run_revenue_pipeline()

    df, future = load_data()

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------
    st.sidebar.header("🔎 Revenue Filters")

    # Safety check (avoid crash if empty df)
    if df.empty:
        st.warning("No data available")
        return

    years = sorted(df["ds"].dt.year.unique())
    selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)

    type_filter = st.sidebar.selectbox(
        "Business Type",
        ["All", "B2C", "B2B"]
    )

    # -------------------------
    # APPLY FILTERS
    # -------------------------
    filtered_df = df.copy()

    # Year filter
    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["ds"].dt.year == selected_year
        ]

    # Type filter (only if column exists)
    if type_filter != "All" and "Type" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["Type"] == type_filter
        ]

    # -------------------------
    # DASHBOARD
    # -------------------------
    st.subheader("📈 Historical Revenue vs Prediction")
    st.dataframe(filtered_df)

    st.line_chart(
        filtered_df.set_index("ds")[["y", "Prediction"]]
    )

    st.subheader("🔮 Future Forecast")
    st.dataframe(future)

    st.line_chart(
        future.set_index("ds")[["yhat"]]
    )