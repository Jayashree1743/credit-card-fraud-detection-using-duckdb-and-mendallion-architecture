import duckdb
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from gold import setup_gold_layer

def train_model():
    """
    Trains a RandomForestClassifier on the gold layer data.
    """
    # Ensure the full data pipeline has been run
    setup_gold_layer()

    db_path = os.path.join('..', 'data', 'fraud_detection.duckdb')
    con = duckdb.connect(database=db_path, read_only=False)

    print("Loading data from gold.gold_transactions...")
    # Load a 50% sample of the data to avoid memory errors during training.
    # This is a common strategy when dealing with large datasets that don't fit into memory.
    df = con.execute("SELECT * FROM gold.gold_transactions TABLESAMPLE 50 PERCENT (BERNOULLI)").fetchdf()
    print(f"Loaded a sample of {len(df)} records for training.")
    con.close()

    print("Preparing data for training...")

    # Define features (X) and target (y)
    # Exclude identifiers, raw timestamps, and the target variable itself
    features = [col for col in df.columns if col not in [
        'cc_num', 'first', 'last', 'street', 'city', 'state', 'zip', 'dob',
        'trans_num', 'trans_date_trans_time', 'trans_date_time', 'is_fraud'
    ]]
    
    X = df[features]
    y = df['is_fraud']

    # One-hot encode categorical features
    categorical_features = ['merchant', 'category', 'gender', 'job']
    X = pd.get_dummies(X, columns=categorical_features, drop_first=True)

    # Align columns for prediction later - crucial if test set has different categories
    train_cols = X.columns
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    print("Training RandomForestClassifier model...")
    # Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print("Evaluating model performance...")
    # Make predictions and evaluate
    y_pred = model.predict(X_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save the trained model and the column list
    model_path = os.path.join('..', 'models')
    if not os.path.exists(model_path):
        os.makedirs(model_path)
        
    joblib.dump(model, os.path.join(model_path, 'fraud_detection_model.joblib'))
    joblib.dump(train_cols, os.path.join(model_path, 'model_columns.joblib'))

    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # The train_model function now handles the full pipeline run and training
    train_model()