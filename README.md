# Credit-Card-Fraud-Detection – End-to-End Pipeline with DuckDB

This project implements an end-to-end credit card fraud detection pipeline using **Python and DuckDB**, following a **Lakehouse (Medallion) architecture** on a local machine.

The goal is not just to train a machine learning model, but to design a **production-style data pipeline** that mirrors real-world data engineering and fraud detection systems. The pipeline:

* Ingests raw transaction data
* Cleans and standardizes it
* Engineers fraud-relevant features
* Trains a high-performance ML model
* Produces analytics-ready outputs for evaluation and reporting

The solution is modular, reproducible, and aligned with enterprise data engineering best practices.

---

## Business Problem

A credit card company wants to identify fraudulent transactions in a very large dataset.

**Key Requirement:**

* Missing a fraudulent transaction is more costly than flagging a legitimate one.

This introduces a **precision–recall tradeoff**. While the initial model achieves very high precision, the pipeline is designed so that thresholds can later be tuned toward **higher recall** based on business priorities.

---

## Architecture

The solution follows the **Bronze → Silver → Gold** Medallion architecture using DuckDB as a fast, file-based analytical warehouse.

```
Raw CSV Files  
   ↓  
Bronze Layer (Raw Tables in DuckDB)  
   ↓  
Silver Layer (Cleaned & Enriched Data)  
   ↓  
Gold Layer (ML Feature Table)  
   ↓  
Model Training  
   ↓  
Saved Model & Feature Schema  
   ↓  
Future Batch Scoring
```

DuckDB acts as the single engine for:

* Storage
* SQL transformations
* Analytical queries

No external database or server is required.

---

## Components Used

* **DuckDB** – High-performance in-process analytical database
* **Pandas** – DataFrame handling and ML preparation
* **Scikit-learn** – ML modeling using `RandomForestClassifier`
* **Joblib** – Model and column schema serialization
* **Python Scripts** – Orchestrate the entire pipeline

---

## Dataset

Dataset used:

```
https://www.kaggle.com/datasets/kartik2112/fraud-detection
```

The dataset contains:

* Transaction metadata (time, amount)
* Customer attributes (DOB, city population, job, gender)
* Merchant attributes (location, category)
* Target variable: `is_fraud`

The dataset is **highly imbalanced**, which is typical in fraud detection and drives the modeling strategy.

---

## Project Structure

```
credit-card-trae/
│
├── src/
│   ├── bronze.py        # Raw data ingestion
│   ├── silver.py        # Cleaning and enrichment
│   ├── gold.py          # Feature engineering
│   ├── train.py         # Model training pipeline
│
├── data/
│   ├── fraudTrain.csv
│   └── fraudTest.csv
│
├── models/
│   ├── fraud_model.pkl
│   └── model_columns.pkl
│
├── requirements.txt
└── README.md
```

Each stage represents a clear separation of responsibility in the data pipeline.

---

## Data Layers

### Bronze Layer

* Raw CSV files (`fraudTrain.csv`, `fraudTest.csv`) are ingested into DuckDB tables.
* No transformations are applied.
* Acts as the immutable **source of truth**.

### Silver Layer

* Data is cleaned and standardized:

  * Data types enforced (timestamps, numerics)
  * Missing values handled
  * Derived columns added:

    * `age` from date of birth
    * `trans_hour` from transaction timestamp

### Gold Layer

* Creates the final ML-ready feature table.
* Personally identifiable information (PII) and raw identifiers are removed from the feature set.
* Transaction identifiers are preserved separately for traceability.
* This layer directly feeds model training.

---

## Feature Engineering

Features are designed to capture **behavioral fraud patterns**, not personal identity.

Key feature groups:

* **Time-based**

  * `trans_hour`

* **Amount-based**

  * `amt`

* **Geographic**

  * `lat`, `long`, `merch_lat`, `merch_long`

* **Customer context**

  * `age`, `city_pop`

* **Categorical**

  * `merchant`, `category`, `gender`, `job`
  * Encoded using one-hot encoding

To prevent **data leakage**:

* The encoding schema is learned only from the training data.
* Column mappings are saved and reused during scoring.

---

## Modeling Strategy

### Model Choice

**RandomForestClassifier**

Chosen for:

* High performance
* Ability to capture nonlinear patterns
* Robustness with mixed numerical and categorical features
* Strong performance on imbalanced datasets

---

### Evaluation Approach

* Train/test split is stratified on `is_fraud`
* Class distribution is preserved
* Metrics focus on:

  * Precision
  * Recall
  * Confusion matrix

Current results:

* **Precision: 100%**
* **Recall: 68%**

This means:

* No legitimate transactions are flagged as fraud
* A majority of fraudulent transactions are correctly identified

The system is designed so recall can be increased later by adjusting thresholds.

---

## How to Run the Project

1. Clone the repository:

```bash
git clone <your-repo-url>
cd credit-card-trae
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add the dataset:
   Place:

```
fraudTrain.csv  
fraudTest.csv
```

inside the project root or `data/` directory.

4. Run the entire pipeline:

```bash
python src/train.py
```

This single command executes:

* Bronze ingestion
* Silver cleaning
* Gold feature creation
* Model training
* Model + schema saving

---

## Key Design Decisions

* **DuckDB as Core Engine**
  Eliminates the need for external databases while providing high-speed analytics.

* **Medallion Architecture**
  Ensures clean separation between raw, cleaned, and ML-ready data.

* **No Data Leakage**
  Encodings and transformations are learned strictly from training data.

* **Reproducibility**
  Model and feature columns are saved using Joblib.

* **Modular Design**
  Each stage is independently understandable and maintainable.

---

## Skills Demonstrated

* End-to-End Data Pipeline Design
* Medallion (Bronze / Silver / Gold) Architecture
* DuckDB for Analytical Workloads
* Feature Engineering for Imbalanced ML Problems
* Random Forest Modeling
* Precision–Recall Tradeoff Analysis
* Production-Oriented ML Workflow
* Python-based Data Engineering

---

## Future Improvements

* Add `predict.py` for batch scoring on new data
* Introduce model versioning with MLflow
* Cost-based threshold optimization
* Real-time or streaming ingestion
* Docker containerization
* Power BI / Streamlit dashboard for fraud analytics

---

This DuckDB project mirrors enterprise-grade Fabric pipelines, showing that **production-quality data engineering and ML pipelines can be built locally using open-source tools**.
