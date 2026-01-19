import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="My Humanizer 2.5", page_icon="🚀")

# --- KOD TAMBAHAN: SOROKKAN MENU & FOOTER ---
# Kod ini akan hilangkan bar atas, titik tiga menu, dan footer "Made with Streamlit"
hide_elements_css = """
<style>
/* Sorokkan Header Atas (Termasuk butang Fork & GitHub) */
header {visibility: hidden;}

/* Sorokkan Menu Hamburger (3 titik di bucu kanan) */
#MainMenu {visibility: hidden;}

/* Sorokkan Footer Bawah */
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)
# --------------------------------------------

st.title("🚀 AI Mish Humanizer")
st.markdown("Versi terkini menggunakan model yang lebih laju.")

# 2. Setup API Key
# Dia akan cari dalam 'Secrets' dulu. Kalau tak ada, baru dia minta user masukkan.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Di Sini:", height=200, placeholder="Paste teks AI anda di sini...")

# 4. Logik Pemprosesan
if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # KEMASKINI: Guna model yang wujud dalam senarai server anda
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"""
            Rewrite the following text to bypass AI detectors like ZeroGPT.
            
            Rules:
            1. BURSTINESS: Mix short, punchy sentences with longer, complex ones. 
            2. PERPLEXITY: Use varied vocabulary. Avoid robotic words like "Moreover", "In conclusion".
            3. TONE: Natural, conversational, and slightly imperfect (human-like).
            
            Original Text:
            {text_input}
            """

            with st.spinner('Sedang memproses...'):
                response = model.generate_content(prompt)
                st.success("Siap!")
                st.subheader("Hasil:")
                st.write(response.text)
                
                # Kotak kod ini memudahkan copy-paste
                st.code(response.text, language=None)
                
        except Exception as e:
            st.error(f"Ralat: {e}")
