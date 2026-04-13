from data.loader.sql_loader import load_data
from data.extract.product_queries import ABC_XYZ_QUERY, MARKET_BASKET_QUERY

from models.product_manager.abc_xyz import abc_xyz_analysis
from models.product_manager.market_basket import run_market_basket


# ===============================
# ABC / XYZ PIPELINE
# ===============================
def run_abc_xyz_pipeline():
    df = load_data(ABC_XYZ_QUERY)

    # DEBUG (optional, remove later)
    print("ABC XYZ DF:")
    print(df.head())

    result = abc_xyz_analysis(df)

    return result


# ===============================
# MARKET BASKET PIPELINE
# ===============================
def run_market_basket_pipeline():
    df = load_data(MARKET_BASKET_QUERY)

    print("Basket DF:")
    print(df.head())

    rules = run_market_basket(df)

    return rules