import pandas as pd
import numpy as np


def abc_xyz_analysis(df):
    # ======================
    # ABC CLASS (Revenue)
    # ======================
    product_revenue = df.groupby("Product_ID")["Revenue"].sum().reset_index()
    product_revenue = product_revenue.sort_values("Revenue", ascending=False)

    total_revenue = product_revenue["Revenue"].sum()
    product_revenue["cum_pct"] = product_revenue["Revenue"].cumsum() / total_revenue

    def abc_class(x):
        if x <= 0.8:
            return "A"
        elif x <= 0.95:
            return "B"
        else:
            return "C"

    product_revenue["ABC"] = product_revenue["cum_pct"].apply(abc_class)

    # ======================
    # XYZ CLASS (Volatility)
    # ======================
    df["Full_Date"] = pd.to_datetime(df["Full_Date"])
    df["Month"] = df["Full_Date"].dt.to_period("M")

    pivot = df.pivot_table(
        index="Product_ID",
        columns="Month",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    cv = pivot.std(axis=1) / (pivot.mean(axis=1) + 1e-9)

    def xyz_class(x):
        if x <= 0.5:
            return "X"
        elif x <= 1.0:
            return "Y"
        else:
            return "Z"

    xyz = cv.reset_index()
    xyz.columns = ["Product_ID", "CV"]
    xyz["XYZ"] = xyz["CV"].apply(xyz_class)

    # ======================
    # FINAL MERGE
    # ======================
    final = product_revenue.merge(xyz, on="Product_ID")

    return final