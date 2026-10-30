"""
Adımlar:
    1. Gerekli kütüphanelerin import edilmesi ve streamlit sayfa ayarlarının yapılması
    2. Sayfa yüklenince geçmiş analizlerin db den yüklenmesi
    3. Dashbord istatistik kartlarının gösterilmesi
    4. Yorum formunun oluşturulması
    5. Form gönderilince Gemini analiz sonucunun yapılması ve sayfanın yeniden render edilmesi
    6. Geçmiş analizlerin gösterilmesi

Kurulum:
    1. Uygulamayı başlatmak için:
        streamlit run app.py
"""

# ============================
# 1. Gerekli kütüphanelerin import edilmesi ve streamlit sayfa ayarlarının yapılması
# ============================
import streamlit as st
from api_client import analyze_comment, get_history

st.set_page_config(
    page_title="Yapay Zeka ile Müsteri Yorum Analizi",
    page_icon="🎓",
    layout="wide"
)

# ============================
# 2. Sayfa yüklenince geçmiş analizlerin db den yüklenmesi
# ============================

def _load_from_db():
    """
    Amaç:
        FastAPI üzerinden veri tabanındaki tüm analizleri çekip session_state'e kaydet
    """
    try:
        data=get_history(limit=100)
        st.session_state.analyses = [
            {
                "comment": a["comment_text"],
                "sentiment": a["sentiment"],
                "confidence": a["confidence"],
                "explanation": a["explanation"]
            }
            for a in data.get("analyses", [])
        ]
    except Exception:
        pass

if "analyses" not in st.session_state:
    _load_from_db()

if "analyses" not in st.session_state:
    st.error("Backend bağlantısı kurulamadı")
    if st.button("Yeniden Dene"):
        st.rerun()
    st.stop()

analyses = st.session_state.analyses
total = len(analyses)
pozitif=sum(1 for a in analyses if a["sentiment"].lower() == "pozitif") 
negatif=sum(1 for a in analyses if a["sentiment"].lower() == "negatif") 
notr=total-pozitif-negatif

st.title("🎓 Yapay Zeka ile Müsteri Yorum Analizi")

# ============================
# 3. Dashbord istatistik kartlarının gösterilmesi
# ============================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Toplam", total)
col2.metric("Pozitif", pozitif)
col3.metric("Negatif", negatif)
col4.metric("Nötr", notr)

st.divider() 

left, right = st.columns([2,3])

# ============================
# 4. Yorum formunun oluşturulması
# ============================

with right:
    st.subheader("Yorum yaz")

    with st.form("comment_form", clear_on_submit=True):
        comment = st.text_area(
            label="Yorumunuzu yazınız: ",
            placeholder="Uygulamayı kullandınız mı? Kullandıysanız beğendiniz mi?",
            height=150
        )

        submitted = st.form_submit_button(
            "Gönder & Analiz Et", 
            use_container_width=True
        )

        # ============================
        # 5. Form gönderilince Gemini analiz sonucunun yapılması ve sayfanın yeniden render edilmesi
        # ============================

        if submitted:
            if not comment.strip():
                st.warning("Lütfen bir yorum giriniz")
            else: 
                with st.spinner("Gemini Analiz Ediyor..."):
                    try:
                        analyze_comment(comment.strip())
                        _load_from_db()
                        st.toast("Analiz Tamalandı")
                        st.rerun()
                    except Exception:
                        st.error("API bağlantı hatası")

# ============================
# 6. Geçmiş analizlerin gösterilmesi
# ============================

with left:
    st.subheader("Son Analizler")

    if not analyses:
        st.info("Henüz analiz yok! Sağ taraftan yorum gönderiniz")
    else:
        for a in analyses:
            sentiment = a["sentiment"].lower()
            confidence = int(a["confidence"] * 100)
            short = a["comment"][:150] + "..." if len(a["comment"])>150 else a["comment"]

            with st.container(border=True):

                if sentiment == "pozitif":
                    st.success(f"Pozitif - %{confidence} güven")
                elif sentiment == "negatif":
                    st.error(f"Negatif - %{confidence} güven")
                else:
                    st.warning(f"Nötr - %{confidence} güven")

                st.write(short)
                if a.get("explanation"):
                    st.caption(f"{a['explanation']}")