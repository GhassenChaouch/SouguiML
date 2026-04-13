from data.extract.segmentation_queries import SEGMENTATION_QUERY
from data.loader.sql_loader import load_data
from models.segmentation.segmentation_model import SegmentationModel


def run_segmentation_pipeline():

    df = load_data(SEGMENTATION_QUERY)

    model = SegmentationModel()

    df_clean, X = model.prepare_data(df)

    # KMEANS
    k_labels, k_score = model.kmeans_model(X)

    # DBSCAN
    d_labels, d_score = model.dbscan_model(X)

    df_clean['KMeans_Cluster'] = k_labels
    df_clean['DBSCAN_Cluster'] = d_labels

    comparison = {
        "KMeans_Silhouette": k_score,
        "DBSCAN_Silhouette": d_score,
        "Best_Model": "KMeans" if k_score > d_score else "DBSCAN"
    }

    return df_clean, comparison