import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Academic Humanizer Ultimate", page_icon="🎓")

# --- CSS UNTUK UI BERSIH ---
hide_elements_css = """
<style>
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stFooter"] {visibility: hidden;}
.stAppDeployButton {display: none;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)
# ---------------------------

st.title("🎓 Academic Humanizer (Clean Text)")
st.markdown("Ubah teks AI kepada gaya akademik manusia (Format Teks Bersih).")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Slider Kawalan
creativity = st.slider("Tahap 'Kreativiti' (Tolak kanan jika ZeroGPT masih detect)", 
                       min_value=0.5, max_value=1.0, value=0.9, step=0.1)

# 4. Kotak Input
text_input = st.text_area("Masukkan Teks Assignment:", height=250, placeholder="Paste teks di sini...")

# 5. Logik Pemprosesan
if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Masukkan API Key dulu.")
    elif not text_input:
        st.warning("Tiada teks.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- TUKAR KEMBALI KE 1.5 FLASH (KUOTA 1,500 SEHARI) ---
            # Model ini paling stabil untuk Free Tier
            model = genai.GenerativeModel('gemini-1.5-flash')

            banned_words = """
            delve, tapestry, landscape, realm, crucial, vital, pivotal, leveraging, fostering, 
            harnessing, underscore, moreover, furthermore, in conclusion, comprehensive, 
            nuance, multifaceted, testament, game-changer, dynamic, myriad, plethora, 
            spearhead, notable, significant, in essence, ultimately, it is important to note.
            """

            # --- ARAHAN UNIVERSAL (Boleh guna untuk semua subject) ---
            prompt = f"""
            You are a strict academic editor. Rewrite the text below to bypass AI detection (ZeroGPT).
            
            CRITICAL INSTRUCTIONS:
            1. **VOCABULARY BAN:** You are FORBIDDEN from using these AI-cliché words: [{banned_words}]. Find simpler or more specific synonyms.
            2. **SENTENCE RHYTHM:** Do not use a consistent rhythm. Mix short and long sentences.
            3. **USE "WE" or "I":** Change passive voice to active personal voice where appropriate (e.g. "We found that...").
            4. **INTENTIONAL IMPERFECTION:** Do not try to be perfectly polished.
            5. **NO MARKDOWN FORMATTING:** Do NOT use bolding (**), italics (*), or headers (#). Do NOT use bullet points. Write in standard PLAIN TEXT paragraphs only.
            
            Original Text:
            {text_input}
            """

            with st.spinner('Sedang memproses...'):
                response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=creativity))
                
                st.success(f"Siap! (Tahap Kreativiti: {creativity})")
                
                # Papar dalam kotak kod (Ada butang Copy, teks bersih tanpa simbol **)
                st.caption("Tekan ikon kertas (Copy) di bucu kanan kotak di bawah:")
                st.code(response.text, language=None)
                
                st.info("💡 Tips: Kalau ZeroGPT masih detect, cuba ubah sedikit perkataan pertama setiap perenggan.")

        except Exception as e:
            st.error(f"Ralat: {e}")
