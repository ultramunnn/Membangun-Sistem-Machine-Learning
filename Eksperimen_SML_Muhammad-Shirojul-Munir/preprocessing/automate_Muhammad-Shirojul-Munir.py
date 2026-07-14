import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def load_data():
    """Memuat dataset breast cancer dari sklearn"""
    print("Memuat dataset...")
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df

def preprocess_data(df):
    """Melakukan tahapan preprocessing data"""
    print("Memulai preprocessing data...")
    # Cek missing values (Breast cancer sklearn biasanya bersih, tapi ini best practice)
    if df.isnull().sum().sum() > 0:
        df = df.dropna()
        
    # Memisahkan fitur dan target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Normalisasi data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Konversi kembali ke dataframe
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    
    X_train_scaled_df['target'] = y_train.values
    X_test_scaled_df['target'] = y_test.values
    
    return X_train_scaled_df, X_test_scaled_df

def save_raw_data(df, output_dir):
    print(f"Menyimpan data raw ke {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, 'raw.csv'), index=False)
    print("Data raw berhasil disimpan!")

def save_data(train_df, test_df, output_dir):
    print(f"Menyimpan data ke {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)
    print("Data berhasil disimpan!")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(script_dir, "..", "breast_cancer_raw")
    output_directory = os.path.join(script_dir, "..", "breast_cancer_preprocessing")
    
    raw_df = load_data()
    save_raw_data(raw_df, raw_dir)
    train_processed, test_processed = preprocess_data(raw_df)
    save_data(train_processed, test_processed, output_directory)
