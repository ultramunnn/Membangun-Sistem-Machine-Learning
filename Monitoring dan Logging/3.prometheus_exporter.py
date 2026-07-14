from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time
import psutil
import requests
import random
import pandas as pd
import os
import json

# Definisi Metrik
INFERENCE_TOTAL = Counter('model_inference_total', 'Total prediksi yang dilakukan oleh model')
INFERENCE_DURATION = Histogram('model_inference_duration_seconds', 'Waktu yang dihabiskan untuk prediksi (Real)')
PREDICTION_0_TOTAL = Counter('model_prediction_0_total', 'Total prediksi kelas 0 (Malignant) asli')
PREDICTION_1_TOTAL = Counter('model_prediction_1_total', 'Total prediksi kelas 1 (Benign) asli')
CPU_USAGE = Gauge('cpu_usage_percent', 'Penggunaan CPU saat ini (%)')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Penggunaan RAM saat ini (bytes)')
ACTIVE_REQUESTS = Gauge('active_requests', 'Jumlah request yang sedang diproses')
ERROR_REQUESTS = Counter('error_requests_total', 'Total request yang gagal atau error asli')

MLFLOW_SERVING_URL = "http://127.0.0.1:5000/invocations"

def load_test_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(script_dir, "..", "Eksperimen_SML_Muhammad-Shirojul-Munir", "preprocessing", "dataset_preprocessing", "test.csv")
        test_data = pd.read_csv(test_path)
        X_test_df = test_data.drop('target', axis=1)
        columns = X_test_df.columns.tolist()
        X_test = X_test_df.values.tolist()
        return columns, X_test
    except Exception as e:
        print("Gagal membaca test.csv. Pastikan file ada. Error:", e)
        return [str(i) for i in range(30)], [[0.5] * 30] * 10

def process_request(columns, X_test):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    
    # Update resource metrics
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    
    try:
        sample = random.choice(X_test)
        payload = {
            "dataframe_split": {
                "columns": columns,
                "data": [sample]
            }
        }
        
        # Real Inference Request
        response = requests.post(MLFLOW_SERVING_URL, json=payload, headers={'Content-Type': 'application/json'}, timeout=5)
        INFERENCE_TOTAL.inc()
        
        if response.status_code == 200:
            result = response.json()
            # Asumsi response JSON berupa list atau dict dengan prediksi, contoh: {"predictions": [0]} atau [0]
            prediction = None
            if isinstance(result, dict) and "predictions" in result:
                prediction = result["predictions"][0]
            elif isinstance(result, list):
                prediction = result[0]
                
            if prediction == 0:
                PREDICTION_0_TOTAL.inc()
            elif prediction == 1:
                PREDICTION_1_TOTAL.inc()
        else:
            ERROR_REQUESTS.inc()
            
    except requests.exceptions.RequestException:
        ERROR_REQUESTS.inc()
    finally:
        duration = time.time() - start_time
        INFERENCE_DURATION.observe(duration)
        ACTIVE_REQUESTS.dec()

if __name__ == '__main__':
    columns, X_test = load_test_data()
    
    # Jalankan server Prometheus exporter di port 8000
    start_http_server(8000)
    print("Prometheus metrics exporter (REAL) berjalan di http://localhost:8000")
    print("Memulai pengiriman traffic riil ke MLflow server di", MLFLOW_SERVING_URL)
    
    # Simulasi loop inferensi riil
    while True:
        process_request(columns, X_test)
        time.sleep(random.uniform(1, 4))
