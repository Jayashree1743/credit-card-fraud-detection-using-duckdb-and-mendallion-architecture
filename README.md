
### Data Layers

**Bronze Layer**
-   Raw transaction data from `fraudTrain.csv` and `fraudTest.csv` is ingested into a single table in DuckDB.
-   No transformations are applied. This layer acts as the immutable source of truth.

**Silver Layer**
-   Data is cleaned and standardized.
-   Proper data types are enforced (timestamps, numerics).
-   New columns are derived, such as `age` from date of birth and `trans_hour` from the transaction timestamp.

**Gold Layer**
-   Creates the final, ML-ready feature table.
-   Personally identifiable information (PII) and raw identifiers are excluded from the feature set but preserved for traceability.
-   This layer serves as the direct input for model training.

### Feature Engineering

Features are selected to capture behavioral patterns relevant to fraud.

-   **Time-based:** `trans_hour`
-   **Amount-based:** `amt`
-   **Geographic:** `lat`, `long`, `merch_lat`, `merch_long`
-   **Customer context:** `age`, `city_pop`
-   **Categorical:** `merchant`, `category`, `gender`, `job` are one-hot encoded to be used in the model.

To prevent data leakage, the one-hot encoding schema is determined only from the training data and saved, ensuring consistency during future scoring.

### Modeling Strategy

**Model Choice**
-   **RandomForestClassifier**
-   Chosen for its high performance, robustness with mixed data types, and ability to handle complex interactions between features.

**Evaluation Approach**
-   The dataset is split into training and testing sets with stratification on the `is_fraud` column to maintain the same class distribution in both sets.
-   The model achieved **100% precision** and **68% recall** on the fraud class, meaning it generates no false positives while catching a majority of fraudulent transactions.

### How to Run the Project

1.  **Prerequisites:** Ensure you have Python and `pip` installed.
2.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd credit-card-trae
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Add Data:** Place `fraudTrain.csv` and `fraudTest.csv` in the root directory of the project.
5.  **Run the pipeline:**
    ```bash
    python src/train.py
    ```
    This single command will execute the entire Bronze → Silver → Gold pipeline and train the model.

### Key Design Decisions

-   **DuckDB as a Core Engine:** Using DuckDB simplifies the architecture by providing a powerful, file-based data warehouse without the need for external database servers.
-   **Modularity:** Each step of the ETL pipeline (Bronze, Silver, Gold, Train) is a separate Python script, making the system easy to understand, maintain, and debug.
-   **No Data Leakage:** Strict separation of `train` and `test` data, with feature encodings learned only from the training set.
-   **Reproducibility:** The model and the columns used for training are saved, ensuring that batch scoring can be performed consistently.

### Skills Demonstrated

-   End-to-End Data Pipeline Development
-   Medallion (Bronze/Silver/Gold) Architecture
-   DuckDB for High-Performance Data Transformation
-   Feature Engineering for Imbalanced Datasets
-   Scikit-learn for Classification Modeling
-   Model Evaluation (Precision, Recall, Confusion Matrix)
-   Python-based Scripting and Orchestration

### Future Improvements

-   Implement a separate `predict.py` script for batch scoring on new data.
-   Introduce model versioning and experiment tracking (e.g., with MLflow).
-   Develop a cost-based evaluation metric to optimize the classification threshold directly against business costs.
-   Containerize the application with Docker for easier deployment.
