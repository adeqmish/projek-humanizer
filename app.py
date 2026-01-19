import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Academic Humanizer Pro", page_icon="🎓")

# --- KOD CSS: SOROKKAN SEMUA MENU & BUTANG ---
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
# --------------------------------------------

st.title("🎓 Academic Humanizer (Anti-ZeroGPT)")
st.markdown("Mod: **High Perplexity** (Untuk elak dikesan 100%)")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Assignment Di Sini:", height=250, placeholder="Paste teks di sini...")

# 4. Logik Pemprosesan
if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # --- RAHSIANYA ADA DI SINI ---
            prompt = f"""
            Act as a university student. Rewrite the text below to bypass AI detectors (ZeroGPT) completely.
            
            CRITICAL RULES TO AVOID DETECTION:
            1. **NO BULLET POINTS:** Write in full, cohesive paragraphs. AI loves lists; humans write paragraphs.
            2. **ACTIVE VOICE:** Use active voice (e.g., "The study analyzes...") instead of passive voice.
            3. **VARY SENTENCE LENGTH:** Start with a short sentence. Then a very long, complex one. Then a medium one. This breaks the AI pattern.
            4. **REMOVE AI WORDS:** Do NOT use words like: "Delve", "Crucial", "Vital", "Realm", "Landscape", "Furthermore", "In conclusion", "It is important to note".
            5. **ADD NUANCE:** Use hedging words like "suggests," "indicates," "might," or "arguably" instead of being 100% certain.
            
            Original Text:
            {text_input}
            """

            # Setting Temperature tinggi sikit supaya ayat lebih 'random' (Manusia)
            config = genai.types.GenerationConfig(temperature=1.0)

            with st.spinner('Sedang memerah otak supaya nampak macam student tulis...'):
                response = model.generate_content(prompt, generation_config=config)
                
                st.success("Siap! Cuba semak di ZeroGPT sekarang.")
                st.subheader("Hasil:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Ralat: {e}")
