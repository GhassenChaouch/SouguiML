from data.extract.revenue_queries import REVENUE_QUERY
from data.loader.sql_loader import load_data
from models.revenue.revenue_model import RevenueModel


def run_revenue_pipeline():
    df = load_data(REVENUE_QUERY)

    model = RevenueModel()

    df = model.prepare_data(df)
    model.train(df)

    df = model.predict(df)
    future = model.forecast(df)

    return df, future