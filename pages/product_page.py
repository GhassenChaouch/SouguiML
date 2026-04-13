import streamlit as st
import pandas as pd

from services.product_service import (
    run_abc_xyz_pipeline,
    run_market_basket_pipeline
)

from services.price_service import (
    run_price_sensitivity_pipeline,
    run_price_simulation
)


# =========================
# PAGE FUNCTION
# =========================
def show_product_page():

    st.title("📦 Product Intelligence Dashboard")

    # =========================
    # INIT STATES
    # =========================
    if "abc_loaded" not in st.session_state:
        st.session_state.abc_loaded = False

    if "basket_loaded" not in st.session_state:
        st.session_state.basket_loaded = False

    if "price_loaded" not in st.session_state:
        st.session_state.price_loaded = False

    # =========================
    # ABC / XYZ
    # =========================
    if st.button("Run ABC / XYZ Segmentation"):
        df = run_abc_xyz_pipeline()
        st.session_state.abc_df = df
        st.session_state.abc_loaded = True

    if st.session_state.abc_loaded:
        df = st.session_state.abc_df

        st.subheader("📊 Raw Segmentation Data")
        st.dataframe(df)

        st.subheader("📈 ABC Distribution")
        st.bar_chart(df["ABC"].value_counts().sort_index())

        st.subheader("📉 XYZ Distribution")
        st.bar_chart(df["XYZ"].value_counts().sort_index())

        st.subheader("📋 Summary")
        summary = df.groupby(["ABC", "XYZ"]).size().reset_index(name="Count")
        st.dataframe(summary)

    # =========================
    # MARKET BASKET
    # =========================
    st.divider()
    st.subheader("🛒 Market Basket Analysis")

    if st.button("Run Market Basket Rules"):
        rules = run_market_basket_pipeline()
        st.session_state.basket_rules = rules
        st.session_state.basket_loaded = True

    if st.session_state.basket_loaded:
        rules = st.session_state.basket_rules

        st.dataframe(rules)

        # OPTIONAL CLEAN VISUAL
        if rules is not None and not rules.empty:

            df = rules.copy()

            df["antecedents"] = df["antecedents"].apply(
                lambda x: ", ".join(map(str, list(x)))
            )
            df["consequents"] = df["consequents"].apply(
                lambda x: ", ".join(map(str, list(x)))
            )

            df["rule"] = df["antecedents"] + " → " + df["consequents"]

            st.subheader("🔥 Top Rules (Confidence)")

            top_rules = df.sort_values("confidence", ascending=False).head(10)

            st.bar_chart(top_rules.set_index("rule")["confidence"])

    # =========================
    # PRICE SENSITIVITY
    # =========================
    st.divider()
    st.subheader("💰 Price Sensitivity")

    if st.button("Run Price Model"):
        df, model = run_price_sensitivity_pipeline()

        st.session_state.price_df = df
        st.session_state.price_model = model
        st.session_state.price_loaded = True

    if st.session_state.price_loaded:

        df = st.session_state.price_df
        model = st.session_state.price_model

        st.subheader("📊 Data Sample")
        st.dataframe(df.head())

        st.subheader("📉 Simulator")

        current_price = st.number_input("Your Price", value=100.0)
        competitor_price = st.number_input("Competitor Price", value=110.0)
        change_pct = st.slider("Price Change (%)", -0.5, 0.5, 0.1)

        if st.button("Simulate Impact"):

            result = run_price_simulation(
                model,
                current_price,
                competitor_price,
                change_pct
            )

            st.success("Result")
            st.write("New Price:", result["new_price"])
            st.write("Predicted Demand:", result["predicted_demand"])