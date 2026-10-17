import json
import os
import joblib
import numpy as np
import pandas as pd
import shap

# Pandas compatibility
try:
    _orig_string_dtype_init = pd.StringDtype.__init__
    def _compat_string_dtype_init(self, storage=None, *args, **kwargs):
        _orig_string_dtype_init(self, storage=storage)
    pd.StringDtype.__init__ = _compat_string_dtype_init
except Exception:
    pass

BASE_DIR = os.path.abspath('.')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load models and test data
rf_model = joblib.load(os.path.join(MODELS_DIR, 'klasik_sampiyon_model.pkl'))
mlp_model = joblib.load(os.path.join(MODELS_DIR, 'mlp_model.pkl'))
scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
feature_names = joblib.load(os.path.join(MODELS_DIR, 'feature_columns.pkl'))
shap_data_rf = joblib.load(os.path.join(MODELS_DIR, 'shap_data.pkl'))
test_data = joblib.load(os.path.join(MODELS_DIR, 'test_data.pkl'))

with open(os.path.join(MODELS_DIR, 'metadata.json'), 'r', encoding='utf-8') as f:
    metadata = json.load(f)

X_test_scaled = test_data['X_test_scaled']
X_test_raw = test_data['X_test_raw']
y_test = test_data['y_test']

print('Feature count:', len(feature_names))
print('Features:', feature_names)

# 1. RF Global SHAP
rf_shap_vals = shap_data_rf['shap_values'] # shape (100, 21)
rf_mean_abs = np.abs(rf_shap_vals).mean(axis=0)
rf_importance = pd.DataFrame({
    'Feature': feature_names,
    'Mean_Abs_SHAP': rf_mean_abs
}).sort_values('Mean_Abs_SHAP', ascending=False).reset_index(drop=True)

print('\n=== RANDOM FOREST TOP 10 GLOBAL FEATURES ===')
print(rf_importance.head(10).to_string(index=False))

# 2. MLP SHAP Calculation
print('\nComputing MLP SHAP values on test sample...')
sample_size = 100
np.random.seed(42)
sample_indices = np.random.choice(len(X_test_scaled), sample_size, replace=False)
X_sample = X_test_scaled.iloc[sample_indices]

# Background for MLP explainer
bg_size = 50
bg_indices = np.random.choice(len(X_test_scaled), bg_size, replace=False)
X_bg = X_test_scaled.iloc[bg_indices]

mlp_explainer = shap.Explainer(mlp_model.predict_proba, X_bg)
mlp_shap_values = mlp_explainer(X_sample)

if hasattr(mlp_shap_values, "values") and mlp_shap_values.values.ndim == 3:
    mlp_shap_vals_class1 = mlp_shap_values.values[:, :, 1]
    mlp_base_value_class1 = mlp_shap_values.base_values[:, 1]
else:
    mlp_shap_vals_class1 = mlp_shap_values.values
    mlp_base_value_class1 = mlp_shap_values.base_values

mlp_mean_abs = np.abs(mlp_shap_vals_class1).mean(axis=0)
mlp_importance = pd.DataFrame({
    'Feature': feature_names,
    'Mean_Abs_SHAP': mlp_mean_abs
}).sort_values('Mean_Abs_SHAP', ascending=False).reset_index(drop=True)

print('\n=== MLP (DERİN ÖĞRENME) TOP 10 GLOBAL FEATURES ===')
print(mlp_importance.head(10).to_string(index=False))

# 3. Select a specific customer for local analysis
# Let's pick a customer who actually churned or high risk
# Find a customer where both or one model predicts churn
rf_probs = rf_model.predict_proba(X_test_scaled)[:, 1]
mlp_probs = mlp_model.predict_proba(X_test_scaled)[:, 1]

# Let's pick a customer with index 24 (or one with clear churn risk)
cust_idx = 24
raw_customer = X_test_raw.iloc[cust_idx]
scaled_customer = X_test_scaled.iloc[[cust_idx]]
actual_label = y_test.iloc[cust_idx]

rf_pred_prob = rf_model.predict_proba(scaled_customer)[0, 1]
mlp_pred_prob = mlp_model.predict_proba(scaled_customer)[0, 1]

print(f'\n=== SELECTED CUSTOMER ANALYSIS (Test Index: {cust_idx}) ===')
print(f'Actual Status: {"AYRILDI (Churn=1)" if actual_label == 1 else "KALDI (Churn=0)}"}')
print(f'Random Forest Churn Tahmin Olasılığı: %{rf_pred_prob*100:.1f}')
print(f'MLP (Derin Öğrenme) Churn Tahmin Olasılığı: %{mlp_pred_prob*100:.1f}')

print('\nMüşteri Profil Özellikleri (Ham Değerler):')
for k, v in raw_customer.items():
    print(f'  {k}: {v}')

# Local SHAP for RF on this customer
rf_explainer = shap.TreeExplainer(rf_model)
rf_cust_shap = rf_explainer(scaled_customer)
if rf_cust_shap.values.ndim == 3:
    rf_cust_vals = rf_cust_shap.values[0, :, 1]
    rf_cust_base = rf_cust_shap.base_values[0, 1]
else:
    rf_cust_vals = rf_cust_shap.values[0]
    rf_cust_base = rf_cust_shap.base_values[0]

rf_cust_df = pd.DataFrame({
    'Feature': feature_names,
    'Value': raw_customer.values,
    'SHAP_Value': rf_cust_vals
}).sort_values('SHAP_Value', key=abs, ascending=False).reset_index(drop=True)

print('\n--- RANDOM FOREST: Müşteri Kararını En Çok Etkileyen Faktörler ---')
print(f'Base Value (Ortalama Tahmin): {rf_cust_base:.3f}')
print(rf_cust_df.head(10).to_string(index=False))

# Local SHAP for MLP on this customer
mlp_cust_shap = mlp_explainer(scaled_customer)
if hasattr(mlp_cust_shap, "values") and mlp_cust_shap.values.ndim == 3:
    mlp_cust_vals = mlp_cust_shap.values[0, :, 1]
    mlp_cust_base = mlp_cust_shap.base_values[0, 1]
else:
    mlp_cust_vals = mlp_cust_shap.values[0]
    mlp_cust_base = mlp_cust_shap.base_values[0]

mlp_cust_df = pd.DataFrame({
    'Feature': feature_names,
    'Value': raw_customer.values,
    'SHAP_Value': mlp_cust_vals
}).sort_values('SHAP_Value', key=abs, ascending=False).reset_index(drop=True)

print('\n--- MLP (DERİN ÖĞRENME): Müşteri Kararını En Çok Etkileyen Faktörler ---')
print(f'Base Value (Ortalama Tahmin): {mlp_cust_base:.3f}')
print(mlp_cust_df.head(10).to_string(index=False))

# Save analysis data to json
analysis_out = {
    'models_results': metadata['results'],
    'rf_top_features': rf_importance.to_dict(orient='records'),
    'mlp_top_features': mlp_importance.to_dict(orient='records'),
    'customer_analysis': {
        'cust_idx': int(cust_idx),
        'actual_label': int(actual_label),
        'rf_pred_prob': float(rf_pred_prob),
        'mlp_pred_prob': float(mlp_pred_prob),
        'raw_values': {k: float(v) if isinstance(v, (int, float, np.number)) else str(v) for k, v in raw_customer.items()},
        'rf_local_shap': rf_cust_df.to_dict(orient='records'),
        'mlp_local_shap': mlp_cust_df.to_dict(orient='records'),
        'rf_base_value': float(rf_cust_base),
        'mlp_base_value': float(mlp_cust_base)
    }
}

with open('detailed_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_out, f, ensure_ascii=False, indent=2)

print('\nAnalysis successfully saved to detailed_analysis_results.json')
