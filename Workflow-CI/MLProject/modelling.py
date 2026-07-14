import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import mlflow
import os

if __name__ == "__main__":
    mlflow.autolog()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    train_path = os.path.join(script_dir, "breast_cancer_preprocessing", "train.csv")
    test_path = os.path.join(script_dir, "breast_cancer_preprocessing", "test.csv")
    
    if not os.path.exists(train_path):
        print(f"File {train_path} tidak ditemukan.")
        exit(1)
        
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    with mlflow.start_run(run_name="basic_rf_model"):
        # Training Model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluasi
        accuracy = model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy:.4f}")
        
        # Model sudah otomatis tersimpan ke MLflow berkat autolog()
