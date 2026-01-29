import duckdb
import os
from silver import setup_silver_layer

def setup_gold_layer():
    """
    Connects to DuckDB, reads from the silver layer,
    and creates aggregated features for the gold table.
    """
    # Ensure the silver layer exists before proceeding
    setup_silver_layer()

    db_path = os.path.join('..', 'data', 'fraud_detection.duckdb')
    con = duckdb.connect(database=db_path, read_only=False)

    # Create schema for gold data
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;")

    print("Creating aggregated features for the gold layer...")

    # Create the gold table with aggregated features
    con.execute("""
        CREATE OR REPLACE TABLE gold.gold_transactions AS
        SELECT
            *,
            -- Average transaction amount for the merchant
            AVG(amt) OVER (PARTITION BY merchant) AS avg_merch_spend,
            -- Lag feature: amount of the previous transaction for the card
            LAG(amt, 1, 0) OVER (PARTITION BY cc_num ORDER BY trans_date_time) AS prev_trans_amt,
            -- Lead feature: amount of the next transaction for the card
            LEAD(amt, 1, 0) OVER (PARTITION BY cc_num ORDER BY trans_date_time) AS next_trans_amt
        FROM silver.silver_transactions;
    """)

    print("Gold layer setup complete.")

    # Verify the new columns in the gold table
    print("Columns in gold.gold_transactions:")
    print(con.execute("DESCRIBE gold.gold_transactions;").fetchall())

    record_count = con.execute("SELECT COUNT(*) FROM gold.gold_transactions;").fetchone()[0]
    print(f"Total records in gold_transactions: {record_count}")

    con.close()

if __name__ == "__main__":
    # For direct execution, this will now run the full pipeline up to gold
    print("Setting up gold layer (which includes bronze and silver)...")
    setup_gold_layer()
    print("Gold layer setup finished.")