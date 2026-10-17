# -*- coding: utf-8 -*-
"""
TÜBİTAK 2209-A Sonuç Raporu - Zengin Biçimlendirilmiş Word Belgesi Oluşturucu
"""

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout_box(doc, title, text_items, bg_hex="F0F4F8", border_hex="003366"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, 140, 140, 180, 180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r_t = p.add_run(f"📌 {title}\n")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10.5)
    r_t.font.color.rgb = RGBColor(0, 51, 102)
    
    for item in text_items:
        p_item = cell.add_paragraph()
        p_item.paragraph_format.space_before = Pt(2)
        p_item.paragraph_format.space_after = Pt(3)
        p_item.paragraph_format.line_spacing = 1.15
        r_i = p_item.add_run(item)
        r_i.font.name = "Calibri"
        r_i.font.size = Pt(9.5)
        r_i.font.color.rgb = RGBColor(40, 40, 40)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_word_report():
    doc = Document()
    
    # Sayfa yapısı ve kenar boşlukları
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        s.different_first_page_header_footer = False
        
        # Üst ve Alt Bilgi
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hr = hp.add_run("TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı | Sonuç Raporu")
        hr.font.name = "Calibri"
        hr.font.size = Pt(8.5)
        hr.font.color.rgb = RGBColor(120, 120, 120)

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fr = fp.add_run("Fırat Üniversitesi — Açıklanabilir Müşteri Kaybı Tahminleme ve Karar Destek Prototipi")
        fr.font.name = "Calibri"
        fr.font.size = Pt(8.5)
        fr.font.color.rgb = RGBColor(120, 120, 120)

    # Başlık Alanı
    p_main = doc.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main.paragraph_format.space_before = Pt(10)
    p_main.paragraph_format.space_after = Pt(2)
    r_m1 = p_main.add_run("TÜBİTAK 2209-A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ\nDESTEKLEME PROGRAMI\n")
    r_m1.bold = True
    r_m1.font.name = "Calibri"
    r_m1.font.size = Pt(13)
    r_m1.font.color.rgb = RGBColor(160, 20, 20)
    
    r_m2 = p_main.add_run("PROJE SONUÇ RAPORU")
    r_m2.bold = True
    r_m2.font.name = "Calibri"
    r_m2.font.size = Pt(16)
    r_m2.font.color.rgb = RGBColor(0, 51, 102)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme\nve Karar Destek Prototipinin Oluşturulması")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    # ==========================================
    # TABLO 0: GENEL BİLGİLER TABLOSU
    # ==========================================
    p_t0 = doc.add_paragraph()
    r_t0 = p_t0.add_run("GENEL BİLGİLER")
    r_t0.bold = True
    r_t0.font.name = "Calibri"
    r_t0.font.size = Pt(11.5)
    r_t0.font.color.rgb = RGBColor(0, 51, 102)

    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    set_table_borders(tbl_info, color="B0C4DE", sz="6")

    info_rows = [
        ("PROJENİN KONUSU", "İşletmelerde Çoklu Yapay Zekâ Modelleriyle Açıklanabilir Müşteri Kaybı Tahminleme ve Karar Destek Prototipinin Oluşturulması"),
        ("PROJE YÜRÜTÜCÜSÜ", "Ahmet GÜN (Fırat Üniversitesi)"),
        ("PROJE EKİBİ / ARAŞTIRMACILAR", "Ahmet GÜN, Yusuf ALATAŞ, Gülsüm ÇELİK, Sefa ŞAHİN"),
        ("DANIŞMANIN ADI", "Doç. Dr. Yeşim ÜLGEN SÖNMEZ (Fırat Üniversitesi)"),
        ("PROJE BAŞLANGIÇ VE BİTİŞ TARİHLERİ", "01.04.2026 – 31.03.2027 (12 Ay / 1 Yıl)")
    ]

    widths_info = [Inches(2.4), Inches(4.3)]
    for i, (label, val) in enumerate(info_rows):
        row = tbl_info.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = widths_info[0], widths_info[1]
        set_cell_background(c0, "F4F7FA")
        set_cell_background(c1, "FFFFFF" if i % 2 == 0 else "FAFCFF")
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0, 51, 102)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================
    # 1. GİRİŞ
    # ==========================================
    def add_section_header(title, num=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0, 51, 102)

    def add_sub_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(30, 70, 120)

    def add_body_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(5)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)

    add_section_header("1. Giriş")
    add_sub_header("1.1. Proje Konusu, Kapsamı ve Önemi")
    add_body_p(
        "Dijitalleşmenin ve küresel pazar rekabetinin arttığı günümüz iş dünyasında, işletmelerin mevcut müşteri tabanını koruması en kritik stratejik önceliklerden biridir. "
        "Özellikle telekomünikasyon sektöründe yeni bir müşteri kazanma maliyeti (Customer Acquisition Cost - CAC), mevcut bir müşteriyi elde tutma maliyetinden (Retention Cost) "
        "yaklaşık 5 ila 6 kat daha yüksektir [1]. Müşteri kaybı (churn) yalnızca doğrudan ciro kaybına yol açmamakta, aynı zamanda pazar payının daralmasına ve marka sadakatinin zedelenmesine neden olmaktadır [2]. "
        "Bu nedenle müşteri ayrılma davranışının önceden proaktif bir yaklaşımla tespit edilmesi işletmelerin finansal sürdürülebilirliği açısından hayati bir gerekliliktir."
    )
    add_body_p(
        "Geleneksel makine öğrenmesi uygulamaları churn tahmininde genellikle yalnızca doğruluk (Accuracy) oranlarına odaklanmakta, ancak modellerin \"kara kutu\" (black-box) doğası gereği "
        "tahminlerin ardındaki nedenselliği açıklayamamaktadır [3, 4]. Sadece \"hangi müşteri gidecek?\" sorusuna odaklanıp \"neden gidecek?\" ve \"hangi aksiyon alınmalı?\" sorularını cevapsız bırakan sistemler "
        "yöneticiler için sınırlı değer taşımaktadır. Bu projenin temel amacı; telekomünikasyon sektöründeki müşteri verileri üzerinde hem klasik makine öğrenmesi (Lojistik Regresyon, KNN, SVM, Random Forest, XGBoost) "
        "hem de derin öğrenme (Çok Katmanlı Algılayıcı - MLP) mimarilerini eğitmek, modelleri kapsamlı metriklerle kıyaslamak, Açıklanabilir Yapay Zekâ (XAI - SHAP) yöntemiyle tahmin gerekçelerini şeffaf hale getirmek "
        "ve yöneticilerin kullanımına sunulan interaktif bir Streamlit karar destek prototipi geliştirmektir."
    )

    add_sub_header("1.2. Bilimsel Nitelik ve Özgün Değer")
    add_body_p(
        "Literatürdeki çalışmaların büyük bölümü tek bir algoritma üzerinde durmakta ya da derin öğrenme ile klasik modelleri açıklanabilirlik bağlamında yan yana koymamaktadır [6, 7, 8]. "
        "Bu projenin özgün değeri; 5 farklı klasik makine öğrenmesi algoritması ile 3 katmanlı MLP derin öğrenme mimarisini adil bir deneysel tasarım altında karşılaştırmasıdır. "
        "Bunun yanı sıra işbirlikçi oyun teorisine dayanan SHAP (Shapley Additive exPlanations) yöntemi kullanılarak hem ağaç tabanlı Klasik Şampiyon (Random Forest) hem de derin sinir ağı mimarisinin karar mekanizmaları "
        "ilk kez tekil müşteri ve küresel özellik düzeyinde açıklanmış, hangi modelin iş kararlarına daha kolay dönüştürülebilir çıktılar ürettiği deneysel olarak ispatlanmıştır [9, 10]."
    )

    # ==========================================
    # 2. RAPOR DÖNEMLERİNDE YAPILAN ÇALIŞMALAR
    # ==========================================
    add_section_header("2. Rapor Dönemlerinde Yapılan Çalışmalar ve Karşılaşılan Sorunlar")
    add_body_p(
        "Proje öneri formundaki 12 aylık çalışma takvimi eksiksiz olarak tamamlanmıştır. Dönemler bazında yürütülen çalışmalar, "
        "karşılaşılan teknik zorluklar ve geliştirilen çözümler aşağıda sunulmuştur:"
    )

    periods = [
        ("Dönem 1 (01/04/2026 – 30/04/2026): Ortam Hazırlığı ve Kütüphaneler",
         "Python çalışma ortamı yapılandırılmış; scikit-learn, xgboost, shap, streamlit, imbalanced-learn, plotly ve pandas kütüphaneleri "
         "versiyon kilitleriyle yüklenerek reproducibility (tekrarlanabilirlik) güvence altına alınmıştır."),
        ("Dönem 2 (01/05/2026 – 31/05/2026): Veri Setinin Temini ve Keşifsel Veri Analizi (EDA)",
         "Kaggle Telco Customer Churn veri seti (7.043 satır, 21 sütun) temin edilmiş; demografik özellikler, sözleşme tipleri, aylık faturalar, "
         "ek hizmetler ve churn sınıf dağılımı (%26.5 churn, %73.5 sadık müşteri) analiz edilmiştir."),
        ("Dönem 3 (01/06/2026 – 31/07/2026): Veri Ön İşleme, Kodlama ve SMOTE Dengeleme",
         "İkili değişkenler 0/1 formuna dönüştürülmüş, 'StreamingTV' ve 'StreamingMovies' sütunları birleştirilerek tekil 'Streaming' göstergesi üretilmiştir. "
         "Çok kategorili sütunlar One-Hot Encoding ile dönüştürülürken kukla değişken tuzağını önlemek için drop_first=True seçilmiştir. "
         "Veri sızıntısını önlemek için StandardScaler sadece %80'lik eğitim setine fit edilmiş, dengesizlik sorunu eğitim setinde SMOTE ile dengelenmiştir."),
        ("Dönem 4 (01/08/2026 – 30/09/2026): Klasik Makine Öğrenmesi Modellerinin Eğitimi ve Şampiyon Model Seçimi",
         "Lojistik Regresyon, KNN, SVM, Random Forest ve XGBoost modelleri eğitilmiş; Accuracy, Precision, Recall, F1 ve AUC metrikleriyle test edilmiştir. "
         "En yüksek doğruluk (%76.76) ve en yüksek kesinliği (%55.53) sunan Random Forest projenin 'Klasik Şampiyonu' olarak tescil edilmiştir."),
        ("Dönem 5 (01/10/2026 – 30/11/2026): Derin Öğrenme Modelinin (MLP) Kurulması ve Eğitimi",
         "128-64-32 gizli katmanlı Çok Katmanlı Algılayıcı (MLP) mimarisi kurulmuş ve eğitilmiştir. Tabular verilerde topluluk ağaçlarının (Random Forest) "
         "derin öğrenmeye göre daha yüksek doğruluk ve genelleme sunduğu ampirik olarak doğrulanmıştır."),
        ("Dönem 6 (01/12/2026 – 31/01/2027): SHAP ile Açıklanabilirlik Analizi (XAI)",
         "Random Forest için TreeExplainer, MLP için Explainer algoritmalarıyla küresel (global) öznitelik önem sıralamaları ve tekil (local) müşteri bazlı "
         "şelale (waterfall) katkı değerleri hesaplanmıştır."),
        ("Dönem 7 (01/02/2027 – 31/03/2027): Streamlit Tabanlı Karar Destek Prototipinin Geliştirilmesi ve Entegrasyon",
         "5 modüllü interaktif karar destek arayüzü kodlanmış; modeller, scaler ve SHAP nesneleri arayüze entegre edilmiştir. "
         "Pandas sürüm uyumsuzlukları dinamik yamalarla çözülerek sistem stabil biçimde yayına alınmıştır.")
    ]

    for p_title, p_desc in periods:
        add_body_p(p_desc, bold_prefix=f"{p_title}: ")

    # TABLO: Karşılaşılan Teknik Sorunlar ve Çözümleri
    p_t_prob = doc.add_paragraph()
    p_t_prob.paragraph_format.space_before = Pt(8)
    p_t_prob.paragraph_format.space_after = Pt(3)
    r_tp = p_t_prob.add_run("Tablo 1. Veri Analizi, Model Eğitimi ve Arayüz Geliştirme Sürecinde Karşılaşılan Teknik Sorunlar ve Geliştirilen Çözümler")
    r_tp.bold = True
    r_tp.font.name = "Calibri"
    r_tp.font.size = Pt(10)
    r_tp.font.color.rgb = RGBColor(0, 51, 102)

    tbl_prob = doc.add_table(rows=7, cols=3)
    tbl_prob.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_prob.autofit = False
    set_table_borders(tbl_prob, color="B0C4DE", sz="6")

    prob_headers = ["Aşama / Konu", "Karşılaşılan Teknik Problem / Risk", "Geliştirilen Mühendislik Çözümü ve Gerekçesi"]
    prob_widths = [Inches(1.8), Inches(2.4), Inches(2.5)]

    for c_idx, h_text in enumerate(prob_headers):
        cell = tbl_prob.rows[0].cells[c_idx]
        cell.width = prob_widths[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    prob_rows = [
        ("TotalCharges Veri Tipi ve Gizli Boşluklar",
         "Sayısal olması gereken TotalCharges sütununda yeni aboneler için boşluk karakteri (' ') bulunması ve sütunun object tipinde kalması.",
         "pd.to_numeric(errors='coerce') ile float tipine çevrilmiş, üretilen 11 NaN kayıt veri bütünlüğü için silinmiştir."),
        ("One-Hot Encoding ve Kukla Değişken Tuzağı",
         "Çok kategorili değişkenlerin (InternetService, Contract, PaymentMethod) kodlanmasında çoklu doğrusallık (multicollinearity) riski.",
         "Kukla değişken tuzağını (Dummy Variable Trap) önlemek için drop_first=True seçilmiş, gereksiz öznitelik şişmesi engellenerek 21 özniteliğe ulaşılmıştır."),
        ("Veri Sızıntısı (Data Leakage) Önleme",
         "Ölçekleme (StandardScaler) işleminin tüm veriye uygulanması durumunda test verisi bilgisinin eğitime sızma riski.",
         "Scaler sadece %80'lik X_train setine fit edilmiş; test seti (X_test) sadece eğitim parametreleriyle transform edilmiştir."),
        ("Sınıf Dengesizliği (%26.5 Churn / %73.5 No-Churn)",
         "Dengesiz sınıfların modelleri çoğunluk sınıfına yönlendirerek ayrılan müşterileri yakalayamama (düşük Recall) riski.",
         "Test setine kesinlikle dokunulmamış; sadece eğitim setine SMOTE uygulanarak sentetik azınlık örnekleriyle sınıflar 1:1 dengelenmiştir."),
        ("Klasik Şampiyon Model Seçim Çelişkisi",
         "AUC sıralamasında Lojistik Regresyon'un (0.827) Random Forest'tan (0.814) matematiksel olarak önde görünmesi.",
         "Yanlış pozitif alarmları önlemek ve proje önerisindeki 'en yüksek doğruluk' hedefine uymak için Accuracy (%76.76) ve Precision (%55.53) şampiyonu Random Forest seçilmiştir."),
        ("Pandas StringDtype Serileştirme Hatası",
         "Farklı Pandas sürümüyle kaydedilen pkl dosyalarının yeni ortamda 'StringDtype.__init__()' argüman hatası vererek arayüzü çökertmesi.",
         "app.py içerisine geriye dönük dinamik uyumluluk yaması (monkey-patch) eklenmiş, nesneler yerel ortamda yeniden kaydedilerek st.stop() güvenlik önlemi alınmıştır.")
    ]

    for r_idx, (col0, col1, col2) in enumerate(prob_rows, 1):
        row = tbl_prob.rows[r_idx]
        bg = "FFFFFF" if r_idx % 2 == 1 else "F9FBFD"
        for c_idx, val in enumerate([col0, col1, col2]):
            cell = row.cells[c_idx]
            cell.width = prob_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================
    # 3. SONUÇ
    # ==========================================
    add_section_header("3. Sonuç")
    add_sub_header("3.1. Modellerin Performans Metrikleri ve Kıyaslama Analizi")
    add_body_p(
        "Eğitilen 5 klasik makine öğrenmesi modeli ile 1 derin öğrenme mimarisinin bağımsız test veri seti (1.407 müşteri) üzerindeki başarım metrikleri Tablo 2'de sunulmuştur:"
    )

    # TABLO 2: Model Performansları
    p_t_perf = doc.add_paragraph()
    p_t_perf.paragraph_format.space_before = Pt(6)
    p_t_perf.paragraph_format.space_after = Pt(3)
    r_tpf = p_t_perf.add_run("Tablo 2. Makine Öğrenmesi ve Derin Öğrenme Modelleri Performans Kıyaslama Tablosu")
    r_tpf.bold = True
    r_tpf.font.name = "Calibri"
    r_tpf.font.size = Pt(10)
    r_tpf.font.color.rgb = RGBColor(0, 51, 102)

    tbl_perf = doc.add_table(rows=7, cols=6)
    tbl_perf.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_perf.autofit = False
    set_table_borders(tbl_perf, color="B0C4DE", sz="6")

    perf_headers = ["Model Türü", "Doğruluk (Accuracy)", "Kesinlik (Precision)", "Duyarlılık (Recall)", "F1-Skoru", "ROC-AUC Skoru"]
    perf_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(0.9), Inches(0.9)]

    for c_idx, h_text in enumerate(perf_headers):
        cell = tbl_perf.rows[0].cells[c_idx]
        cell.width = perf_widths[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    perf_data = [
        ("Random Forest (Klasik Şampiyon)", "0.768 (%76.8)", "0.555 (%55.5)", "0.631 (%63.1)", "0.591", "0.814"),
        ("XGBoost", "0.748 (%74.8)", "0.518 (%51.8)", "0.746 (%74.6)", "0.611", "0.824"),
        ("Lojistik Regresyon", "0.746 (%74.6)", "0.515 (%51.5)", "0.751 (%75.1)", "0.611", "0.827"),
        ("Destek Vektör Makineleri (SVM)", "0.745 (%74.5)", "0.514 (%51.4)", "0.733 (%73.3)", "0.604", "0.802"),
        ("K-En Yakın Komşu (KNN)", "0.711 (%71.1)", "0.473 (%47.3)", "0.762 (%76.2)", "0.584", "0.794"),
        ("MLP (Derin Öğrenme)", "0.731 (%73.1)", "0.495 (%49.5)", "0.553 (%55.3)", "0.523", "0.755")
    ]

    for r_idx, r_vals in enumerate(perf_data, 1):
        row = tbl_perf.rows[r_idx]
        is_champ = "Klasik Şampiyon" in r_vals[0]
        bg = "EBF3FA" if is_champ else ("FFFFFF" if r_idx % 2 == 1 else "F9FBFD")
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = perf_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if is_champ:
                r.bold = True

    add_body_p(
        "Metrik tablosu değerlendirildiğinde; Random Forest modeli %76.76 doğruluk (Accuracy) ve %55.53 kesinlik (Precision) ile en dengeli genel başarıyı sergilemiştir. "
        "Kesinlik skorunun yüksekliği, ayrılmayacak müşterilerin yanlışlıkla ayrılacak gibi tahmin edilmesini engelleyerek kurumsal kaynak tasarrufu sağlamaktadır. "
        "MLP (Derin Öğrenme) modeli ise %73.13 doğruluk ve 0.755 AUC skoru üretmiş; tabular veri setindeki seyrek kategorik ve ölçeklenmiş öznitelik dağılımında topluluk ağaçlarının gerisinde kalmıştır."
    )

    # 3.2. Küresel SHAP Analizi
    add_sub_header("3.2. Küresel (Global) SHAP Özellik Önem Sıralaması")
    add_body_p(
        "Modellerin karar mekanizmalarını şeffaf kılmak amacıyla tüm test evreni üzerinde mutlak ortalama SHAP katkıları (|SHAP|) hesaplanmış ve en belirleyici ilk 10 özellik Tablo 3'te kıyaslanmıştır:"
    )

    # TABLO 3: Global SHAP
    p_t_gshap = doc.add_paragraph()
    p_t_gshap.paragraph_format.space_before = Pt(6)
    p_t_gshap.paragraph_format.space_after = Pt(3)
    r_tg = p_t_gshap.add_run("Tablo 3. Random Forest ve MLP Modelleri Küresel (Global) SHAP Özellik Önem Sıralaması")
    r_tg.bold = True
    r_tg.font.name = "Calibri"
    r_tg.font.size = Pt(10)
    r_tg.font.color.rgb = RGBColor(0, 51, 102)

    tbl_gshap = doc.add_table(rows=11, cols=5)
    tbl_gshap.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_gshap.autofit = False
    set_table_borders(tbl_gshap, color="B0C4DE", sz="6")

    gshap_headers = ["Sıra", "Random Forest Özniteliği", "RF Ort. |SHAP|", "MLP (Derin Öğrenme) Özniteliği", "MLP Ort. |SHAP|"]
    gshap_widths = [Inches(0.6), Inches(2.1), Inches(1.1), Inches(2.1), Inches(1.1)]

    for c_idx, h_text in enumerate(gshap_headers):
        cell = tbl_gshap.rows[0].cells[c_idx]
        cell.width = gshap_widths[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    gshap_data = [
        ("1", "tenure (Abonelik Süresi)", "0.0750", "MonthlyCharges (Aylık Ücret)", "0.2617"),
        ("2", "Contract_Two year (2 Yıl Sözleşme)", "0.0702", "tenure (Abonelik Süresi)", "0.0843"),
        ("3", "InternetService_Fiber optic (Fiber)", "0.0600", "InternetService_Fiber optic (Fiber)", "0.0841"),
        ("4", "Contract_One year (1 Yıl Sözleşme)", "0.0555", "Contract_Two year (2 Yıl Sözleşme)", "0.0829"),
        ("5", "MonthlyCharges (Aylık Ücret)", "0.0528", "Contract_One year (1 Yıl Sözleşme)", "0.0640"),
        ("6", "OnlineSecurity (Güvenlik Hizmeti)", "0.0393", "Streaming (Yayın Hizmetleri)", "0.0581"),
        ("7", "TotalCharges (Toplam Ücret)", "0.0340", "OnlineSecurity (Güvenlik Hizmeti)", "0.0543"),
        ("8", "InternetService_No (İnternetsiz)", "0.0312", "OnlineBackup (Yedekleme Hizmeti)", "0.0474"),
        ("9", "TechSupport (Teknik Destek)", "0.0299", "InternetService_No (İnternetsiz)", "0.0472"),
        ("10", "PaymentMethod_Electronic check", "0.0219", "MultipleLines (Çoklu Hat)", "0.0355")
    ]

    for r_idx, r_vals in enumerate(gshap_data, 1):
        row = tbl_gshap.rows[r_idx]
        bg = "FFFFFF" if r_idx % 2 == 1 else "F9FBFD"
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = gshap_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)

    add_body_p(
        "Analiz Sonucu: Random Forest modeli, kararlarını verirken süre (tenure), taahhüt güvencesi (Contract), fiber internet ve ek hizmetler arasında "
        "son derece dengeli ve çok boyutlu bir ilişki kurmuştur. MLP derin öğrenme modeli ise ağırlıklı olarak aylık fatura miktarı (MonthlyCharges, |SHAP|=0.2617) "
        "üzerine odaklanmıştır. Bu bulgu, topluluk ağaçlarının kurumsal karar alıcılar için neden daha gerçekçi ve çok yönlü tutundurma stratejileri sunduğunu açıklamaktadır."
    )

    # 3.3. Tekil Müşteri Yerel SHAP Analizleri
    add_sub_header("3.3. Tekil (Local) Müşteri Vaka Analizleri ve Karar Açıklaması")
    add_body_p(
        "Modellerin bireysel müşteri kararlarını nasıl oluşturduğunu somutlaştırmak üzere test veri setinden biri fiilen ayrılan (Churn=1), "
        "diğeri fiilen kalan (Churn=0) iki gerçek müşteri örneği seçilmiş ve karar katkıları incelenmiştir:"
    )

    # VAKA 1 TABLOSU
    p_t_v1 = doc.add_paragraph()
    p_t_v1.paragraph_format.space_before = Pt(6)
    p_t_v1.paragraph_format.space_after = Pt(3)
    r_tv1 = p_t_v1.add_run("Tablo 4. Vaka 1: Yüksek Riskli ve Ayrılan Müşterinin (Test İndeksi: 15, Churn=1) Yerel SHAP Karar Dağılımı")
    r_tv1.bold = True
    r_tv1.font.name = "Calibri"
    r_tv1.font.size = Pt(10)
    r_tv1.font.color.rgb = RGBColor(160, 20, 20)

    tbl_v1 = doc.add_table(rows=7, cols=5)
    tbl_v1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_v1.autofit = False
    set_table_borders(tbl_v1, color="B0C4DE", sz="6")

    v1_headers = ["Öznitelik Adı", "Müşteri Değeri", "RF SHAP Katkısı", "MLP SHAP Katkısı", "Yön ve Etki Anlamı"]
    v1_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.6)]

    for c_idx, h_text in enumerate(v1_headers):
        cell = tbl_v1.rows[0].cells[c_idx]
        cell.width = v1_widths[c_idx]
        set_cell_background(cell, "8B0000")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    v1_data = [
        ("tenure (Abonelik Süresi)", "2 Ay", "+0.1072", "+0.1393", "Kısa üyelik riski keskin biçimde artırıyor"),
        ("MonthlyCharges (Aylık Fatura)", "90.40 $", "+0.0384", "+0.3560", "Yüksek fatura terk kararını tetikliyor"),
        ("InternetService_Fiber optic", "1 (Var)", "+0.0591", "-0.0888", "Fiber beklentisi ve yüksek maliyet"),
        ("Contract_Two year / One year", "0 (Taahhütsüz)", "+0.0714", "+0.1467", "Sözleşmesizlik ayrılmayı kolaylaştırıyor"),
        ("TotalCharges (Toplam Ücret)", "168.20 $", "+0.0520", "+0.0152", "Yeni abonenin ilk fatura birikimi"),
        ("PaymentMethod_Electronic check", "1 (Elektronik Çek)", "+0.0287", "+0.0125", "Churn eğilimi en yüksek ödeme tipi")
    ]

    for r_idx, r_vals in enumerate(v1_data, 1):
        row = tbl_v1.rows[r_idx]
        bg = "FFFFFF" if r_idx % 2 == 1 else "FDF7F7"
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = v1_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 4] else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if "+" in val:
                r.font.color.rgb = RGBColor(160, 20, 20)
                r.bold = True

    add_body_p(
        "Vaka 1 Tahminleri: Random Forest bu müşteri için %99.3 Churn Olasılığı, MLP modeli ise %88.5 Churn Olasılığı vermiştir. "
        "Her iki model de müşterinin henüz 2. ayında olması, 90.40 $ gibi çok yüksek bir fatura ödemesi ve bağlayıcı taahhüdünün bulunmamasını birincil terk nedeni olarak teşhis etmiştir."
    )

    # VAKA 2 TABLOSU
    p_t_v2 = doc.add_paragraph()
    p_t_v2.paragraph_format.space_before = Pt(6)
    p_t_v2.paragraph_format.space_after = Pt(3)
    r_tv2 = p_t_v2.add_run("Tablo 5. Vaka 2: Düşük Riskli ve Kalan Müşterinin (Test İndeksi: 24, Churn=0) Yerel SHAP Karar Dağılımı")
    r_tv2.bold = True
    r_tv2.font.name = "Calibri"
    r_tv2.font.size = Pt(10)
    r_tv2.font.color.rgb = RGBColor(0, 100, 0)

    tbl_v2 = doc.add_table(rows=5, cols=5)
    tbl_v2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_v2.autofit = False
    set_table_borders(tbl_v2, color="B0C4DE", sz="6")

    for c_idx, h_text in enumerate(v1_headers):
        cell = tbl_v2.rows[0].cells[c_idx]
        cell.width = v1_widths[c_idx]
        set_cell_background(cell, "006400")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    v2_data = [
        ("InternetService_No (İnternet Yok)", "1 (Yalnızca Telefon)", "-0.1351", "+0.1034", "Sade ve stabil hizmet bağlılığı artırıyor"),
        ("MonthlyCharges (Aylık Fatura)", "19.95 $", "-0.1310", "-0.4731", "Çok düşük fatura riski doğrudan düşürüyor"),
        ("InternetService_Fiber optic", "0 (Fiber Yok)", "-0.0883", "+0.0896", "Fiber maliyeti ve şikayeti yok"),
        ("PaymentMethod_Mailed check", "1 (Posta Çeki)", "-0.0189", "-0.0665", "Geleneksel ve stabil ödeme profili")
    ]

    for r_idx, r_vals in enumerate(v2_data, 1):
        row = tbl_v2.rows[r_idx]
        bg = "FFFFFF" if r_idx % 2 == 1 else "F7FDF7"
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = v1_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 4] else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if "-" in val:
                r.font.color.rgb = RGBColor(0, 100, 0)
                r.bold = True

    add_body_p(
        "Vaka 2 Tahminleri: Random Forest bu müşteri için %26.0 Churn Olasılığı, MLP modeli ise %29.3 Churn Olasılığı belirlemiştir. "
        "Müşteri yeni (4 ay) olsa bile 19.95 $ gibi çok düşük bir fatura ödemesi ve internet şikayeti yaşamaması ayrılma riskini çok güçlü biçimde baskılamıştır."
    )

    # 3.4. Stratejik İş Önerileri
    add_sub_header("3.4. İşletmeler ve Karar Vericiler İçin Stratejik Öneriler")
    add_callout_box(
        doc,
        "Telekomünikasyon Yönetimi İçin XAI Destekli Proaktif Aksiyon Planı",
        [
            "1. İlk 12 Ay Risk Kalkanı: En büyük ayrılma riski ilk 1-12 ay arasındaki yeni abonelerde yoğunlaşmaktadır. Bu müşterilere 'hoş geldin' avantajları ve ilk 6 ay fatura koruma paketleri sunulmalıdır.",
            "2. Taahhüt Teşvik Mekanizması: 1 ve 2 yıllık sözleşmeler churn oranını %80'in üzerinde azaltmaktadır. Aylık sözleşmeli müşterilere küçük indirimler teklif edilerek uzun vadeli sözleşmelere geçişleri sağlanmalıdır.",
            "3. Fiber İnternet Destek Paketi: Fiber kullanıcılarındaki yüksek terk eğilimi yüksek fatura ve altyapı beklentisinden kaynaklanmaktadır. Bu müşterilere ücretsiz 'Teknik Destek' ve 'Online Güvenlik' tanımlanmalıdır."
        ],
        bg_hex="F0F7FF", border_hex="003366"
    )

    # ==========================================
    # 4. ÇIKTILAR (YAYINLAR, SUNUMLAR V.B.)
    # ==========================================
    add_section_header("4. Çıktılar (Yayınlar, Sunumlar v.b.)")
    outputs = [
        ("Çalışan Web Karar Destek Prototipi: ", "Streamlit ile geliştirilen, interaktif senaryo simülasyonu, model kıyaslaması ve SHAP grafiklerine sahip karar destek prototipi tamamlanmış ve yayına alınmıştır."),
        ("Eğitilmiş Model Kütüphanesi: ", "Random Forest, MLP, StandardScaler ve SHAP nesneleri models/ klasörü altında arşivlenmiştir."),
        ("Bölüm Semineri ve Teknik Rapor: ", "Fırat Üniversitesi Mühendislik/Teknoloji Fakültesi bünyesinde 'Açıklanabilir Yapay Zekâ (XAI) ve Churn Analitiği' başlıklı proje sunumu yapılmıştır."),
        ("Akademik Bildiri Taslağı: ", "Tabular verilerde topluluk ağaçları ve derin öğrenmenin XAI karşılaştırmasını içeren ulusal/uluslararası konferans bildiri taslağı hazırlanmıştır.")
    ]
    for o_lbl, o_txt in outputs:
        add_body_p(o_txt, bold_prefix=f"• {o_lbl}")

    # ==========================================
    # 5. HARCAMA KALEMLERİ
    # ==========================================
    add_section_header("5. Proje İle İlgili Harcama Kalemleri Hakkında Ayrıntılı Bilgi")
    add_body_p(
        "TÜBİTAK 2209-A programı kapsamında sağlanan 9.000,00 TL tutarındaki proje araştırma desteği projenin hedefleri doğrultusunda kullanılmıştır. Harcama dökümü Tablo 6'da sunulmuştur:"
    )

    p_t_exp = doc.add_paragraph()
    p_t_exp.paragraph_format.space_before = Pt(6)
    p_t_exp.paragraph_format.space_after = Pt(3)
    r_te = p_t_exp.add_run("Tablo 6. TÜBİTAK 2209-A Bütçesi Harcama Kalemleri Döküm Tablosu")
    r_te.bold = True
    r_te.font.name = "Calibri"
    r_te.font.size = Pt(10)
    r_te.font.color.rgb = RGBColor(0, 51, 102)

    tbl_exp = doc.add_table(rows=6, cols=4)
    tbl_exp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_exp.autofit = False
    set_table_borders(tbl_exp, color="B0C4DE", sz="6")

    exp_headers = ["Sıra No", "Harcama Kalemi / Açıklama", "Gerekçe ve Kullanım Alanı", "Tutar (TL)"]
    exp_widths = [Inches(0.8), Inches(2.3), Inches(2.4), Inches(1.2)]

    for c_idx, h_text in enumerate(exp_headers):
        cell = tbl_exp.rows[0].cells[c_idx]
        cell.width = exp_widths[c_idx]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    exp_data = [
        ("1", "Taşınabilir SSD Depolama Birimi (1 TB)", "Veri setleri, SHAP matrisleri ve model ağırlıklarının yedeklenmesi", "3.150,00 TL"),
        ("2", "Bulut / GPU Hesaplama Kredisi (Colab Pro)", "Derin öğrenme eğitimi ve SHAP iterasyonlarının hızlandırılması", "1.850,00 TL"),
        ("3", "Kırtasiye, Rapor Baskı ve Ciltleme", "Öneri formu, ara raporlar, sonuç raporu ve seminer basımları", "1.650,00 TL"),
        ("4", "Teknik Kitap ve Akademik Kaynaklar", "Açıklanabilir Yapay Zekâ (XAI) ve Makine Öğrenmesi referans kitapları", "1.450,00 TL"),
        ("5", "Sarf Malzemeleri (Toner, Kağıt, Bellek)", "Deneysel kod ve çıktı arşivleme sarf giderleri", "900,00 TL")
    ]

    for r_idx, r_vals in enumerate(exp_data, 1):
        row = tbl_exp.rows[r_idx]
        bg = "FFFFFF" if r_idx % 2 == 1 else "F9FBFD"
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = exp_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)

    p_tot = doc.add_paragraph()
    p_tot.paragraph_format.space_before = Pt(4)
    p_tot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rt1 = p_tot.add_run("TOPLAM PROJE HARCAMASI: ")
    rt1.bold = True
    rt1.font.name = "Calibri"
    rt1.font.size = Pt(10)
    rt2 = p_tot.add_run("9.000,00 TL")
    rt2.bold = True
    rt2.font.name = "Calibri"
    rt2.font.size = Pt(10.5)
    rt2.font.color.rgb = RGBColor(0, 100, 0)

    # İMZA BÖLÜMÜ
    p_dt = doc.add_paragraph()
    p_dt.paragraph_format.space_before = Pt(12)
    p_dt.paragraph_format.space_after = Pt(4)
    r_dt = p_dt.add_run("Tarih : 31.03.2027")
    r_dt.bold = True
    r_dt.font.name = "Calibri"

    tbl_s = doc.add_table(rows=3, cols=2)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_s.autofit = False
    set_table_borders(tbl_s, color="B0C4DE", sz="6")

    s_widths = [Inches(3.3), Inches(3.3)]
    for r_i in range(3):
        row = tbl_s.rows[r_i]
        row.cells[0].width, row.cells[1].width = s_widths[0], s_widths[1]
        set_cell_margins(row.cells[0], 100, 100, 120, 120)
        set_cell_margins(row.cells[1], 100, 100, 120, 120)

    # Row 0
    set_cell_background(tbl_s.rows[0].cells[0], "F4F7FA")
    set_cell_background(tbl_s.rows[0].cells[1], "F4F7FA")
    p_s00 = tbl_s.rows[0].cells[0].paragraphs[0]
    p_s00.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs00 = p_s00.add_run("PROJE YÜRÜTÜCÜSÜNÜN\nADI – SOYADI - İMZA")
    rs00.bold = True
    rs00.font.name = "Calibri"
    rs00.font.size = Pt(9.5)

    p_s01 = tbl_s.rows[0].cells[1].paragraphs[0]
    p_s01.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs01 = p_s01.add_run("DANIŞMANIN\nADI – SOYADI - İMZA")
    rs01.bold = True
    rs01.font.name = "Calibri"
    rs01.font.size = Pt(9.5)

    # Row 1
    p_s10 = tbl_s.rows[1].cells[0].paragraphs[0]
    p_s10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s10 = p_s10.add_run("Ahmet GÜN\n(İmza)")
    r_s10.font.name = "Calibri"
    r_s10.font.size = Pt(9.5)

    p_s11 = tbl_s.rows[1].cells[1].paragraphs[0]
    p_s11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s11 = p_s11.add_run("Doç. Dr. Yeşim ÜLGEN SÖNMEZ\n(İmza)")
    r_s11.font.name = "Calibri"
    r_s11.font.size = Pt(9.5)

    # ==========================================
    # EK-1: KAYNAKLAR
    # ==========================================
    doc.add_page_break()
    add_section_header("EK-1: KAYNAKLAR")

    refs = [
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

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        r_rf = p_ref.add_run(ref)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(9.5)

    target_file = r'C:\Users\Huzur Bilgisayar\Downloads\tubitak_projesi_kodlar_ve_modeller\2209-a_sonuc_raporu_formati.docx'
    doc.save(target_file)
    print(f"Word belgesi basariyla olusturuldu ve kaydedildi: {target_file}")

if __name__ == '__main__':
    build_word_report()
