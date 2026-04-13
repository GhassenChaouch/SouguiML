from data.extract.churn_queries import CHURN_QUERY
from data.loader.sql_loader import load_data
from models.churn.churn_model import ChurnModel


def run_churn_pipeline():

    df = load_data(CHURN_QUERY)

    model = ChurnModel()

    X, y, df_clean = model.prepare_data(df)

    comparison = model.compare_models(X, y)

    df_clean['Churn_Risk'] = y

    return df_clean, comparison