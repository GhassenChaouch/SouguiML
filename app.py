import streamlit as st

st.set_page_config(page_title="Sougui BI Dashboard", layout="wide")

st.sidebar.title("📊 Sougui BI Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Revenue", "Product Manager", "Segmentation", "Churn"]
)

# -------------------------
# ROUTING
# -------------------------
if page == "Revenue":
    from pages.revenue_page import show_revenue_page
    show_revenue_page()

elif page == "Product Manager":
    from pages.product_page import show_product_page
    show_product_page()

elif page == "Segmentation":
    from pages.segmentation_page import show_segmentation_page
    show_segmentation_page()

elif page == "Churn":
    from pages.churn_page import show_churn_page
    show_churn_page()