from services.revenue_service import run_revenue_pipeline

if __name__ == "__main__":
    df, future = run_revenue_pipeline()

    print("=== HISTORICAL DATA ===")
    print(df.tail())

    print("\n=== FUTURE PREDICTIONS ===")
    print(future)