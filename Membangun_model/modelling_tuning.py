import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import mlflow
import mlflow.sklearn
import dagshub
import os

def create_confusion_matrix_plot(y_true, y_pred, output_path="confusion_matrix.png"):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_feature_importance_plot(model, feature_names, num_features, output_path="feature_importance.png"):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(num_features), importances[indices], align="center")
    plt.xticks(range(num_features), [feature_names[i] for i in indices], rotation=90)
    plt.xlim([-1, num_features])
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    mlflow.autolog(disable=True)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    train_path = os.path.join(script_dir, "..", "Eksperimen_SML_Muhammad-Shirojul-Munir", "breast_cancer_preprocessing", "train.csv")
    test_path = os.path.join(script_dir, "..", "Eksperimen_SML_Muhammad-Shirojul-Munir", "breast_cancer_preprocessing", "test.csv")
    
    if not os.path.exists(train_path):
        alt_path = os.path.join(script_dir, "breast_cancer_preprocessing", "train.csv")
        if os.path.exists(alt_path):
            train_path = alt_path
            test_path = os.path.join(script_dir, "breast_cancer_preprocessing", "test.csv")
        else:
            print(f"File tidak ditemukan. Pastikan preprocessing sudah dijalankan.")
            exit(1)
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    with mlflow.start_run(run_name="tuned_rf_model"):
        # Hyperparameter tuning dengan GridSearchCV
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        }
        
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
        grid_search.fit(X_train, y_train)
        
        best_model = grid_search.best_estimator_
        
        # Prediksi dan Evaluasi
        y_pred = best_model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # --- Manual Logging ke MLflow ---
        # 1. Log parameter (best params)
        mlflow.log_params(grid_search.best_params_)
        
        # 2. Log metrics
        mlflow.log_metrics({
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1
        })
        
        # 3. Log model
        mlflow.sklearn.log_model(best_model, "model")
        
        # 4. Log Ekstra Artefak (Kriteria Advanced: minimal 2 artefak tambahan)
        cm_path = "confusion_matrix.png"
        fi_path = "feature_importance.png"
        
        create_confusion_matrix_plot(y_test, y_pred, cm_path)
        create_feature_importance_plot(best_model, X_train.columns, X_train.shape[1], fi_path)
        
        mlflow.log_artifact(cm_path)
        mlflow.log_artifact(fi_path)
        
        # Cleanup file lokal
        os.remove(cm_path)
        os.remove(fi_path)
        
        print("Training dan Logging Selesai. Artefak berhasil disimpan ke MLflow.")
