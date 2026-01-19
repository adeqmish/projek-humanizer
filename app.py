import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Academic Humanizer", page_icon="🎓")

# --- KOD CSS: SOROKKAN SEMUA MENU & BUTANG (Kekal Bersih) ---
hide_elements_css = """
<style>
/* Sorokkan Header Atas */
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden;}

/* Sorokkan Menu Hamburger */
#MainMenu {visibility: hidden;}

/* Sorokkan Footer Bawah */
footer {visibility: hidden;}
[data-testid="stFooter"] {visibility: hidden;}

/* Sorokkan Butang Merah & Profil Admin */
.stAppDeployButton {display: none;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)
# --------------------------------------------

st.title("🎓 Academic Humanizer")
st.markdown("Ubah teks AI kepada gaya penulisan akademik (Assignment/Thesis) yang natural.")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Assignment Di Sini:", height=250, placeholder="Paste teks AI anda di sini...")

# 4. Logik Pemprosesan
if st.button("Tukar Ke Gaya Akademik"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Guna model Gemini 2.5 Flash
            model = genai.GenerativeModel('gemini-2.5-flash')

            # --- PROMPT BARU: KHAS UNTUK AKADEMIK ---
            prompt = f"""
            You are a university student writing a high-quality academic paper. 
            Rewrite the following text to bypass AI detectors (like ZeroGPT/Turnitin) while maintaining a formal academic tone.
            
            STRICT GUIDELINES:
            1. TONE: Formal, objective, and professional. Do NOT use slang or conversational language.
            2. NO AI CLICHES: Strictly avoid overused AI phrases like "In conclusion", "It is important to note", "Delving into", "In the realm of", "Moreover", "Furthermore". Use more natural academic transitions instead.
            3. BURSTINESS: Vary your sentence structure significantly. Combine complex clauses with direct statements to break the predictable rhythm of AI text.
            4. VOCABULARY: Use precise and sophisticated vocabulary suitable for university-level work.
            
            Original Text:
            {text_input}
            """

            with st.spinner('Sedang menulis semula dengan gaya akademik...'):
                response = model.generate_content(prompt)
                st.success("Siap!")
                st.subheader("Hasil Akademik:")
                
                # Papar teks biasa sahaja (tiada kotak hitam)
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Ralat: {e}")
