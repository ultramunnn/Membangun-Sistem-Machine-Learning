import requests
import time
import random
import pandas as pd
import os

# Asumsi model diserve di localhost:5000 menggunakan mlflow models serve
url = "http://127.0.0.1:5000/invocations"

# Load sample data dari test.csv
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(script_dir, "..", "Eksperimen_SML_Muhammad-Shirojul-Munir", "breast_cancer_preprocessing", "test.csv")
    test_data = pd.read_csv(test_path)
    X_test_df = test_data.drop('target', axis=1)
    columns = X_test_df.columns.tolist()
    X_test = X_test_df.values.tolist()
except Exception as e:
    print("Gagal membaca test.csv. Pastikan file ada. Error:", e)
    columns = [str(i) for i in range(30)]
    X_test = [[0.5] * 30] * 10  # Fallback dummy data jika tidak ketemu

print("Memulai simulasi request (Inference) ke endpoint MLflow...")

while True:
    # Ambil 1 baris random dari data test
    sample = random.choice(X_test)
    
    payload = {
        "dataframe_split": {
            "columns": columns,
            "data": [sample]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"Request status: {response.status_code}, Prediction: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        
    time.sleep(random.uniform(1.0, 3.0)) # Jeda 1-3 detik antar request
