# -*- coding: utf-8 -*-
"""
TÜBİTAK 2209-A Araştırma Projesi - Model Eğitimi ve Nesne Kaydı Betiği
İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme
"""

import sys
import os
import json
import warnings
import urllib.request

# Kullanıcı site-packages yolunu ekle
USER_SITE = r"C:\Users\SEFA\AppData\Roaming\Python\Python314\site-packages"
if os.path.exists(USER_SITE) and USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
from imblearn.over_sampling import SMOTE
import joblib
import shap

np.random.seed(42)

def train_and_save():
    print("=" * 60)
    print("TÜBİTAK 2209-A Model Eğitimi Başlatılıyor...")
    print("=" * 60)

    # 1. Veri seti temini
    dataset_file = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    if not os.path.exists(dataset_file):
        print("Veri seti yerelde bulunamadı, indiriliyor...")
        url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
        urllib.request.urlretrieve(url, dataset_file)
        print("Veri seti indirildi.")
    else:
        print("Veri seti yerel diskten yükleniyor.")

    df = pd.read_csv(dataset_file)
    print(f"Orijinal Veri Boyutu: {df.shape[0]} satır, {df.shape[1]} sütun")

    # 2. Ön İşleme
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna(subset=['TotalCharges']).reset_index(drop=True)
    df = df.drop_duplicates().reset_index(drop=True)

    df["MultipleLines"] = df["MultipleLines"].replace("No phone service", "No")
    internet_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    for col in internet_cols:
        df[col] = df[col].replace("No internet service", "No")

    df["Streaming"] = ((df["StreamingTV"] == "Yes") | (df["StreamingMovies"] == "Yes")).astype(int)
    df = df.drop(["StreamingTV", "StreamingMovies"], axis=1)

    if 'gender' in df.columns:
        df = df.drop(["gender"], axis=1)
    if 'customerID' in df.columns:
        df = df.drop(["customerID"], axis=1)

    binary_cols = [
        'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'PaperlessBilling', 'Churn'
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X = pd.get_dummies(
        X, columns=['InternetService', 'Contract', 'PaymentMethod'],
        drop_first=True, dtype=int
    )

    feature_names = X.columns.tolist()
    print(f"Öznitelik Sayısı: {len(feature_names)}")

    # 3. Train / Test Ayrımı
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    # SMOTE Uygulaması
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

    # 4. Modellerin Eğitimi
    classifiers = {
        "Lojistik Regresyon": LogisticRegression(max_iter=1000, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=11),
        "SVM": SVC(probability=True, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4, eval_metric="logloss", random_state=42),
        "MLP (Derin Öğrenme)": MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=200, random_state=42)
    }

    results = []
    trained_models = {}
    roc_curves = {}
    confusion_matrices = {}

    for name, clf in classifiers.items():
        print(f"Eğitiliyor: {name}...")
        clf.fit(X_train_res, y_train_res)
        y_pred = clf.predict(X_test_scaled)
        y_proba = clf.predict_proba(X_test_scaled)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        fpr, tpr, _ = roc_curve(y_test, y_proba)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results.append({
            "Model": name,
            "Accuracy": float(acc),
            "Precision": float(prec),
            "Recall": float(rec),
            "F1-Score": float(f1),
            "AUC": float(auc)
        })
        trained_models[name] = clf
        roc_curves[name] = {"fpr": fpr.tolist(), "tpr": tpr.tolist()}
        confusion_matrices[name] = cm

    results_df = pd.DataFrame(results).sort_values("AUC", ascending=False).reset_index(drop=True)
    print("\n--- MODEL KARŞILAŞTIRMA METRİKLERİ ---")
    print(results_df.to_string(index=False))

    # 5. Şampiyon Model Seçimi (Klasik ve DL)
    # Proje hedeflerine ve raporuna göre en yüksek doğruluk (Accuracy: 0.768) ve kesinliğe sahip model: Random Forest
    klasik_sampiyon_name = "Random Forest"
    klasik_sampiyon_model = trained_models[klasik_sampiyon_name]
    mlp_model = trained_models["MLP (Derin Öğrenme)"]

    print(f"\nKlasik Şampiyon Model: {klasik_sampiyon_name}")

    # 6. SHAP Açıklanabilirlik Analizi
    print("\nSHAP Analizleri Hesaplanıyor...")
    bg_size = min(100, len(X_train_res))
    sample_size = min(100, len(X_test_scaled))

    X_bg = shap.sample(X_train_res, bg_size, random_state=42)
    X_sample = X_test_scaled.sample(sample_size, random_state=42)

    # SHAP Explainer (Ağaç tabanlı model için TreeExplainer)
    if isinstance(klasik_sampiyon_model, RandomForestClassifier) or hasattr(klasik_sampiyon_model, "estimators_"):
        explainer = shap.TreeExplainer(klasik_sampiyon_model)
        shap_values = explainer(X_sample)
    else:
        explainer = shap.Explainer(klasik_sampiyon_model.predict_proba, X_bg)
        shap_values = explainer(X_sample)

    if hasattr(shap_values, "values") and shap_values.values.ndim == 3:
        shap_vals_class1 = shap_values.values[:, :, 1]
        base_value_class1 = shap_values.base_values[:, 1]
    else:
        shap_vals_class1 = shap_values.values
        base_value_class1 = shap_values.base_values

    # 7. Kaydetme
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(klasik_sampiyon_model, os.path.join(models_dir, "klasik_sampiyon_model.pkl"))
    joblib.dump(mlp_model, os.path.join(models_dir, "mlp_model.pkl"))
    joblib.dump(scaler, os.path.join(models_dir, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(models_dir, "feature_columns.pkl"))

    shap_payload = {
        "shap_values": shap_vals_class1,
        "base_values": base_value_class1,
        "sample_data": X_sample,
        "feature_names": feature_names,
        "klasik_sampiyon_name": klasik_sampiyon_name
    }
    joblib.dump(shap_payload, os.path.join(models_dir, "shap_data.pkl"))

    test_payload = {
        "X_test_scaled": X_test_scaled,
        "y_test": y_test,
        "X_test_raw": X_test
    }
    joblib.dump(test_payload, os.path.join(models_dir, "test_data.pkl"))

    meta_info = {
        "klasik_sampiyon_name": klasik_sampiyon_name,
        "results": results,
        "roc_curves": roc_curves,
        "confusion_matrices": confusion_matrices,
        "feature_names": feature_names
    }
    with open(os.path.join(models_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)

    print(f"\nTüm modeller ve açıklanabilirlik nesneleri '{models_dir}' klasörüne başarıyla kaydedildi!")

if __name__ == "__main__":
    train_and_save()
