# import pandas as pd
# from sklearn.linear_model import LinearRegression


# class RevenueModel:

#     def __init__(self):
#         self.model = LinearRegression()

#     # -----------------------------
#     # PREPROCESSING
#     # -----------------------------
#     def prepare_data(self, df):
#         # Create proper date
#         df['Date'] = pd.to_datetime(
#             df['Annee'].astype(str) + '-' + df['Mois'].astype(str)
#         )

#         # Sort by time
#         df = df.sort_values('Date')

#         # Create time index (feature)
#         df['t'] = range(len(df))

#         return df

#     # -----------------------------
#     # TRAINING
#     # -----------------------------
#     def train(self, df):
#         X = df[['t']]
#         y = df['Total_Revenue']

#         self.model.fit(X, y)

#         return self.model

#     # -----------------------------
#     # PREDICTION (historical)
#     # -----------------------------
#     def predict(self, df):
#         X = df[['t']]
#         df['Prediction'] = self.model.predict(X)
#         return df

#     # -----------------------------
#     # FUTURE FORECAST
#     # -----------------------------
#     def forecast(self, df, periods=6):
#         future = pd.DataFrame({
#             't': range(len(df), len(df) + periods)
#         })

#         future['Prediction'] = self.model.predict(future)

#         return future
    
import pandas as pd
from prophet import Prophet


class RevenueModel:

    def __init__(self):
        # Prophet tuned for business forecasting
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )

    # -----------------------------
    # PREPROCESSING
    # -----------------------------
    def prepare_data(self, df):

        # Build proper datetime
        df['Date'] = pd.to_datetime(
            df['Annee'].astype(str) + '-' + df['Mois'].astype(str)
        )

        df = df.sort_values('Date')

        # Keep only needed columns
        df = df[['Date', 'Total_Revenue']]

        df.columns = ['ds', 'y']

        # IMPORTANT: aggregate in case of duplicates
        df = df.groupby('ds').sum().reset_index()

        return df

    # -----------------------------
    # TRAIN MODEL
    # -----------------------------
    def train(self, df):
        self.model.fit(df)

    # -----------------------------
    # HISTORICAL PREDICTIONS
    # -----------------------------
    def predict(self, df):

        forecast = self.model.predict(df)

        df['Prediction'] = forecast['yhat'].values

        return df

    # -----------------------------
    # FUTURE FORECAST
    # -----------------------------
    def forecast(self, df, periods=6):

        future = self.model.make_future_dataframe(
            periods=periods,
            freq='ME'   # Month End (FIXED)
        )

        forecast = self.model.predict(future)

        # Remove negative values (business safe)
        forecast['yhat'] = forecast['yhat'].clip(lower=0)

        return forecast[['ds', 'yhat']]