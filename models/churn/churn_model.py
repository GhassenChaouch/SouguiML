import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


class ChurnModel:

    def prepare_data(self, df):

        df['Last_Purchase_Date'] = pd.to_datetime(df['Last_Purchase_Date'])

        max_date = df['Last_Purchase_Date'].max()

        # Recency
        df['Recency'] = (max_date - df['Last_Purchase_Date']).dt.days

        # CHURN LABEL
        df['Churn'] = np.where(df['Recency'] > 90, 1, 0)

        features = df[['Frequency', 'Total_Spent', 'Recency']]
        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        y = df['Churn']

        return X, y, df

    # -------------------------
    # LOGISTIC REGRESSION
    # -------------------------
    def logistic_model(self, X, y):

        model = LogisticRegression()
        model.fit(X, y)

        preds = model.predict(X)
        acc = accuracy_score(y, preds)

        return model, acc

    # -------------------------
    # RANDOM FOREST
    # -------------------------
    def random_forest(self, X, y):

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        preds = model.predict(X)
        acc = accuracy_score(y, preds)

        return model, acc

    # -------------------------
    # COMPARE
    # -------------------------
    def compare_models(self, X, y):

        _, acc1 = self.logistic_model(X, y)
        _, acc2 = self.random_forest(X, y)

        return {
            "Logistic_Accuracy": acc1,
            "RandomForest_Accuracy": acc2,
            "Best_Model": "RandomForest" if acc2 > acc1 else "LogisticRegression"
        }