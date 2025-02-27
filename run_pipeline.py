from src.extract import extract
from src.load import load
from src.transform import run_queries, QueryEnum
from src import config
from sqlalchemy import create_engine
import traceback
import sys
from datetime import datetime
import pandas as pd
from src.plots import (
    plot_freight_value_weight_relationship,
    plot_global_amount_order_status,
    plot_real_vs_predicted_delivered_time,
    plot_revenue_by_month_year,
    plot_revenue_per_state,
    plot_top_10_least_revenue_categories,
    plot_top_10_revenue_categories,
    plot_top_10_revenue_categories_ammount,
    plot_delivery_date_difference,
    plot_order_amount_per_day_with_holidays,
)

def setup_logging():
    log_file = f"pipeline_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    sys.stdout = open(log_file, 'w')
    sys.stderr = sys.stdout
    return log_file

def main():
    log_file = setup_logging()
    try:
        print("1. Testing CSV reading...")
        test_file = "dataset/olist_customers_dataset.csv"
        df = pd.read_csv(test_file)
        print(f"Successfully read test file {test_file}")
        print(f"Shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head())
        
        print("\n2. Extracting all data...")
        data_frames = extract(
            csv_folder=config.DATASET_ROOT_PATH,
            csv_table_mapping=config.get_csv_to_table_mapping(),
            public_holidays_url=config.PUBLIC_HOLIDAYS_URL
        )
        print("Data extraction completed successfully")
        print(f"Number of dataframes: {len(data_frames)}")
        for name, df in data_frames.items():
            print(f"{name}: {df.shape} rows")
        
        print("\n3. Loading data...")
        database = create_engine(f"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}")
        load(data_frames=data_frames, database=database)
        print("Data loading completed successfully")
        
        print("\n4. Running queries...")
        query_results = run_queries(database=database)
        print("Queries completed successfully")
        print(f"Number of query results: {len(query_results)}")
        
        print("\n5. Generating plots...")
        # Generate all plots
        plot_revenue_by_month_year(query_results[QueryEnum.REVENUE_BY_MONTH_YEAR.value], 2017)
        plot_top_10_revenue_categories(query_results[QueryEnum.TOP_10_REVENUE_CATEGORIES.value])
        plot_top_10_least_revenue_categories(query_results[QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value])
        plot_revenue_per_state(query_results[QueryEnum.REVENUE_PER_STATE.value])
        plot_freight_value_weight_relationship(query_results[QueryEnum.FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value])
        plot_global_amount_order_status(query_results[QueryEnum.GLOBAL_AMOUNT_ORDER_STATUS.value])
        plot_delivery_date_difference(query_results[QueryEnum.DELIVERY_DATE_DIFFERECE.value])
        plot_real_vs_predicted_delivered_time(query_results[QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value])
        plot_order_amount_per_day_with_holidays(query_results[QueryEnum.ORDER_AMOUNT_PER_DAY.value])
        print("Plots generated successfully")
        
        print("\nPipeline completed successfully!")
    except Exception as e:
        print("\nError in pipeline execution:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        raise
    finally:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(f"Log file created at: {log_file}")

if __name__ == "__main__":
    main()
