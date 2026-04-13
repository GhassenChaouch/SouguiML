from data.loader.sql_loader import load_data
from data.extract.product_queries import PRICE_SENSITIVITY_QUERY

from models.product_manager.price_sensitivity import (
    prepare_price_data,
    train_price_model,
    simulate_price_change
)


# =========================
# PRICE PIPELINE
# =========================
def run_price_sensitivity_pipeline():

    df = load_data(PRICE_SENSITIVITY_QUERY)

    df = prepare_price_data(df)

    model = train_price_model(df)

    return df, model


# =========================
# SIMULATION WRAPPER
# =========================
def run_price_simulation(model, current_price, competitor_price, change_pct):

    return simulate_price_change(
        model,
        current_price,
        competitor_price,
        change_pct
    )