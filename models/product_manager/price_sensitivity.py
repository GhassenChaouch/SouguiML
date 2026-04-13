import pandas as pd
from sklearn.linear_model import LinearRegression


def prepare_price_data(df):
    df = df.copy()

    # Fill missing competitor prices
    df["Competitor_Price"] = df[["Competitor_Price_1", "Competitor_Price_2"]].mean(axis=1)

    # Drop rows with missing values
    df = df.dropna(subset=["Prix_du_produit", "Competitor_Price", "Quantite"])

    return df


def train_price_model(df):
    X = df[["Prix_du_produit", "Competitor_Price"]]
    y = df["Quantite"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_demand(model, your_price, competitor_price):
    prediction = model.predict([[your_price, competitor_price]])
    return prediction[0]


def simulate_price_change(model, current_price, competitor_price, change_pct):
    new_price = current_price * (1 + change_pct)
    predicted = model.predict([[new_price, competitor_price]])

    return {
        "new_price": new_price,
        "predicted_demand": predicted[0]
    }