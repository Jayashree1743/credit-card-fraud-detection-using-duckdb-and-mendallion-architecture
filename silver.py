import duckdb
import os
from bronze import setup_bronze_layer

def setup_silver_layer():
    """
    Connects to DuckDB, reads from the bronze layer,
    and applies transformations to create the silver table.
    """
    # Ensure the bronze layer exists before proceeding
    setup_bronze_layer()

    db_path = os.path.join('..', 'data', 'fraud_detection.duckdb')
    con = duckdb.connect(database=db_path, read_only=False)

    # Create schema for silver data
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    print("Transforming data for the silver layer...")

    # Perform transformations and create the silver table
    con.execute("""
        CREATE OR REPLACE TABLE silver.silver_transactions AS
        SELECT
            *,
            -- The column is already a timestamp, so just alias it
            trans_date_trans_time AS trans_date_time,
            -- Calculate age of the cardholder at the time of transaction
            date_part('year', trans_date_trans_time) - date_part('year', dob) AS age,
            -- Extract hour of day from transaction time
            date_part('hour', trans_date_trans_time) AS trans_hour
        FROM bronze.bronze_transactions;
    """)

    print("Silver layer setup complete.")

    # Verify the new columns in the silver table
    print("Columns in silver.silver_transactions:")
    print(con.execute("DESCRIBE silver.silver_transactions;").fetchall())

    record_count = con.execute("SELECT COUNT(*) FROM silver.silver_transactions;").fetchone()[0]
    print(f"Total records in silver_transactions: {record_count}")


    con.close()

if __name__ == "__main__":
    # For direct execution, this will now run the full pipeline up to silver
    print("Setting up silver layer (which includes bronze)...")
    setup_silver_layer()
    print("Silver layer setup finished.")