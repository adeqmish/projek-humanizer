import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="My Humanizer 2.5", page_icon="🚀")

# --- KOD CSS: SOROKKAN SEMUA MENU & BUTANG ---
hide_elements_css = """
<style>
/* Sorokkan Header Atas (Termasuk butang Fork & GitHub) */
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden;}

/* Sorokkan Menu Hamburger (3 titik di bucu kanan) */
#MainMenu {visibility: hidden;}

/* Sorokkan Footer Bawah (Made with Streamlit) */
footer {visibility: hidden;}
[data-testid="stFooter"] {visibility: hidden;}

/* Sorokkan Butang Merah 'Manage App' & Profil Admin */
.stAppDeployButton {display: none;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)
# --------------------------------------------

st.title("🚀 AI Mish Humanizer")
st.markdown("Versi terkini menggunakan model yang lebih laju.")

# 2. Setup API Key
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
            
            # Guna model Gemini 2.5 Flash
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
                
                # --- HANYA TEKS BIASA (Kotak Gelap Dah Dibuang) ---
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Ralat: {e}")
