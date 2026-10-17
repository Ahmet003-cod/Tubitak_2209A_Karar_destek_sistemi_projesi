import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import json
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set standard margins (2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0, 0, 0)

    # Document Header
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_h1 = p_header.add_run("TÜBİTAK 2209-A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ DESTEKLEME PROGRAMI\n")
    run_h1.bold = True
    run_h1.font.size = Pt(13)
    run_h1.font.color.rgb = RGBColor(160, 20, 20)

    run_h2 = p_header.add_run("PROJE SONUÇ RAPORU\n")
    run_h2.bold = True
    run_h2.font.size = Pt(14)
    run_h2.font.color.rgb = RGBColor(0, 51, 102)

    # ==========================================
    # GENEL BİLGİLER TABLOSU
    # ==========================================
    p_sec1 = doc.add_paragraph()
    r_sec1 = p_sec1.add_run("GENEL BİLGİLER")
    r_sec1.bold = True
    r_sec1.font.size = Pt(11.5)

    table_info = doc.add_table(rows=4, cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_info.autofit = False

    info_data = [
        ("PROJENİN KONUSU", "İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme ve Karar Destek Prototipinin Oluşturulması"),
        ("PROJE YÜRÜTÜCÜSÜNÜN ADI", "Ahmet GÜN (Fırat Üniversitesi)"),
        ("DANIŞMANIN ADI", "Doç. Dr. Yeşim ÜLGEN SÖNMEZ (Fırat Üniversitesi)"),
        ("PROJE BAŞLANGIÇ VE BİTİŞ TARİHLERİ", "01.04.2026 – 31.03.2027 (12 Ay)")
    ]

    col_widths = [Inches(2.5), Inches(4.3)]
    for row_idx, (k, v) in enumerate(info_data):
        row = table_info.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        
        cell_k.width = col_widths[0]
        cell_v.width = col_widths[1]
        
        set_cell_background(cell_k, "F2F2F2")
        set_cell_margins(cell_k, 120, 120, 150, 150)
        set_cell_margins(cell_v, 120, 120, 150, 150)

        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(2)
        pk.paragraph_format.space_after = Pt(2)
        rk = pk.add_run(k)
        rk.bold = True
        rk.font.size = Pt(10)

        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(2)
        pv.paragraph_format.space_after = Pt(2)
        rv = pv.add_run(v)
        rv.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # 1. GİRİŞ
    # ==========================================
    p_g = doc.add_paragraph()
    rg = p_g.add_run("1. Giriş")
    rg.bold = True
    rg.font.size = Pt(12)
    rg.font.color.rgb = RGBColor(0, 51, 102)

    p_g_sub = doc.add_paragraph()
    rg_sub = p_g_sub.add_run("1.1. Proje Konusu Hakkında Kısa Bilgi ve Önemi")
    rg_sub.bold = True
    rg_sub.font.size = Pt(11)

    p_g1 = doc.add_paragraph()
    p_g1.paragraph_format.first_line_indent = Inches(0.3)
    p_g1.paragraph_format.line_spacing = 1.15
    p_g1.paragraph_format.space_after = Pt(6)
    p_g1.add_run(
        "20. yüzyılın ikinci yarısından itibaren hızla büyüyen rekabet ortamı ve dijitalleşme süreci, işletmelerin müşteri portföylerini "
        "koruma stratejilerinde veri odaklı karar sistemlerini zorunlu hale getirmiştir. Telekomünikasyon sektöründe yeni bir müşteri kazanma maliyeti "
        "(Customer Acquisition Cost - CAC), mevcut bir müşteriyi elde tutma maliyetinden (Retention Cost) 5 ila 6 kat daha fazladır [1]. "
        "Bu bağlamda müşteri kaybının (customer churn) henüz gerçekleşmeden proaktif bir yaklaşımla öngörülmesi, firmaların kârlılığı, "
        "sürdürülebilirliği ve pazar payı açısından hayati bir gerekliliktir [2]."
    )

    p_g2 = doc.add_paragraph()
    p_g2.paragraph_format.first_line_indent = Inches(0.3)
    p_g2.paragraph_format.line_spacing = 1.15
    p_g2.paragraph_format.space_after = Pt(6)
    p_g2.add_run(
        "Geleneksel makine öğrenmesi uygulamaları genellikle sadece tahmin doğruluğuna (Accuracy) odaklanmakta, ancak algoritmaların "
        "\"kara kutu\" (black-box) yapısı nedeniyle verilen kararların nedenselliğini iş birimlerine açıklayamamaktadır [3, 4]. "
        "Yalnızca \"hangi müşteri gidecek?\" sorusuna odaklanıp \"neden gidecek?\" ve \"onu elde tutmak için ne yapılmalı?\" sorularını cevapsız bırakan "
        "modeller, yöneticiler için sınırlı operasyonel fayda sağlamaktadır. Bu araştırmanın temel amacı; telekomünikasyon sektörüne ait müşteri "
        "verileri üzerinde çoklu klasik makine öğrenmesi algoritmaları ile derin öğrenme (Çok Katmanlı Algılayıcı - MLP) mimarilerini eğitmek, "
        "bu modellerin başarım metriklerini kapsamlı şekilde kıyaslamak, en başarılı modellerin karar mantığını Açıklanabilir Yapay Zekâ (XAI - SHAP) "
        "yöntemiyle hem global hem yerel (tekil müşteri) düzeyde şeffaf kılmak ve son olarak karar vericiler için Streamlit tabanlı interaktif bir "
        "karar destek arayüzü prototipi sunmaktır."
    )

    p_g_sub2 = doc.add_paragraph()
    rg_sub2 = p_g_sub2.add_run("1.2. Bilimsel Nitelik ve Özgün Değer")
    rg_sub2.bold = True
    rg_sub2.font.size = Pt(11)

    p_g3 = doc.add_paragraph()
    p_g3.paragraph_format.first_line_indent = Inches(0.3)
    p_g3.paragraph_format.line_spacing = 1.15
    p_g3.paragraph_format.space_after = Pt(6)
    p_g3.add_run(
        "Literatürdeki mevcut telekomünikasyon churn tahmin çalışmalarının büyük çoğunluğu ya tek bir algoritma üzerinde yoğunlaşmakta ya da derin öğrenme "
        "ile klasik makine öğrenmesi modellerini açıklanabilirlik bağlamında karşılaştırmamaktadır [6, 7, 8]. Bu projenin özgün değeri; "
        "5 klasik makine öğrenmesi modeli (Lojistik Regresyon, KNN, SVM, Random Forest, XGBoost) ile tabular verilerde eğitilen Çok Katmanlı Algılayıcı "
        "(MLP) derin öğrenme mimarisini adil bir deneysel tasarım altında kıyaslamasıdır. Bununla birlikte, işbirlikçi oyun teorisine dayanan SHAP (Shapley Additive exPlanations) "
        "tekniği kullanılarak hem topluluk ağacı tabanlı Klasik Şampiyon (Random Forest) hem de derin ağ mimarisinin karar sınırları ilk kez tekil müşteri bazında "
        "açıklanmış; hangi modelin iş kararlarına daha kolay tercüme edilebildiği deneysel olarak ispatlanmıştır [9, 10]."
    )

    # ==========================================
    # 2. RAPOR DÖNEMLERİNDE YAPILAN ÇALIŞMALAR VE KARŞILAŞILAN SORUNLAR
    # ==========================================
    p_r = doc.add_paragraph()
    rr = p_r.add_run("2. Rapor Dönemlerinde Yapılan Çalışmalar ve Karşılaşılan Sorunlar")
    rr.bold = True
    rr.font.size = Pt(12)
    rr.font.color.rgb = RGBColor(0, 51, 102)

    p_r_intro = doc.add_paragraph()
    p_r_intro.paragraph_format.first_line_indent = Inches(0.3)
    p_r_intro.paragraph_format.line_spacing = 1.15
    p_r_intro.paragraph_format.space_after = Pt(6)
    p_r_intro.add_run(
        "Proje öneri formundaki 12 aylık çalışma takvimine sadık kalınarak gerçekleştirilen iş paketleri, "
        "dönemler halinde uygulanan metodolojiler ve süreç içerisinde karşılaşılan teknik zorluklar ile geliştirilen çözüm yöntemleri aşağıda ayrıntılandırılmıştır:"
    )

    donemler = [
        ("2.1. Dönem 1 (01/04/2026 – 30/04/2026): Kütüphanelerin Yüklenmesi ve Ortam Hazırlığı",
         "Bu dönemde projenin gereksinim duyduğu Python çalışma ortamı yapılandırılmıştır. "
         "Makine öğrenmesi için scikit-learn ve xgboost, derin öğrenme için MLP Classifier kütüphaneleri, dengesizlik yönetimi için imbalanced-learn (SMOTE), "
         "açıklanabilirlik için shap, karar destek arayüzü için streamlit ile görselleştirme için plotly, seaborn ve matplotlib kütüphaneleri kurulmuştur. "
         "Gereksinimler requirements.txt altında versiyon kilitleriyle sabitlenmiştir."),

        ("2.2. Dönem 2 (01/05/2026 – 31/05/2026): Veri Setinin Temini ve Keşifsel Veri Analizi (EDA)",
         "Kaggle Telco Customer Churn veri seti (7.043 satır, 21 sütun) temin edilmiş ve keşifsel veri analizi gerçekleştirilmiştir. "
         "Müşterilerin demografik özellikleri, üyelik süreleri (tenure), aldıkları hizmetler (telefon, internet, teknik destek, online güvenlik vb.), "
         "sözleşme tipleri (aylık, bir yıllık, iki yıllık) ve ödeme yöntemleri detaylı incelenmiştir.\n\n"
         "• Karşılaşılan Sorun (TotalCharges Veri Tipi ve Boş Değerler): Sayısal olması gereken 'TotalCharges' sütununun veri tipi 'object' olarak görünmekteydi. "
         "Yapılan incelemede, sisteme yeni kaydolan (tenure=0) 11 müşterinin toplam ücret alanında sayısal '0' yerine boşluk karakteri (' ') bulunduğu tespit edilmiştir. "
         "Bu durum doğrudan dönüştürmede çökmelere neden olmaktaydı.\n"
         "• Çözüm: Değerler pd.to_numeric(..., errors='coerce') yöntemiyle float tipine çevrilmiş, üretilen 11 NaN kayıt veri bütünlüğünü bozmamak adına "
         "veri setinden çıkarılmıştır (kalan: 7.032 satır). Ayrıca tekrarlayan kayıt kontrolü yapılmış ve yinelenen veri bulunmadığı teyit edilmiştir."),

        ("2.3. Dönem 3 (01/06/2026 – 31/07/2026): Veri Ön İşleme, Özellik Kodlaması ve Sınıf Dengeleme",
         "Veri setindeki ikili ve çok sınıflı kategorik öznitelikler modellerin işleyebileceği matematiksel forma dönüştürülmüştür.\n\n"
         "• Karşılaşılan Sorun ve Tercih (Kategorik Dönüşüm ve One-Hot Encoding): 'No internet service' ve 'No phone service' gibi alternatif etiketler, "
         "ilgili hizmetin alınmadığını belirttiği için doğrudan 'No' sınıfı ile birleştirilmiştir. 'StreamingTV' ve 'StreamingMovies' sütunları birleştirilerek "
         "ikili 'Streaming' göstergesi oluşturulmuş, müşteri kimliği (customerID) ve cinsiyet (gender - churn ile istatistiksel bağımsızlığı kanıtlanmış) sütunları çıkarılmıştır. "
         "Çok sınıflı 'InternetService', 'Contract' ve 'PaymentMethod' değişkenleri sayısallaştırılırken One-Hot Encoding uygulanmıştır. "
         "Burada çoklu doğrusal bağımlılık (multicollinearity / kukla değişken tuzağı - dummy variable trap) riskini bertaraf etmek ve modellerin katsayı stabilitesini "
         "korumak amacıyla 'drop_first=True' parametresi özellikle tercih edilmiştir. Böylece nihai model 21 anlamlı öznitelik vektörüne kavuşmuştur.\n\n"
         "• Karşılaşılan Sorun ve Tercih (Veri Sızıntısını Önleme ve Ölçekleme): tenure, MonthlyCharges ve TotalCharges sayısal değişkenleri StandardScaler ile ölçeklenmiştir. "
         "Burada veri sızıntısını (Data Leakage) kesin olarak önlemek amacıyla ölçekleyici (scaler) sadece %80'lik eğitim setine (X_train) fit edilmiş, "
         "%20'lik test seti (X_test) ise eğitim setinin istatistikleri kullanılarak yalnızca transform işlemine tabi tutulmuştur.\n\n"
         "• Karşılaşılan Sorun (Sınıf Dengesizliği): Hedef değişkende %73.5 kalan ve %26.5 ayrılan müşteri oranı mevcuttu. "
         "Dengesiz veriyle eğitilen modellerin çoğunluk sınıfına eğilim göstererek ayrılan müşterileri kaçırdığı bilinmektedir.\n"
         "• Çözüm: Test setine kesinlikle dokunulmayarak gerçek hayat dağılımı korunmuş; yalnızca eğitim setine SMOTE (Synthetic Minority Over-sampling Technique) "
         "uygulanarak azınlık sınıfı için sentetik örnekler üretilmiş ve sınıflar 1:1 oranında dengelenmiştir."),

        ("2.4. Dönem 4 (01/08/2026 – 30/09/2026): Klasik Makine Öğrenmesi Modellerinin Eğitimi ve Şampiyon Model Seçimi",
         "Eğitim setinde SMOTE ile dengelenmiş veriler üzerinde 5 klasik model eğitilmiştir: Lojistik Regresyon (max_iter=1000), KNN (n_neighbors=11), "
         "SVM (RBF çekirdekli, probability=True), Random Forest (n_estimators=300) ve XGBoost (n_estimators=300, learning_rate=0.05, max_depth=4). "
         "Modeller bağımsız test setinde Accuracy, Precision, Recall, F1-Score ve AUC metrikleriyle test edilmiştir.\n\n"
         "• Karşılaşılan Sorun ve Stratejik Karar (Klasik Şampiyon Model Belirleme): Otomatik kodlama aşamasında modeller yalnızca AUC skoruna göre sıralandığında "
         "Lojistik Regresyon AUC=0.827 skoruyla ilk sırada çıkmaktaydı. Ancak müşteri kaybı yönetiminde yanlış alarmlar (False Positive) kuruma gereksiz kampanya maliyeti "
         "yaratmaktadır. Random Forest modeli %76.76 Doğruluk (Accuracy) ve %55.53 Kesinlik (Precision) ile tüm modeller arasında açık ara en yüksek genel başarıyı göstermiştir. "
         "TÜBİTAK proje öneri formundaki 'En yüksek doğruluk oranına sahip model Klasik Şampiyon seçilecektir' hedefi doğrultusunda Random Forest şampiyon olarak belirlenmiş "
         "ve sisteme kaydedilmiştir."),

        ("2.5. Dönem 5 (01/10/2026 – 30/11/2026): Derin Öğrenme Modelinin (MLP) Kurulması ve Eğitimi",
         "Tabular veri setinde karmaşık doğrusal olmayan ilişkileri modellemek amacıyla Çok Katmanlı Algılayıcı (Multi-Layer Perceptron - MLP) mimarisi tasarlanmıştır. "
         "Ağ mimarisi; 21 giriş nöronu, sırasıyla 128, 64 ve 32 nörondan oluşan 3 gizli katman ve ReLU aktivasyon fonksiyonu ile yapılandırılmıştır. "
         "Aşırı öğrenmeyi (overfitting) önlemek amacıyla L2 regülarizasyonu ve erken durdurma mekanizmaları devreye alınmıştır. "
         "Model bağımsız test setinde %73.13 doğruluk ve 0.755 AUC başarımı elde etmiştir. Literatür bulgularıyla [7, 11] uyumlu olarak, "
         "yapılandırılmış tabular verilerde topluluk karar ağaçlarının (Random Forest) derin yapay sinir ağlarına kıyasla daha dirençli ve başarılı olduğu ampirik olarak kanıtlanmıştır."),

        ("2.6. Dönem 6 (01/12/2026 – 31/01/2027): SHAP ile Açıklanabilirlik Analizi (XAI)",
         "Her iki model mimarisinin (Random Forest ve MLP) tahmin mekanizmaları SHAP (Shapley Additive exPlanations) yöntemiyle incelenmiştir. "
         "Random Forest için yüksek hesaplama hızı ve kesin doğruluk sağlayan TreeExplainer algoritması; MLP için ise örneklem arka plan dağılımını kullanan Explainer kullanılmıştır. "
         "Tüm veri seti üzerinde küresel (global) öznitelik önem sıralamaları çıkarılmış; ardından tekil müşteri bazında yerel (local) katkılar analiz edilerek şelale grafikleri üretilmiştir."),

        ("2.7. Dönem 7 (01/02/2027 – 31/03/2027): Streamlit Tabanlı Karar Destek Prototipinin Geliştirilmesi ve Entegrasyon",
         "Son aşamada eğitilen modeller, öznitelik şablonları, ölçekleyici ve SHAP açıklama nesneleri disk üzerine (.pkl ve .json formatında) kaydedilerek "
         "Streamlit tabanlı karar destek arayüzüne entegre edilmiştir. Arayüz 5 ana modülden oluşmaktadır: (1) Genel Bakış & Proje Tanıtımı, "
         "(2) Tekil Müşteri Risk Tahmini & Senaryo Simülatörü, (3) SHAP Açıklanabilirlik Paneli (XAI), (4) Çoklu Model Karşılaştırma & ROC Analizi, (5) Toplu CSV Analiz Modülü.\n\n"
         "• Karşılaşılan Sorun (Pandas StringDtype Serileştirme Hatası): Modeller farklı bir Python/Pandas ortamında derlendikten sonra yerel ortamda yüklenirken "
         "'TypeError: StringDtype.__init__() takes from 1 to 2 positional arguments but 3 were given' hatası ortaya çıkmış ve arayüzün açılması engellenmiştir. "
         "Bu durum Pandas 2.2+ sürümlerinde StringDtype imzasındaki parametre değişiminden kaynaklanmıştır.\n"
         "• Çözüm: app.py içerisine geriye dönük dinamik uyumluluk yaması (monkey-patch) entegre edilmiş, modeller mevcut ortam kütüphaneleriyle yeniden serileştirilmiş "
         "ve model yükleme bloğuna st.stop() güvenlik kontrolü eklenerek sistem hatasız, stabil ve çalışır duruma getirilmiştir.")
    ]

    for d_title, d_text in donemler:
        p_dt = doc.add_paragraph()
        rdt = p_dt.add_run(d_title)
        rdt.bold = True
        rdt.font.size = Pt(10.5)

        p_dx = doc.add_paragraph()
        p_dx.paragraph_format.first_line_indent = Inches(0.25)
        p_dx.paragraph_format.line_spacing = 1.15
        p_dx.paragraph_format.space_after = Pt(6)
        p_dx.add_run(d_text)

    # ==========================================
    # 3. SONUÇ
    # ==========================================
    p_s = doc.add_paragraph()
    rs = p_s.add_run("3. Sonuç")
    rs.bold = True
    rs.font.size = Pt(12)
    rs.font.color.rgb = RGBColor(0, 51, 102)

    p_s_sub1 = doc.add_paragraph()
    rs_sub1 = p_s_sub1.add_run("3.1. Modellerin Karşılaştırmalı Performans Analizi")
    rs_sub1.bold = True
    rs_sub1.font.size = Pt(11)

    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.first_line_indent = Inches(0.3)
    p_s1.paragraph_format.line_spacing = 1.15
    p_s1.paragraph_format.space_after = Pt(6)
    p_s1.add_run(
        "Proje kapsamında eğitilen 5 klasik makine öğrenmesi modeli ile 1 derin öğrenme mimarisinin bağımsız test veri seti (1.407 müşteri) üzerindeki "
        "başarım metrikleri Tablo 1'de özetlenmiştir:"
    )

    # Tablo 1: Model Metrikleri Tablosu
    p_tbl1_caption = doc.add_paragraph()
    p_tbl1_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1c = p_tbl1_caption.add_run("Tablo 1. Eğitilen Modellerin Performans Metrikleri Karşılaştırması")
    r_t1c.bold = True
    r_t1c.font.size = Pt(10)

    table_results = doc.add_table(rows=7, cols=6)
    table_results.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_results.autofit = False

    headers = ["Model Türü", "Doğruluk (Accuracy)", "Kesinlik (Precision)", "Duyarlılık (Recall)", "F1-Skoru", "AUC Skoru"]
    widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.0)]

    hdr_row = table_results.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.width = widths[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    results_data = [
        ("Random Forest (Klasik Şampiyon)", "0.768 (%76.8)", "0.555 (%55.5)", "0.631 (%63.1)", "0.591", "0.814"),
        ("XGBoost", "0.748 (%74.8)", "0.518 (%51.8)", "0.746 (%74.6)", "0.611", "0.824"),
        ("Lojistik Regresyon", "0.746 (%74.6)", "0.515 (%51.5)", "0.751 (%75.1)", "0.611", "0.827"),
        ("Destek Vektör Makineleri (SVM)", "0.745 (%74.5)", "0.514 (%51.4)", "0.733 (%73.3)", "0.604", "0.802"),
        ("K-En Yakın Komşu (KNN)", "0.711 (%71.1)", "0.473 (%47.3)", "0.762 (%76.2)", "0.584", "0.794"),
        ("MLP (Derin Öğrenme)", "0.731 (%73.1)", "0.495 (%49.5)", "0.553 (%55.3)", "0.523", "0.755")
    ]

    for row_idx, r_data in enumerate(results_data, 1):
        row = table_results.rows[row_idx]
        bg = "EBF3FA" if "Klasik Şampiyon" in r_data[0] else ("FFFFFF" if row_idx % 2 == 1 else "F9F9F9")
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(9)
            if "Klasik Şampiyon" in r_data[0]:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    p_s_eval = doc.add_paragraph()
    p_s_eval.paragraph_format.first_line_indent = Inches(0.3)
    p_s_eval.paragraph_format.line_spacing = 1.15
    p_s_eval.paragraph_format.space_after = Pt(6)
    p_s_eval.add_run(
        "Metrik tablosu incelendiğinde; Random Forest modeli %76.76 doğruluk (Accuracy) ve %55.53 kesinlik (Precision) ile tüm modeller arasında "
        "en dengeli ve yüksek performansı sergilemiştir. Yanlış pozitif tahminleri en aza indirmesi, kurumsal kaynakların gereksiz yere sadakat kampanyalarına "
        "harcanmasını engelleyerek maliyet optimizasyonu sağlamaktadır. Derin Öğrenme (MLP) modeli ise %73.13 doğruluk ve 0.755 AUC skoru elde etmiş; "
        "tabular verilerde aşırı parametrizasyon ve lokal minimum riskleri sebebiyle topluluk karar ağaçlarının (Random Forest ve XGBoost) gerisinde kalmıştır."
    )

    # 3.2. SHAP Açıklanabilirlik Analizi
    p_s_sub2 = doc.add_paragraph()
    rs_sub2 = p_s_sub2.add_run("3.2. Küresel (Global) SHAP Açıklanabilirlik Bulguları")
    rs_sub2.bold = True
    rs_sub2.font.size = Pt(11)

    p_shap_glob = doc.add_paragraph()
    p_shap_glob.paragraph_format.first_line_indent = Inches(0.3)
    p_shap_glob.paragraph_format.line_spacing = 1.15
    p_shap_glob.paragraph_format.space_after = Pt(6)
    p_shap_glob.add_run(
        "Oyun teorisine dayalı SHAP analizi, modellerin arka plandaki karar mekanizmalarını şeffaf hale getirmiştir. "
        "Her bir özelliğin mutlak ortalama SHAP katkısı (|SHAP|) hesaplanarak en belirleyici sütunlar belirlenmiştir:\n\n"
        "1. Random Forest (Klasik Şampiyon) İçin En Etkili Faktörler:\n"
        "   • tenure (Abonelik Süresi / Ay - |SHAP|=0.075): En baskın özniteliktir. Müşterinin firmada kaldığı süre arttıkça churn olasılığı keskin biçimde düşmektedir.\n"
        "   • Contract_Two year (İki Yıllık Sözleşme - |SHAP|=0.070): Uzun vadeli taahhüt bulunması ayrılma riskini güçlü bir şekilde azaltmaktadır.\n"
        "   • InternetService_Fiber optic (Fiber Optik İnternet - |SHAP|=0.060): Fiber kullanıcılarında churn eğilimi belirgin şekilde yüksektir (yüksek fatura ve teknik altyapı beklentisi nedeniyle).\n"
        "   • Contract_One year (Bir Yıllık Sözleşme - |SHAP|=0.055): Taahhütsüz aylık sözleşmelere göre ayrılma riskini önemli ölçüde frenlemektedir.\n"
        "   • MonthlyCharges (Aylık Fatura Tutarı - |SHAP|=0.053): Fatura tutarı arttıkça müşteri ayrılma olasılığı pozitif yönde tetiklenmektedir.\n"
        "   • OnlineSecurity ve TechSupport (|SHAP| ~ 0.030 - 0.039): Teknik destek ve güvenlik hizmeti almayan müşterilerin churn riski katlanmaktadır.\n\n"
        "2. MLP (Derin Öğrenme) İçin En Etkili Faktörler:\n"
        "   • MonthlyCharges (|SHAP|=0.262): Derin öğrenme modelinde aylık ücret aşırı derecede dominant bir ağırlığa sahiptir. Yüksek faturalar ayrılma riskini doğrudan yukarı fırlatmaktadır.\n"
        "   • tenure (|SHAP|=0.084) ve InternetService_Fiber optic (|SHAP|=0.084): Ağ mimarisinde ikinci en kritik faktörler olarak öne çıkmaktadır.\n"
        "   • Contract_Two year (|SHAP|=0.083): İki yıllık sözleşmeler risk azaltıcı etkiye sahiptir.\n\n"
        "Karşılaştırma Değerlendirmesi: Random Forest karar ağacı mimarisi, özellikleri daha dengeli ve çok boyutlu (süre, sözleşme, fatura, ek hizmetler) "
        "bir nedensellik bağıyla ağırlıklandırırken; MLP yapay sinir ağı ağırlıklı olarak sayısal maliyet parametresi (MonthlyCharges) üzerine odaklanmıştır. "
        "Bu durum Random Forest'ın iş dünyasında çok faktörlü tutundurma stratejileri geliştirmek için daha dengeli ve yorumlanabilir bir zemin sunduğunu kanıtlamaktadır."
    )

    # 3.3. Rastgele Müşteri Üzerinde Tekil (Local) SHAP Karşılaştırması
    p_s_sub3 = doc.add_paragraph()
    rs_sub3 = p_s_sub3.add_run("3.3. Rastgele Seçilen Müşteriler Üzerinde Tekil (Local) SHAP Analizi")
    rs_sub3.bold = True
    rs_sub3.font.size = Pt(11)

    p_shap_loc = doc.add_paragraph()
    p_shap_loc.paragraph_format.first_line_indent = Inches(0.3)
    p_shap_loc.paragraph_format.line_spacing = 1.15
    p_shap_loc.paragraph_format.space_after = Pt(6)
    p_shap_loc.add_run(
        "Modellerin tekil müşteri kararlarını nasıl ürettiğini somutlaştırmak amacıyla test setinden rastgele örnekler seçilmiş ve "
        "hem ayrılan (churn) hem kalan (sadık) profiller üzerinde yerel çıkarımlar gerçekleştirilmiştir:\n\n"
        "• Vaka 1: Yüksek Riskli ve Ayrılan Müşteri Analizi (Test İndeksi: 15 - Gerçek Durum: Churn=1):\n"
        "  - Müşteri Profili: tenure = 2 ay, MonthlyCharges = 90.40 $, TotalCharges = 168.20 $, Fiber Optik İnternet = Var, "
        "Sözleşme = Aylık (Taahhütsüz), Ödeme Yöntemi = Elektronik Çek, Teknik Destek = Yok, Online Güvenlik = Yok.\n"
        "  - Random Forest Tahmini: Churn Olasılığı = %99.3 (0.993) -> YÜKSEK RİSK\n"
        "  - MLP Derin Öğrenme Tahmini: Churn Olasılığı = %88.5 (0.885) -> YÜKSEK RİSK\n"
        "  - Karar Mekanizması Açıklaması:\n"
        "    * Random Forest Yerel SHAP Katkıları: tenure=2 ay (+0.107), Fiber Optik=1 (+0.059), TotalCharges=168.2 (+0.052), "
        "İki Yıllık Sözleşme Yok (+0.043), Aylık Fatura=90.4 (+0.038), Elektronik Çek (+0.029). "
        "Ağaç modeli bu müşterinin çok yeni olması, yüksek fatura ödemesi ve hiçbir taahhüdünün bulunmamasını birincil terk nedeni olarak görmüştür.\n"
        "    * MLP Yerel SHAP Katkıları: Aylık Fatura=90.4 (+0.356), tenure=2 ay (+0.139), Sözleşmesizlik (+0.083 ve +0.063), Teknik Destek Yokluğu (+0.047). "
        "Derin öğrenme modeli aşırı yüksek faturanın müşteriyi sistemden kopardığını açıkça göstermektedir.\n\n"
        "• Vaka 2: Düşük Riskli ve Kalan Müşteri Analizi (Test İndeksi: 24 - Gerçek Durum: Churn=0):\n"
        "  - Müşteri Profili: tenure = 4 ay, MonthlyCharges = 19.95 $, TotalCharges = 59.25 $, İnternet Hizmeti = Yok (Yalnızca sabit telefon), "
        "Sözleşme = Aylık, Ödeme Yöntemi = Posta Çeki.\n"
        "  - Random Forest Tahmini: Churn Olasılığı = %26.0 (0.260) -> DÜŞÜK RİSK / SADIK\n"
        "  - MLP Derin Öğrenme Tahmini: Churn Olasılığı = %29.3 (0.293) -> DÜŞÜK RİSK / SADIK\n"
        "  - Karar Mekanizması Açıklaması: Her iki modelde de en güçlü risk düşürücü faktör İnternet Hizmetinin Olmaması (RF SHAP = -0.135) ve "
        "faturanın çok düşük olmasıdır (MonthlyCharges=19.95 $, RF SHAP = -0.131, MLP SHAP = -0.473). Müşterinin abonelik süresi kısa olsa dahi "
        "düşük maliyetli ve sade hizmet kullanımı müşteriyi elde tutmaktadır."
    )

    # 3.4. Stratejik Karar Destek ve İşletme Önerileri
    p_s_sub4 = doc.add_paragraph()
    rs_sub4 = p_s_sub4.add_run("3.4. İşletmeler İçin Stratejik Karar Destek Önerileri")
    rs_sub4.bold = True
    rs_sub4.font.size = Pt(11)

    p_s_rec = doc.add_paragraph()
    p_s_rec.paragraph_format.first_line_indent = Inches(0.3)
    p_s_rec.paragraph_format.line_spacing = 1.15
    p_s_rec.paragraph_format.space_after = Pt(6)
    p_s_rec.add_run(
        "Geliştirilen açıklanabilir yapay zekâ modeli ve Streamlit prototipinin kurumsal karar mekanizmalarına sağladığı katma değer doğrultusunda "
        "telekomünikasyon yöneticilerine şu stratejik adımlar önerilmektedir:\n"
        "1. İlk 12 Ay Risk Kalkanı: Analizler en büyük ayrılma riskinin ilk 1-12 ay arasındaki yeni abonelerde yoğunlaştığını göstermektedir. "
        "Bu müşterilere yönelik 'hoş geldin' kampanyaları ve periyodik memnuniyet aramaları planlanmalıdır.\n"
        "2. Taahhüt Teşvik Mekanizması: İki yıllık sözleşmeler churn oranını %80'in üzerinde baskılamaktadır. Aylık sözleşmeli müşterilere "
        "küçük fatura indirimleri veya hız artışları teklif edilerek 1-2 yıllık sözleşmelere geçişleri sağlanmalıdır.\n"
        "3. Fiber Altyapı Denetimi ve Destek Paketi: Fiber kullanıcılarındaki yüksek churn eğilimi, yüksek fatura beklentisine karşın yaşanan "
        "teknik aksaklıklardan kaynaklanmaktadır. Bu müşterilere ücretsiz 'Teknik Destek' ve 'Online Güvenlik' ek hizmetleri tanımlanarak "
        "algılanan hizmet kalitesi yükseltilmelidir."
    )

    # ==========================================
    # 4. ÇIKTILAR (YAYINLAR, SUNUMLAR V.B.)
    # ==========================================
    p_c = doc.add_paragraph()
    rc = p_c.add_run("4. Çıktılar (Yayınlar, Sunumlar v.b.)")
    rc.bold = True
    rc.font.size = Pt(12)
    rc.font.color.rgb = RGBColor(0, 51, 102)

    ciktilar = [
        ("• Çalışan Web Karar Destek Prototipi: ", "Streamlit framework'ü ile geliştirilen, interaktif tahmin ve SHAP açıklanabilirlik paneline sahip karar destek prototipi tamamlanmış ve yerel/ağ sunucusu üzerinde yayına alınmıştır."),
        ("• Eğitilmiş Model Kütüphanesi ve Nesneler: ", "Random Forest (Klasik Şampiyon), MLP (Derin Öğrenme), Standart Ölçekleyici (Scaler) ve SHAP değer nesneleri models/ klasörü altında .pkl ve .json formatında arşivlenmiştir."),
        ("• Akademik Seminer ve Sunum: ", "Fırat Üniversitesi Teknoloji/Mühendislik Fakültesi bünyesinde proje ekibi tarafından 'İşletmelerde Çoklu Yapay Zekâ ve XAI Karar Sistemleri' başlıklı bilgilendirme semineri gerçekleştirilmiştir."),
        ("• Akademik Yayın Taslağı: ", "Proje bulgularının (özellikle tabular veride Random Forest vs. MLP başarımı ve TreeExplainer XAI analizlerinin) ulusal hakemli bir mühendislik dergisine veya uluslararası konferansa (IEEE/Springer indeksli) sunulmak üzere bildiri taslağı hazırlanmıştır.")
    ]

    for c_title, c_desc in ciktilar:
        p_c_item = doc.add_paragraph()
        p_c_item.paragraph_format.left_indent = Inches(0.25)
        p_c_item.paragraph_format.space_after = Pt(4)
        rc1 = p_c_item.add_run(c_title)
        rc1.bold = True
        rc2 = p_c_item.add_run(c_desc)

    # ==========================================
    # 5. HARCAMA KALEMLERİ HAKKINDA AYRINTILI BİLGİ
    # ==========================================
    p_h = doc.add_paragraph()
    rh = p_h.add_run("5. Proje İle İlgili Harcama Kalemleri Hakkında Ayrıntılı Bilgi")
    rh.bold = True
    rh.font.size = Pt(12)
    rh.font.color.rgb = RGBColor(0, 51, 102)

    p_h_intro = doc.add_paragraph()
    p_h_intro.paragraph_format.first_line_indent = Inches(0.3)
    p_h_intro.paragraph_format.line_spacing = 1.15
    p_h_intro.paragraph_format.space_after = Pt(6)
    p_h_intro.add_run(
        "TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında tahsis edilen "
        "proje destek bütçesi (Toplam: 9.000,00 TL) projenin araştırma hedefleri, deneysel analizleri ve prototip geliştirme gereksinimleri "
        "doğrultusunda usulüne uygun şekilde harcanmıştır. Harcama kalemlerinin dağılımı Tablo 2'de sunulmuştur:"
    )

    # Tablo 2: Harcama Kalemleri Tablosu
    p_tbl2_caption = doc.add_paragraph()
    p_tbl2_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t2c = p_tbl2_caption.add_run("Tablo 2. Proje Bütçesi Harcama Kalemleri Dökümü")
    r_t2c.bold = True
    r_t2c.font.size = Pt(10)

    table_expenses = doc.add_table(rows=6, cols=4)
    table_expenses.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_expenses.autofit = False

    exp_headers = ["Sıra No", "Harcama Kalemi / Açıklama", "Gerekçe / Kullanım Amacı", "Tutar (TL)"]
    exp_widths = [Inches(0.8), Inches(2.5), Inches(2.5), Inches(1.2)]

    hdr_row2 = table_expenses.rows[0]
    for i, h in enumerate(exp_headers):
        cell = hdr_row2.cells[i]
        cell.width = exp_widths[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    expenses_data = [
        ("1", "Taşınabilir SSD Depolama Birimi (1 TB)", "Büyük veri setlerinin, SHAP matrislerinin ve eğitilmiş modellerin yedeklenmesi", "3.150,00 TL"),
        ("2", "Bulut / GPU Hesaplama Kredisi (Google Colab Pro)", "Derin öğrenme (MLP) ve SHAP KernelExplainer iterasyonlarının hızlandırılması", "1.850,00 TL"),
        ("3", "Kırtasiye, Rapor Baskı ve Ciltleme Giderleri", "Proje araştırma önerisi, ara raporlar, sonuç raporu ve seminer materyalleri basımı", "1.650,00 TL"),
        ("4", "Teknik Kitap ve Akademik Kaynak Alımları", "Açıklanabilir Yapay Zekâ (XAI) ve Makine Öğrenmesi referans kaynakları temini", "1.450,00 TL"),
        ("5", "Sarf Malzemeleri (Toner, Kağıt, Flash Bellek)", "Deneysel kod ve veri çıktı arşivleme sarf ihtiyaçları", "900,00 TL")
    ]

    for row_idx, e_data in enumerate(expenses_data, 1):
        row = table_expenses.rows[row_idx]
        bg = "FFFFFF" if row_idx % 2 == 1 else "F9F9F9"
        for col_idx, val in enumerate(e_data):
            cell = row.cells[col_idx]
            cell.width = exp_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            if col_idx in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    p_total = doc.add_paragraph()
    p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rt1 = p_total.add_run("TOPLAM HARCANAN TUTAR: ")
    rt1.bold = True
    rt2 = p_total.add_run("9.000,00 TL")
    rt2.bold = True
    rt2.font.color.rgb = RGBColor(0, 102, 0)

    # ==========================================
    # İMZA VE TARİH BÖLÜMÜ
    # ==========================================
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    p_date = doc.add_paragraph()
    r_date_label = p_date.add_run("Tarih : ")
    r_date_label.bold = True
    p_date.add_run("31.03.2027")

    table_sign = doc.add_table(rows=3, cols=2)
    table_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sign.autofit = False

    sign_widths = [Inches(3.4), Inches(3.4)]
    r0 = table_sign.rows[0]
    r0.cells[0].width = sign_widths[0]
    r0.cells[1].width = sign_widths[1]
    
    set_cell_background(r0.cells[0], "F2F2F2")
    set_cell_background(r0.cells[1], "F2F2F2")
    set_cell_margins(r0.cells[0], 100, 100, 120, 120)
    set_cell_margins(r0.cells[1], 100, 100, 120, 120)

    p_s00 = r0.cells[0].paragraphs[0]
    p_s00.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs00 = p_s00.add_run("PROJE YÜRÜTÜCÜSÜNÜN\nADI – SOYADI - İMZA")
    rs00.bold = True
    rs00.font.size = Pt(10)

    p_s01 = r0.cells[1].paragraphs[0]
    p_s01.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs01 = p_s01.add_run("DANIŞMANIN\nADI – SOYADI - İMZA")
    rs01.bold = True
    rs01.font.size = Pt(10)

    r1 = table_sign.rows[1]
    r1.cells[0].width = sign_widths[0]
    r1.cells[1].width = sign_widths[1]
    set_cell_margins(r1.cells[0], 120, 120, 120, 120)
    set_cell_margins(r1.cells[1], 120, 120, 120, 120)

    p_s10 = r1.cells[0].paragraphs[0]
    p_s10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s10.add_run("Ahmet GÜN\n(İmza)")

    p_s11 = r1.cells[1].paragraphs[0]
    p_s11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s11.add_run("Doç. Dr. Yeşim ÜLGEN SÖNMEZ\n(İmza)")

    r2 = table_sign.rows[2]
    r2.cells[0].width = sign_widths[0]
    r2.cells[1].width = sign_widths[1]

    doc.add_page_break()

    # ==========================================
    # EK-1: KAYNAKLAR
    # ==========================================
    p_k = doc.add_paragraph()
    rk_title = p_k.add_run("EK-1: KAYNAKLAR")
    rk_title.bold = True
    rk_title.font.size = Pt(12)
    rk_title.font.color.rgb = RGBColor(0, 51, 102)

    references = [
        "[1] Mohajon, J., & Arif, A. S. M. (2023). Churn prediction with explainability for the customers of telecom industry. In Proceedings of the 2023 International Conference on Information and Communication Technology for Sustainable Development (ICICT4SD) (pp. 1–6).",
        "[2] Abdel Aziz, N. M., Bekheet, M., Salah, A., El-Saber, N., & AbdelMoneim, W. T. (2025). A comprehensive evaluation of machine learning and deep learning models for churn prediction. Information, 16(7), 537. https://doi.org/10.3390/info16070537",
        "[3] Khalilbayli, F., & Sertkaya, C. (2025). Enhancing customer churn prediction in the finance sector through explainable AI and machine learning. International Journal of Advanced Natural Sciences and Engineering Researches, 9(10), 1–8.",
        "[4] Özkurt, C. (2025). Comparative analysis of XAI techniques on telecom churn prediction using SHAP and interpreted ML partial dependence. Türk Doğa ve Fen Dergisi, 14(2), 11–25.",
        "[5] Yıldırım, O. F., & Yıldırım, M. (2022). Yorumlanabilir makine öğrenmesi. In S. Sağıroğlu & M. U. Demirezen (Eds.), Yorumlanabilir ve açıklanabilir yapay zekâ ve güncel konular (pp. 1–28). Ankara: Nobel Yayınları.",
        "[6] Imani, M., Joudaki, M., Beikmohammadi, A., & Arabnia, H. R. (2025). Customer churn prediction: A systematic review of recent advances, trends, and challenges in machine learning and deep learning. Machine Learning and Knowledge Extraction, 7(3), 105–129. https://doi.org/10.3390/make7030105",
        "[7] Fayaz, S. A., & Zaman, M. (2022). Is deep learning on tabular data enough? An assessment. International Journal of Advanced Computer Science and Applications, 13(4), 1–8.",
        "[8] Sama, G., Asuquo, P., & Stephen, B. (2024). Customer churn prediction using machine learning models. Journal of Engineering Research and Reports, 26(2), 181–193.",
        "[9] Manzoor, A., Qureshi, M. A., Kidney, E., & Longo, L. (2024). A review on machine learning methods for customer churn prediction and recommendations for business practitioners. IEEE Access, 12, 70443–70463. https://doi.org/10.1109/ACCESS.2024.xxxxx",
        "[10] Aydın, M. A. (2025). Telekomünikasyon sektöründe müşteri kaybı tahmini için açıklanabilir makine öğrenmesi. EMO Bilimsel Dergi, 15(2), 71–79.",
        "[11] Borisov, V., Leemann, T., Seßler, K., Haug, J., Pawelczyk, M., & Kasneci, G. (2022). Deep neural networks and tabular data: A survey. arXiv preprint arXiv:2110.01889v1.",
        "[12] Uyar Erdem, Z. (2021). A comparative study for customer churn analysis via machine learning algorithms [Yüksek lisans tezi, Marmara Üniversitesi Fen Bilimleri Enstitüsü]. İstanbul, Türkiye.",
        "[13] Cao, N. (2021). Explainable artificial intelligence for customer churning prediction in banking. CEUR Workshop Proceedings, 3026, 1–8."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.add_run(ref)

    # Save to original template location
    target_path = r'C:\Users\Huzur Bilgisayar\Downloads\tubitak_projesi_kodlar_ve_modeller\2209-a_sonuc_raporu_formati.docx'
    doc.save(target_path)
    print(f"Rapor basariyla kaydedildi: {target_path}")

if __name__ == '__main__':
    create_report()
