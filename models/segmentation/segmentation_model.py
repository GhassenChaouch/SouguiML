import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class SegmentationModel:

    # -------------------------
    # PREPARE FEATURES
    # -------------------------
    def prepare_data(self, df):

        df['Last_Purchase_Date'] = pd.to_datetime(df['Last_Purchase_Date'])

        # Recency (days since last purchase)
        max_date = df['Last_Purchase_Date'].max()
        df['Recency'] = (max_date - df['Last_Purchase_Date']).dt.days

        df['Avg_Order_Value'] = df['Total_Spent'] / df['Frequency']

        features = df[['Frequency', 'Total_Spent', 'Recency', 'Avg_Order_Value']]

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        return df, scaled_features

    # -------------------------
    # KMEANS
    # -------------------------
    def kmeans_model(self, X, k=4):

        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(X)

        score = silhouette_score(X, labels)

        return labels, score

    # -------------------------
    # DBSCAN
    # -------------------------
    def dbscan_model(self, X):

        model = DBSCAN(eps=0.5, min_samples=5)
        labels = model.fit_predict(X)

        # DBSCAN may produce noise (-1)
        try:
            score = silhouette_score(X, labels)
        except:
            score = -1

        return labels, score

    # -------------------------
    # ELBOW METHOD (KMEANS)
    # -------------------------
    def elbow_analysis(self, X):

        inertia = []
        K = range(2, 10)

        for k in K:
            model = KMeans(n_clusters=k, random_state=42)
            model.fit(X)
            inertia.append(model.inertia_)

        return K, inertia

    # -------------------------
    # COMPARE MODELS
    # -------------------------
    def compare_models(self, X):

        k_labels, k_score = self.kmeans_model(X)
        d_labels, d_score = self.dbscan_model(X)

        return {
            "kmeans": k_score,
            "dbscan": d_score,
            "best": "kmeans" if k_score > d_score else "dbscan"
        }