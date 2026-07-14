import requests
import pandas as pd
import random
import os

print("==============================================")
print("SISTEM DIAGNOSIS KANKER PAYUDARA AI ")
print("==============================================\n")

# Load data test
script_dir = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.join(script_dir, "Eksperimen_SML_Muhammad-Shirojul-Munir", "preprocessing", "dataset_preprocessing", "test.csv")

try:
    data = pd.read_csv(test_path)
except Exception as e:
    print("Data tidak ditemukan! Pastikan file test.csv ada.")
    exit()

# Ambil 1 pasien secara acak
patient_idx = random.randint(0, len(data)-1)
patient_data = data.iloc[patient_idx]
features = patient_data.drop('target')
actual_target = patient_data['target']

print(f"Data Lab Pasien No. {patient_idx}:")
for col_name, value in features.items():
    print(f"- {col_name:25} : {value:.4f}")
print("\nMeminta Diagnosis dari Model AI (MLflow Server)...")
url = "http://127.0.0.1:5000/invocations"
payload = {
    "dataframe_split": {
        "columns": features.index.tolist(),
        "data": [features.values.tolist()]
    }
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        prediction = response.json()["predictions"][0]
        
        print("\n================HASIL=================")
        
        # 0 = Malignant (Ganas), 1 = Benign (Jinak)
        diagnosis_ai = "KANKER GANAS 🔴" if prediction == 0 else "TUMOR JINAK 🟢"
        diagnosis_asli = "KANKER GANAS 🔴" if actual_target == 0 else "TUMOR JINAK 🟢"
        
        print(f"Diagnosis AI    : {diagnosis_ai}")
        print(f"Diagnosis Asli  : {diagnosis_asli}")
        
        if prediction == actual_target:
            print("Status          : AI BENAR!")
        else:
            print("Status          : AI SALAH ")
        print("======================================\n")
    else:
        print(f"Error dari server: {response.text}")
except Exception as e:
    print("Gagal menghubungi server model. Pastikan mlflow models serve sedang berjalan!")
