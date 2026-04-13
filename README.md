📊 Sougui BI Dashboard (SQL Server + ML + Streamlit)
An end-to-end Business Intelligence & Machine Learning platform connected to a SQL Server Data Warehouse.
🚀 Features
Revenue Forecasting (Prophet + Linear Regression)
Product Intelligence (ABC/XYZ, Market Basket)
Price Sensitivity Modeling
Demand Prediction (Linear Regression vs XGBoost)
Customer Segmentation (KMeans / DBSCAN)
Churn Analysis
Chatbot Assistant
🏗️ Tech Stack
Python
SQL Server
Streamlit
Scikit-learn
XGBoost
Prophet
Pandas / NumPy
▶️ Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
📁 Structure
app.py → main entry
pages/ → dashboards
services/ → pipelines
models/ → ML models
data/ → SQL queries + loader
🧠 ML Models
Prophet → forecasting
XGBoost → demand prediction
Linear Regression → baseline
KMeans / DBSCAN → segmentation
📌 Author
Sougui BI Project
