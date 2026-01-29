import duckdb
import os

def setup_bronze_layer():
    """
    Connects to DuckDB, creates the bronze_transactions table,
    and ingests data from the CSV files.
    """
    db_path = os.path.join('..', 'data', 'fraud_detection.duckdb')
    con = duckdb.connect(database=db_path, read_only=False)

    # Create schema for raw data
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;")

    # Create bronze table from CSV files
    # The read_csv_auto function will infer schemas and combine files.
    # Using glob to read both train and test data.
    train_file = os.path.join('..', 'data', 'fraudTrain.csv')
    test_file = os.path.join('..', 'data', 'fraudTest.csv')

    # It's better to load them separately and then combine if needed,
    # but for simplicity in bronze, we can create two tables or load into one.
    # Let's load them into one table with an indicator of the source if needed.
    # For now, we just load the training data. We can add test data later.

    print("Ingesting data into bronze_transactions table...")
    con.execute(f"""
        CREATE OR REPLACE TABLE bronze.bronze_transactions AS
        SELECT * FROM read_csv_auto('{train_file}');
    """)

    # To add the test data, you could use an INSERT statement:
    con.execute(f"""
        INSERT INTO bronze.bronze_transactions
        SELECT * FROM read_csv_auto('{test_file}');
    """)

    print("Data ingestion complete.")
    
    # Verify the data is loaded
    record_count = con.execute("SELECT COUNT(*) FROM bronze.bronze_transactions;").fetchone()[0]
    print(f"Total records in bronze_transactions: {record_count}")

    con.close()

if __name__ == "__main__":
    setup_bronze_layer()