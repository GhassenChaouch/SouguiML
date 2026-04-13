import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


# =========================
# STEP 1: BUILD BASKET
# =========================
def prepare_basket(df):

    # Ensure clean types (VERY IMPORTANT)
    df = df.copy()
    df = df.dropna(subset=["Transaction_ID", "Product_ID"])

    # Pivot table (transaction x product matrix)
    basket = (
        df.groupby(["Transaction_ID", "Product_ID"])["Quantite"]
        .sum()
        .unstack(fill_value=0)
    )

    # Convert to binary (0/1)
    basket = basket.astype(bool).astype(int)

    return basket


# =========================
# STEP 2: RUN MODEL
# =========================
def run_market_basket(df):

    basket = prepare_basket(df)

    # Safety check (prevents Streamlit crash)
    if basket.shape[0] == 0 or basket.shape[1] == 0:
        return pd.DataFrame(columns=[
            "antecedents", "consequents", "support", "confidence", "lift"
        ])

    # Frequent itemsets
    frequent_items = apriori(
        basket,
        min_support=0.02,
        use_colnames=True
    )

    # If no patterns found
    if frequent_items.empty:
        return pd.DataFrame(columns=[
            "antecedents", "consequents", "support", "confidence", "lift"
        ])

    # Association rules
    rules = association_rules(
        frequent_items,
        metric="confidence",
        min_threshold=0.3
    )

    # Final output safety
    if rules.empty:
        return rules

    return rules[[
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]]