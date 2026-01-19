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

st.title("🎓 Academic Humanizer (Anti-Vocabulary)")
st.markdown("Versi ini mengharamkan perkataan klise AI untuk kurangkan skor ZeroGPT.")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Slider Kawalan (PENTING UNTUK LAWAN ZEROGPT)
# Default 0.9 (Agak tinggi). Kalau masih detect, naikkan ke 1.0
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
            model = genai.GenerativeModel('gemini-2.5-flash')

            # --- SENARAI PERKATAAN YANG DIHARAMKAN (AI SELALU KANTOI SEBAB INI) ---
            banned_words = """
            delve, tapestry, landscape, realm, crucial, vital, pivotal, leveraging, fostering, 
            harnessing, underscore, moreover, furthermore, in conclusion, comprehensive, 
            nuance, multifaceted, testament, game-changer, dynamic, myriad, plethora, 
            spearhead, notable, significant, in essence, ultimately.
            """

            prompt = f"""
            You are a strict academic editor. Rewrite the text below to bypass AI detection (ZeroGPT).
            
            CRITICAL INSTRUCTIONS:
            1. **VOCABULARY BAN:** You are FORBIDDEN from using these AI-cliché words: [{banned_words}]. Find simpler or more specific synonyms.
            2. **SENTENCE RHYTHM:** Do not use a consistent rhythm. Write a very short sentence. Follow it with a long, complex sentence containing multiple commas. Then another short one.
            3. **USE "WE" or "I":** If the context allows, change passive voice ("It was found") to active personal voice ("We found" or "I argue").
            4. **BE DIRECT:** Remove "fluff" adjectives. Instead of "comprehensive analysis", just say "analysis".
            5. **INTENTIONAL IMPERFECTION:** Do not try to be perfectly polished. Use slightly unusual sentence structures that a native human speaker might use.
            
            Original Text:
            {text_input}
            """

            # Guna nilai dari slider tadi
            config = genai.types.GenerationConfig(temperature=creativity)

            with st.spinner('Sedang membuang perkataan AI...'):
                response = model.generate_content(prompt, generation_config=config)
                
                st.success(f"Siap! (Tahap Kreativiti: {creativity})")
                st.write("### Hasil:")
                st.write(response.text)
                
                st.info("💡 Tips: Kalau masih detect, naikkan slider di atas ke 1.0 dan tekan butang sekali lagi.")

        except Exception as e:
            st.error(f"Ralat: {e}")
