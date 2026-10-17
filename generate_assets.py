# -*- coding: utf-8 -*-
"""
TÜBİTAK 2209-A Projesi - GitHub Assets & Görsel Üretim Betiği
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
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
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Veri ve Modelleri Yükle
with open(os.path.join(MODELS_DIR, 'metadata.json'), 'r', encoding='utf-8') as f:
    metadata = json.load(f)

shap_data = joblib.load(os.path.join(MODELS_DIR, 'shap_data.pkl'))
test_data = joblib.load(os.path.join(MODELS_DIR, 'test_data.pkl'))

# Matplotlib stil ayarları
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

print("1. Churn Dağılım Grafiği Üretiliyor...")
# ==========================================
# 1. CHURN DAĞILIMI
# ==========================================
fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
colors = ['#38bdf8', '#ef4444']
labels = ['Kalan Müşteri (No)', 'Ayrılan Müşteri (Yes)']
sizes = [5174, 1869]
explode = (0, 0.08)

wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    startangle=140, colors=colors, pctdistance=0.75,
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(12)
    autotext.set_weight('bold')

for text in texts:
    text.set_fontsize(11)
    text.set_weight('bold')

ax.set_title("Telco Veri Seti Müşteri Terk (Churn) Dağılımı (7.043 Gözlem)", fontsize=13, weight='bold', pad=15)
plt.tight_layout()
fig.savefig(os.path.join(ASSETS_DIR, 'churn_distribution.png'))
plt.close(fig)

print("2. ROC-AUC Karşılaştırma Eğrisi Üretiliyor...")
# ==========================================
# 2. ROC-AUC EĞRİLERİ
# ==========================================
fig, ax = plt.subplots(figsize=(9, 6), dpi=200)
palette = {
    'Random Forest': '#10b981',
    'XGBoost': '#3b82f6',
    'Lojistik Regresyon': '#f59e0b',
    'SVM': '#8b5cf6',
    'KNN': '#ec4899',
    'MLP (Derin Öğrenme)': '#ef4444'
}

# Modellerin AUC skorlarını alalım
auc_scores = {r['Model']: r['AUC'] for r in metadata['results']}

for name, curve in metadata['roc_curves'].items():
    auc_val = auc_scores.get(name, 0.0)
    color = palette.get(name, '#64748b')
    lw = 2.5 if name == metadata.get('klasik_sampiyon_name') else 1.8
    ax.plot(curve['fpr'], curve['tpr'], label=f"{name} (AUC = {auc_val:.3f})", color=color, linewidth=lw)

ax.plot([0, 1], [0, 1], 'k--', label='Rastgele Tahmin (AUC = 0.500)', alpha=0.6)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.05])
ax.set_xlabel('Yanlış Pozitif Oranı (False Positive Rate)', fontsize=11, fontweight='bold')
ax.set_ylabel('Doğru Pozitif Oranı (True Positive Rate)', fontsize=11, fontweight='bold')
ax.set_title('Çoklu Model ROC-AUC Karşılaştırma Eğrisi', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc="lower right", frameon=True, fontsize=10, shadow=True)
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
fig.savefig(os.path.join(ASSETS_DIR, 'model_comparison_roc.png'))
plt.close(fig)

print("3. Karmaşıklık Matrisi (Confusion Matrix) Üretiliyor...")
# ==========================================
# 3. KARMAŞIKLIK MATRİSİ
# ==========================================
champ_name = metadata.get('klasik_sampiyon_name', 'Random Forest')
cm = np.array(metadata['confusion_matrices'][champ_name])

fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
            xticklabels=['Kalan (0)', 'Ayrılan (1)'],
            yticklabels=['Kalan (0)', 'Ayrılan (1)'],
            annot_kws={'size': 14, 'weight': 'bold'})
ax.set_xlabel('Tahmin Edilen Sınıf', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('Gerçek Sınıf', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title(f'Karmaşıklık Matrisi - {champ_name}', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
fig.savefig(os.path.join(ASSETS_DIR, 'confusion_matrix.png'))
plt.close(fig)

print("4. SHAP Özellik Önemi (Bar Plot) Üretiliyor...")
# ==========================================
# 4. SHAP ÖZELLİK ÖNEMİ
# ==========================================
vals = np.abs(shap_data['shap_values']).mean(axis=0)
feature_importance = pd.DataFrame({
    'Öznitelik': shap_data['feature_names'],
    'Ortalama |SHAP|': vals
}).sort_values('Ortalama |SHAP|', ascending=True).tail(12)

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=200)
y_pos = np.arange(len(feature_importance))
bars = ax.barh(y_pos, feature_importance['Ortalama |SHAP|'], color='#ef4444', height=0.65, edgecolor='#b91c1c')
ax.set_yticks(y_pos)
ax.set_yticklabels(feature_importance['Öznitelik'], fontsize=10, fontweight='bold')
ax.set_xlabel('Ortalama |SHAP Değeri| (Model Kararına Etki Büyüklüğü)', fontsize=11, fontweight='bold')
ax.set_title('Global Açıklanabilirlik: En Etkili 12 Öznitelik (SHAP Bar Plot)', fontsize=12, fontweight='bold', pad=15)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.002, bar.get_y() + bar.get_height()/2, f'{w:.3f}', va='center', ha='left', fontsize=9, fontweight='bold', color='#1e293b')

ax.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
fig.savefig(os.path.join(ASSETS_DIR, 'shap_feature_importance.png'))
plt.close(fig)

print("5. SHAP Beeswarm Dağılım Grafiği Üretiliyor...")
# ==========================================
# 5. SHAP BEESWARM
# ==========================================
fig = plt.figure(figsize=(9, 6), dpi=200)
shap.summary_plot(
    shap_data['shap_values'],
    shap_data['sample_data'],
    feature_names=shap_data['feature_names'],
    max_display=10,
    show=False
)
plt.title("SHAP Beeswarm Özellik Dağılımı ve Yön Etkisi", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, 'shap_summary_beeswarm.png'), bbox_inches='tight')
plt.close()

print("6. SHAP Waterfall (Şelale) Grafiği Üretiliyor...")
# ==========================================
# 6. SHAP WATERFALL
# ==========================================
# Yüksek riskli veya net bir örnek seçelim
sample_idx = 0
exp = shap.Explanation(
    values=shap_data['shap_values'][sample_idx],
    base_values=shap_data['base_values'][sample_idx],
    data=shap_data['sample_data'].iloc[sample_idx].values,
    feature_names=shap_data['feature_names']
)

fig = plt.figure(figsize=(9.5, 5), dpi=200)
shap.waterfall_plot(exp, max_display=10, show=False)
plt.title(f"Örnek Müşteri İçin Yerel Açıklama (Waterfall Plot - İndeks: {sample_idx})", fontsize=11, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, 'shap_waterfall_sample.png'), bbox_inches='tight')
plt.close()

print("7. Dashboard Önizleme Görseli Kontrol Ediliyor...")
# ==========================================
# 7. DASHBOARD PREVIEW
# ==========================================
preview_path = os.path.join(ASSETS_DIR, 'streamlit_dashboard_preview.png')
# Eğer selenium ile screenshot alınabiliyorsa alalım
screenshot_taken = False
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1600,1050')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8501")
    time.sleep(4)
    driver.save_screenshot(preview_path)
    driver.quit()
    screenshot_taken = True
    print("Selenium ile Streamlit arayüz ekran görüntüsü başarıyla alındı!")
except Exception as e:
    print(f"Selenium ile screenshot alınamadı ({e}), alternatif dashboard şablonu oluşturuluyor...")

if not screenshot_taken:
    # Şık bir infografik / overview görseli üretelim
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=200)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    
    # Başlık
    ax.text(0.5, 0.88, "TÜBİTAK 2209-A: Karar Destek Arayüzü & XAI Sistemi", 
            ha='center', va='center', color='#38bdf8', fontsize=18, fontweight='bold')
    ax.text(0.5, 0.80, "Çoklu Makine Öğrenmesi & SHAP Açıklanabilir Müşteri Terk Tahmin Platformu", 
            ha='center', va='center', color='#94a3b8', fontsize=12)
    
    # 5 Sekme Kutusu
    tabs = [
        ("🏠 Genel Bakış\n& Tanıtım", "7.043 Müşteri Analizi\nTarihsel %26.5 Churn"),
        ("🔮 Tekil Risk\nTahmini", "Anlık Olasılık Skoru\nOtomatik Aksiyon"),
        ("🧠 SHAP XAI\nPaneli", "Global Öznitelik Önemi\nTekil Şelale Analizi"),
        ("📊 Çoklu Model\nKıyaslama", "6 Model Karşılaştırma\nİnteraktif ROC & CM"),
        ("📁 Toplu Müşteri\nAnalizi", "Batch CSV Skorlama\nRisk Raporu İndirme")
    ]
    
    x_positions = np.linspace(0.12, 0.88, 5)
    for (title, desc), x in zip(tabs, x_positions):
        rect = plt.Rectangle((x - 0.075, 0.28), 0.15, 0.42, 
                             facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.5,
                             transform=ax.transAxes, clip_on=False, zorder=2)
        ax.add_patch(rect)
        ax.text(x, 0.58, title, ha='center', va='center', color='#f8fafc', fontsize=11, fontweight='bold', transform=ax.transAxes)
        ax.text(x, 0.40, desc, ha='center', va='center', color='#94a3b8', fontsize=8.5, transform=ax.transAxes)
        
    ax.text(0.5, 0.14, "Streamlit Dashboard: http://localhost:8501 | Geliştiriciler: Ahmet Gün, Gülsüm Çelik, Sefa Şahin, Yusuf Alataş", 
            ha='center', va='center', color='#64748b', fontsize=10, transform=ax.transAxes)
    
    ax.axis('off')
    plt.tight_layout()
    fig.savefig(preview_path)
    plt.close(fig)
    print("Alternatif dashboard afişi oluşturuldu.")

print("\nTüm görseller assets/ klasöründe başarıyla hazırlandı!")
