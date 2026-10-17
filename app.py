# -*- coding: utf-8 -*-
"""
TÜBİTAK 2209-A - İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme
Streamlit Karar Destek Arayüzü Prototipi (app.py)
"""

import sys
import os

# Kullanıcı site-packages yolunu ekle (gerekirse)
USER_SITE = r"C:\Users\SEFA\AppData\Roaming\Python\Python314\site-packages"
if os.path.exists(USER_SITE) and USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)

import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# Pandas StringDtype geriye dönük pickle uyumluluk yaması
try:
    _orig_string_dtype_init = pd.StringDtype.__init__
    def _compat_string_dtype_init(self, storage=None, *args, **kwargs):
        _orig_string_dtype_init(self, storage=storage)
    pd.StringDtype.__init__ = _compat_string_dtype_init
except Exception:
    pass

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import joblib
import shap

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="TÜBİTAK 2209-A | Açıklanabilir Müşteri Kaybı Tahminleme",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODEL VE VERİ YÜKLEME ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def load_models_and_artifacts():
    if not os.path.exists(MODELS_DIR) or not os.path.exists(os.path.join(MODELS_DIR, "metadata.json")):
        st.warning("⚠️ Modeller henüz eğitilmemiş. Otomatik eğitim başlatılıyor...")
        try:
            import train_models
            train_models.train_and_save()
        except Exception as e:
            st.error(f"Eğitim hatası: {e}")

    klasik_model = joblib.load(os.path.join(MODELS_DIR, "klasik_sampiyon_model.pkl"))
    mlp_model = joblib.load(os.path.join(MODELS_DIR, "mlp_model.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    feature_names = joblib.load(os.path.join(MODELS_DIR, "feature_columns.pkl"))
    shap_data = joblib.load(os.path.join(MODELS_DIR, "shap_data.pkl"))
    test_data = joblib.load(os.path.join(MODELS_DIR, "test_data.pkl"))

    with open(os.path.join(MODELS_DIR, "metadata.json"), "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return klasik_model, mlp_model, scaler, feature_names, shap_data, test_data, metadata

try:
    klasik_model, mlp_model, scaler, feature_names, shap_data, test_data, metadata = load_models_and_artifacts()
    models_loaded = True
except Exception as e:
    st.error(f"Model yükleme hatası: {e}")
    models_loaded = False
    st.stop()

# --- ÖZEL CSS STİLLERİ ---
st.markdown("""
<style>
    /* Genel Tema Ayarları */
    .main {
        background-color: #0e1117;
    }
    .stAppHeader {
        background-color: rgba(14, 17, 23, 0.8);
    }
    
    /* Header Kartı */
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1fr solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
    }
    .tubitak-badge {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    /* Metric Kartları */
    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #38bdf8;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Risk Badges */
    .risk-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
    }
    .risk-medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid #f59e0b;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
    }
    .risk-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
    }
    
    /* Tavsiye Kutusu */
    .recommend-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-top: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- SOL YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/T%C3%9CB%C4%B0TAK_logo.svg/1200px-T%C3%9CB%C4%B0TAK_logo.svg.png", width=160)
    st.markdown("### TÜBİTAK 2209-A Projesi")
    st.markdown("**Açıklanabilir Müşteri Kaybı Tahminleme**")
    st.divider()

    st.markdown("#### ⚙️ Model Yapılandırması")
    active_model_choice = st.selectbox(
        "Aktif Tahmin Modeli:",
        [f"Klasik Şampiyon ({metadata.get('klasik_sampiyon_name', 'Random Forest')})", "MLP (Derin Öğrenme)"],
        index=0
    )
    
    risk_threshold = st.slider(
        "Risk Uyarısı Eşiği (%)",
        min_value=30, max_value=80, value=50, step=5,
        help="Bu yüzdenin üzerindeki Churn olasılıkları Yüksek Risk olarak işaretlenir."
    )
    
    st.divider()
    if models_loaded:
        st.success("✅ Modeller Yüklendi")
        st.caption(f"Öznitelik Sayısı: {len(feature_names)}")
        st.caption(f"Klasik Şampiyon: {metadata.get('klasik_sampiyon_name', 'Random Forest')}")
    else:
        st.error("❌ Modeller Hazır Değil")

# --- BAŞLIK KARTI ---
st.markdown("""
<div class="header-card">
    <span class="tubitak-badge">TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projesi</span>
    <div class="header-title">İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme</div>
    <div class="header-subtitle">Telekomünikasyon Sektöründe Müşteri Terk (Churn) Risk Analizi & SHAP (XAI) Karar Destek Karar Paneli</div>
</div>
""", unsafe_allow_html=True)

# --- SEKMELER (TABS) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Genel Bakış & Proje Tanıtımı",
    "🔮 Tekil Müşteri Risk Tahmini",
    "🧠 SHAP Açıklanabilirlik Paneli (XAI)",
    "📊 Çoklu Model Karşılaştırma",
    "📁 Toplu Müşteri Analizi (CSV)"
])

# ==============================================================================
# SEKME 1: GENEL BAKIŞ & PROJE TANITIMI
# ==============================================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">7.043</div>
            <div class="metric-label">Toplam Müşteri Verisi</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">%26,5</div>
            <div class="metric-label">Tarihsel Churn Oranı</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">6 Model</div>
            <div class="metric-label">Eğitilen Yapay Zekâ Mimarisi</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        champ_name = metadata.get('klasik_sampiyon_name', 'Random Forest')
        champ_row = next((r for r in metadata['results'] if r['Model'] == champ_name), metadata['results'][0])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">%{champ_row['Accuracy']*100:.1f}</div>
            <div class="metric-label">Şampiyon Model Doğruluğu ({champ_name})</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("### 🎯 Projenin Amacı ve Özgün Değeri")
        st.write("""
        Bu araştırma projesi, telekomünikasyon sektöründeki **müşteri kayıplarını (customer churn)** proaktif bir yaklaşımla önceden tespit etmeyi ve bu kayıpların altında yatan nedenleri **Açıklanabilir Yapay Zekâ (XAI - SHAP)** teknikleriyle şeffaf hale getirmeyi amaçlamaktadır.
        
        Geleneksel makine öğrenmesi uygulamaları genellikle yalnızca "doğruluk" skoruna odaklanmakta ve **"kara kutu" (black-box)** doğası gereği kararların neden alındığını açıklayamamaktadır. Bu proje sayesinde:
        - **Ne Olacak?**: Müşterinin ayrılma olasılığı yüksek doğrulukla tahmin edilir.
        - **Neden Olacak?**: SHAP (SHapley Additive exPlanations) yöntemiyle her bir müşterinin kararını etkileyen faktörler (yüksek fatura, kısa sözleşme, yetersiz teknik destek vb.) sayısal ve görsel olarak ortaya konur.
        - **Ne Yapılmalı?**: Elde tutma stratejileri proaktif olarak yöneticilere sunulur.
        """)
        
    with col_right:
        st.markdown("### 📈 Veri Seti Churn Dağılımı")
        # Örnek pasta grafiği
        df_pie = pd.DataFrame({'Durum': ['Kalan Müşteri (No)', 'Ayrılan Müşteri (Yes)'], 'Sayı': [5174, 1869]})
        fig_pie = px.pie(
            df_pie, names='Durum', values='Sayı',
            color='Durum',
            color_discrete_map={'Kalan Müşteri (No)': '#38bdf8', 'Ayrılan Müşteri (Yes)': '#ef4444'},
            hole=0.4
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

# ==============================================================================
# SEKME 2: TEKİL MÜŞTERİ RİSK TAHMİNİ
# ==============================================================================
with tab2:
    st.markdown("### 🔮 Tekil Müşteri Profilleme ve Anlık Risk Skoru Hesaplama")
    st.write("Aşağıdaki alanlardan müşteri verilerini girerek anlık Churn riskini hesaplayabilirsiniz.")
    
    with st.form("customer_input_form"):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("##### 👤 Abonelik Bilgileri")
            tenure = st.number_input("Abonelik Süresi (Ay):", min_value=1, max_value=72, value=12)
            contract = st.selectbox("Sözleşme Türü:", ["Aylık (Month-to-month)", "1 Yıllık (One year)", "2 Yıllık (Two year)"])
            paperless = st.selectbox("Kağıtsız Fatura:", ["Evet", "Hayır"])
            partner = st.selectbox("Eş / Partner Durumu:", ["Evet", "Hayır"])
            dependents = st.selectbox("Bakmakla Yükümlü Olduğu Kişi:", ["Evet", "Hayır"])

        with col_b:
            st.markdown("##### 💳 Finansal Durum")
            monthly_charges = st.number_input("Aylık Ücret ($):", min_value=18.0, max_value=120.0, value=75.5, step=1.0)
            total_charges = st.number_input("Toplam Ücret ($):", min_value=18.0, max_value=9000.0, value=906.0, step=10.0)
            payment_method = st.selectbox(
                "Ödeme Yöntemi:",
                ["Elektronik Çek (Electronic check)", "Posta Çeki (Mailed check)", "Banka Havalesi (Bank transfer)", "Kredi Kartı (Credit card)"]
            )
            phone_service = st.selectbox("Telefon Hizmeti:", ["Evet", "Hayır"])
            multiple_lines = st.selectbox("Çoklu Hat:", ["Evet", "Hayır"])

        with col_c:
            st.markdown("##### 🌐 İnternet ve Ek Hizmetler")
            internet_service = st.selectbox("İnternet Servisi:", ["Fiber Optic", "DSL", "Yok"])
            online_security = st.selectbox("Çevrimiçi Güvenlik Paket:", ["Evet", "Hayır"])
            tech_support = st.selectbox("Teknik Destek Paket:", ["Evet", "Hayır"])
            online_backup = st.selectbox("Çevrimiçi Yedekleme:", ["Evet", "Hayır"])
            device_protection = st.selectbox("Cihaz Koruma:", ["Evet", "Hayır"])
            streaming = st.selectbox("Yayın Servisleri (TV/Film):", ["Evet", "Hayır"])

        submit_btn = st.form_submit_button("🔍 Churn Riskini Hesapla", use_container_width=True)

    if submit_btn and models_loaded:
        # Kodlama mantığı
        input_dict = {col: 0 for col in feature_names}
        
        # Sayısal değerler
        raw_numeric = pd.DataFrame([[tenure, monthly_charges, total_charges]], columns=['tenure', 'MonthlyCharges', 'TotalCharges'])
        scaled_numeric = scaler.transform(raw_numeric)
        
        input_dict['tenure'] = scaled_numeric[0][0]
        input_dict['MonthlyCharges'] = scaled_numeric[0][1]
        input_dict['TotalCharges'] = scaled_numeric[0][2]
        
        # İkili değişkenler
        input_dict['Partner'] = 1 if partner == "Evet" else 0
        input_dict['Dependents'] = 1 if dependents == "Evet" else 0
        input_dict['PhoneService'] = 1 if phone_service == "Evet" else 0
        input_dict['MultipleLines'] = 1 if multiple_lines == "Evet" else 0
        input_dict['OnlineSecurity'] = 1 if online_security == "Evet" else 0
        input_dict['OnlineBackup'] = 1 if online_backup == "Evet" else 0
        input_dict['DeviceProtection'] = 1 if device_protection == "Evet" else 0
        input_dict['TechSupport'] = 1 if tech_support == "Evet" else 0
        input_dict['PaperlessBilling'] = 1 if paperless == "Evet" else 0
        input_dict['Streaming'] = 1 if streaming == "Evet" else 0
        
        # One-Hot Kategori Kodlama
        if internet_service == "Fiber Optic":
            input_dict['InternetService_Fiber optic'] = 1
        elif internet_service == "Yok":
            input_dict['InternetService_No'] = 1
            
        if contract == "1 Yıllık (One year)":
            input_dict['Contract_One year'] = 1
        elif contract == "2 Yıllık (Two year)":
            input_dict['Contract_Two year'] = 1
            
        if payment_method == "Posta Çeki (Mailed check)":
            input_dict['PaymentMethod_Mailed check'] = 1
        elif payment_method == "Banka Havalesi (Bank transfer)":
            input_dict['PaymentMethod_Bank transfer (automatic)'] = 1
        elif payment_method == "Kredi Kartı (Credit card)":
            input_dict['PaymentMethod_Credit card (automatic)'] = 1

        input_df = pd.DataFrame([input_dict])[feature_names]
        
        # Aktif model seçimi
        model_to_use = klasik_model if "Klasik" in active_model_choice else mlp_model
        prob = float(model_to_use.predict_proba(input_df)[0, 1])
        prob_pct = prob * 100

        st.divider()
        st.markdown("### 📊 Tahmin Sonuçları ve Risk Seviyesi")
        
        r_col1, r_col2 = st.columns([1, 1.5])
        
        with r_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_pct,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Churn Olasılığı (%)", 'font': {'size': 20, 'color': "white"}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#ef4444" if prob_pct >= risk_threshold else ("#f59e0b" if prob_pct >= 35 else "#10b981")},
                    'bgcolor': "#1e293b",
                    'bordercolor': "#334155",
                    'steps': [
                        {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.2)'},
                        {'range': [35, risk_threshold], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [risk_threshold, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': risk_threshold
                    }
                }
            ))
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with r_col2:
            if prob_pct >= risk_threshold:
                st.markdown(f"""
                <div class="risk-high">
                    🔴 YÜKSEK TERK (CHURN) RİSKİ (%{prob_pct:.1f})
                </div>
                """, unsafe_allow_html=True)
            elif prob_pct >= 35:
                st.markdown(f"""
                <div class="risk-medium">
                    🟡 ORTA RİSK (%{prob_pct:.1f})
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="risk-low">
                    🟢 DÜŞÜK RİSK (%{prob_pct:.1f}) - MÜŞTERİ SADIK
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""<div class="recommend-box">""", unsafe_allow_html=True)
            st.markdown("#### 💡 Önerilen Müşteri Elde Tutma Stratejileri:")
            recs = []
            if contract == "Aylık (Month-to-month)":
                recs.append("📌 **Sözleşme Yenileme Teklifi**: Aylık abonelikte risk yüksek. 1 Yıllık sözleşmeye geçişte %15 indirim tanımlanmalı.")
            if internet_service == "Fiber Optic" and tech_support == "Hayır":
                recs.append("📌 **Ücretsiz Teknik Destek**: Fiber abonelerinde teknik destek paketi bulunmuyor. 3 ay ücretsiz Teknik Destek tanımlanabilir.")
            if monthly_charges > 70:
                recs.append("📌 **Sadakat İndirimi**: Yüksek aylık fatura risk oluşturuyor. Sadakat puanı/fatura indirimi teklif edilebilir.")
            if tenure < 6:
                recs.append("📌 **Hoş Geldin Oryantasyonu**: Müşteri henüz ilk 6 ayında. Müşteri temsilcisi tarafından arama gerçekleştirilmeli.")
            if not recs:
                recs.append("✅ Müşteri mevcut şartlardan memnun görünmektedir. Standart kampanya bilgilendirmeleri sürdürülmelidir.")
                
            for rec in recs:
                st.write(rec)
            st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# SEKME 3: SHAP AÇIKLANABİLİRLİK PANELİ (XAI)
# ==============================================================================
with tab3:
    st.markdown("### 🧠 SHAP (SHapley Additive exPlanations) İle Model Açıklanabilirliği")
    st.write("Açıklanabilir Yapay Zekâ (XAI) modülü, modellerin neden belirli bir tahminde bulunduğunu oyun teorisine dayalı SHAP değerleri ile açıklar.")

    st.markdown("#### 1. Genel Özellik Önemi (Global Explainability)")
    st.caption("Veri setindeki tüm müşteriler genelinde Churn tahminini en çok etkileyen 15 öznitelik:")
    
    col_shap1, col_shap2 = st.columns(2)
    
    with col_shap1:
        st.markdown("**SHAP Öznitelik Etki Büyüklüğü (Bar Plot)**")
        vals = np.abs(shap_data['shap_values']).mean(axis=0)
        feature_importance = pd.DataFrame({
            'Öznitelik': shap_data['feature_names'],
            'Ortalama |SHAP Değeri|': vals
        }).sort_values('Ortalama |SHAP Değeri|', ascending=True).tail(12)
        
        fig_bar = px.bar(
            feature_importance, x='Ortalama |SHAP Değeri|', y='Öznitelik',
            orientation='h', color='Ortalama |SHAP Değeri|',
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_shap2:
        st.markdown("**SHAP Özellik Yönü & Dağılımı (Beeswarm View)**")
        fig_bee, ax = plt.subplots(figsize=(7, 5))
        shap.summary_plot(
            shap_data['shap_values'],
            shap_data['sample_data'],
            feature_names=shap_data['feature_names'],
            max_display=10,
            show=False
        )
        plt.tight_layout()
        st.pyplot(fig_bee)
        plt.close()

    st.divider()
    st.markdown("#### 2. Örnek Müşteri İçin Şelale Grafiği (Individual Waterfall Plot)")
    st.write("Aşağıdaki grafik, tek bir müşterinin Churn riskini artıran (Kırmızı) ve azaltan (Mavi) spesifik faktörleri gösterir:")
    
    sample_idx = st.slider("Örnek Müşteri İndeksi Seçin:", min_value=0, max_value=len(shap_data['sample_data'])-1, value=0)
    
    fig_wf, ax_wf = plt.subplots(figsize=(9, 4.5))
    
    exp = shap.Explanation(
        values=shap_data['shap_values'][sample_idx],
        base_values=shap_data['base_values'][sample_idx],
        data=shap_data['sample_data'].iloc[sample_idx].values,
        feature_names=shap_data['feature_names']
    )
    shap.waterfall_plot(exp, max_display=10, show=False)
    plt.tight_layout()
    st.pyplot(fig_wf)
    plt.close()

# ==============================================================================
# SEKME 4: ÇOKLU MODEL KARŞILAŞTIRMA
# ==============================================================================
with tab4:
    st.markdown("### 📊 Makine Öğrenmesi & Derin Öğrenme Modelleri Karşılaştırması")
    st.write("Eğitilen 6 farklı modelin başarım metrikleri aşağıda sunulmuştur:")

    res_df = pd.DataFrame(metadata['results']).sort_values("AUC", ascending=False)
    
    # Metrik Tablosu
    st.dataframe(
        res_df.style.highlight_max(axis=0, subset=["Accuracy", "Precision", "Recall", "F1-Score", "AUC"], color="#065f46")
        .format({"Accuracy": "{:.3f}", "Precision": "{:.3f}", "Recall": "{:.3f}", "F1-Score": "{:.3f}", "AUC": "{:.3f}"}),
        use_container_width=True
    )

    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("#### 📈 İnteraktif ROC Eğrileri")
        fig_roc = go.Figure()
        
        for name, curve in metadata['roc_curves'].items():
            fig_roc.add_trace(go.Scatter(
                x=curve['fpr'], y=curve['tpr'],
                mode='lines',
                name=name
            ))
            
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Rastgele Tahmin'))
        fig_roc.update_layout(
            title="ROC-AUC Eğrisi Karşılaştırması",
            xaxis_title="Yanlış Pozitif Oranı (FPR)",
            yaxis_title="Doğru Pozitif Oranı (TPR)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=420
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    with col_m2:
        st.markdown("#### 🧩 Karmaşıklık Matrisi (Confusion Matrix)")
        model_list = res_df['Model'].tolist()
        default_idx = model_list.index(metadata.get('klasik_sampiyon_name', 'Random Forest')) if metadata.get('klasik_sampiyon_name') in model_list else 0
        selected_cm_model = st.selectbox("Matrisi Görüntülenecek Modeli Seçin:", model_list, index=default_idx)
        cm_data = metadata['confusion_matrices'][selected_cm_model]
        
        fig_cm = px.imshow(
            cm_data,
            labels=dict(x="Tahmin Edilen Sınıf", y="Gerçek Sınıf", color="Müşteri Sayısı"),
            x=['Kalan (0)', 'Ayrılan (1)'],
            y=['Kalan (0)', 'Ayrılan (1)'],
            text_auto=True,
            color_continuous_scale='Blues'
        )
        fig_cm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420)
        st.plotly_chart(fig_cm, use_container_width=True)

# ==============================================================================
# SEKME 5: TOPLU MÜŞTERİ ANALİZİ (CSV)
# ==============================================================================
with tab5:
    st.markdown("### 📁 Toplu Müşteri Churn Risk Analizi (Batch Prediction)")
    st.write("Veri setini CSV formatında yükleyerek yüzlerce müşteri için toplu risk analizi yapabilir ve sonuçları indirebilirsiniz.")

    uploaded_file = st.file_uploader("Müşteri Listesi CSV Dosyası Yükleyin:", type=["csv"])

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        use_sample = st.button("🧪 Örnek Test Verisini Kullan")

    if uploaded_file is not None or use_sample:
        if use_sample:
            raw_data = test_data['X_test_raw'].copy()
            st.info("Örnek test verisi yüklendi (400 müşteri).")
        else:
            raw_data = pd.read_csv(uploaded_file)
            st.success(f"Yüklenen veri boyutu: {raw_data.shape[0]} satır.")

        st.markdown("#### Toplu Tahmin Çalıştırılıyor...")
        
        # Preprocess
        processed_data = test_data['X_test_scaled'].copy() if use_sample else raw_data.copy()
        
        # Batch predict
        probs = klasik_model.predict_proba(processed_data)[:, 1]
        
        results_batch = raw_data.copy()
        results_batch['Churn Olasılığı (%)'] = (probs * 100).round(1)
        results_batch['Risk Seviyesi'] = np.where(
            probs >= (risk_threshold / 100), '🔴 YÜKSEK RİSK',
            np.where(probs >= 0.35, '🟡 ORTA RİSK', '🟢 DÜŞÜK RİSK')
        )
        
        high_risk_count = (results_batch['Risk Seviyesi'] == '🔴 YÜKSEK RİSK').sum()
        
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("Analiz Edilen Müşteri", len(results_batch))
        col_b2.metric("Yüksek Riskli Müşteri", high_risk_count)
        col_b3.metric("Ortalama Churn Risk Skoru", f"%{results_batch['Churn Olasılığı (%)'].mean():.1f}")
        
        st.markdown("#### Müşteri Risk Skoru Listesi:")
        st.dataframe(results_batch[['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn Olasılığı (%)', 'Risk Seviyesi']], use_container_width=True)
        
        csv_export = results_batch.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Sonuçları CSV Olarak İndir",
            data=csv_export,
            file_name="musteri_churn_risk_raporu.csv",
            mime="text/csv"
        )

# --- FOOTER ---
st.divider()
st.caption("TÜBİTAK 2209-A Araştırma Projesi | İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme Prototipi © 2026")
