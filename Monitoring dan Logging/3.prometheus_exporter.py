from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time
import psutil
import random

# Definisi 10 Metrics untuk kriteria Advanced (Bintang 5)
INFERENCE_TOTAL = Counter('model_inference_total', 'Total prediksi yang dilakukan oleh model')
INFERENCE_DURATION = Histogram('model_inference_duration_seconds', 'Waktu yang dihabiskan untuk prediksi')
PREDICTION_0_TOTAL = Counter('model_prediction_0_total', 'Total prediksi kelas 0 (Malignant)')
PREDICTION_1_TOTAL = Counter('model_prediction_1_total', 'Total prediksi kelas 1 (Benign)')
CPU_USAGE = Gauge('cpu_usage_percent', 'Penggunaan CPU saat ini (%)')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Penggunaan RAM saat ini (bytes)')
ACTIVE_REQUESTS = Gauge('active_requests', 'Jumlah request yang sedang diproses')
ERROR_REQUESTS = Counter('error_requests_total', 'Total request yang gagal atau error')
MODEL_ACCURACY_EST = Gauge('model_accuracy_estimate', 'Estimasi akurasi model dari feedback loop')
DATA_DRIFT_SCORE = Gauge('data_drift_score_estimate', 'Estimasi persentase pergeseran data')

def process_request():
    """Simulasi pemrosesan request dan ekspor metrik"""
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    
    # Update resource metrics
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    
    try:
        # Simulasi waktu inferensi (0.1s - 0.5s)
        time.sleep(random.uniform(0.1, 0.5))
        INFERENCE_TOTAL.inc()
        
        # Simulasi hasil prediksi
        prediction = random.choice([0, 1])
        if prediction == 0:
            PREDICTION_0_TOTAL.inc()
        else:
            PREDICTION_1_TOTAL.inc()
            
        # Update dummy accuracy and drift scores
        MODEL_ACCURACY_EST.set(random.uniform(0.92, 0.98))
        DATA_DRIFT_SCORE.set(random.uniform(0.01, 0.05))
        
    except Exception:
        ERROR_REQUESTS.inc()
    finally:
        duration = time.time() - start_time
        INFERENCE_DURATION.observe(duration)
        ACTIVE_REQUESTS.dec()

if __name__ == '__main__':
    # Jalankan server Prometheus exporter di port 8000
    start_http_server(8000)
    print("Prometheus metrics exporter berjalan di http://localhost:8000")
    
    # Simulasi loop agar selalu ada metrik untuk discrap
    while True:
        process_request()
        time.sleep(random.uniform(1, 4))
