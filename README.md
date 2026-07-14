#  Sistem Deteksi Kanker Payudara Berbasis Machine Learning (MLOps)

Proyek ini merupakan Submission untuk kelas **Membangun Sistem Machine Learning** di Dicoding. Proyek ini mendemonstrasikan siklus hidup *Machine Learning Operations* (MLOps) secara penuh dari tahap pemrosesan data, pelatihan model, *Continuous Integration* (CI), hingga *Monitoring & Logging*.

##  Deskripsi Proyek
Model AI dalam proyek ini dilatih menggunakan algoritma `RandomForestClassifier` untuk mendiagnosis sel tumor payudara (Ganas atau Jinak) berdasarkan 30 fitur metrik medis dari dataset Breast Cancer Wisconsin. 

Seluruh siklus hidup (*lifecycle*) proyek ini dirancang dengan prinsip-prinsip *Software Engineering* yang kuat untuk memastikan sistem stabil, mudah diperbarui, dan bisa dipantau secara langsung (*Real-Time*).

##  Fitur MLOps yang Diterapkan

### 1. Data Preprocessing (Kriteria 1)
Data mentah diproses dan dibersihkan menggunakan *pipeline* otomatis (`automate_Muhammad-Shirojul-Munir.py`) untuk memisahkan fitur dengan label, yang kemudian siap disuapkan ke dalam pelatihan model.

### 2. Model Tracking & Registry (Kriteria 2)
Menggunakan **MLflow** dan **DagsHub** untuk melacak setiap eksperimen (Hyperparameter Tuning). Seluruh metrik akurasi, parameter, dan artefak model (Grafik *Confusion Matrix* & *Feature Importance*) direkam dan di-host secara jarak jauh agar bisa dipantau secara online.

### 3. Continuous Integration / CI (Kriteria 3)
Menggunakan **GitHub Actions** untuk memastikan kualitas kode secara otomatis setiap kali ada perubahan (*Push/Pull Request*). Terdiri dari dua alur kerja utama:
- `preprocessing.yml`: Mengotomatiskan validasi data.
- `retrain.yml`: Mengotomatiskan eksperimen dan evaluasi model.

### 4. Real-Time Monitoring & Alerting (Kriteria 4)
Model yang telah jadi dijalankan sebagai *REST API Endpoint* (MLflow Serve). Sistem ini terus diawasi menggunakan kombinasi **Prometheus** dan **Grafana**:
- **Prometheus Exporter:** Mengumpulkan 10 jenis metrik secara kustom dari model.
- **Grafana Dashboard:** Memvisualisasikan lalu-lintas data (jumlah diagnosis, penggunaan CPU, dsb).
- **Alerting System:** Mengirimkan peringatan secara langsung ke *Webhook* apabila metrik (*resource* / *error*) melebihi batas aman.

##  Instalasi & Penggunaan
1. Lakukan instalasi paket menggunakan perintah `pip install -r requirements.txt`.
2. Jalankan *endpoint* MLflow:
   ```bash
   mlflow models serve -m "mlruns/0/<run_id>/artifacts/model" -p 5000 --env-manager local
   ```
3. Lakukan simulasi permintaan (*request*) menggunakan `uji_coba_pasien.py`.
4. Untuk melihat visualisasi, jalankan *Prometheus Exporter* dan sambungkan Grafana Anda.

---
*Dibuat oleh Muhammad Shirojul Munir.*
