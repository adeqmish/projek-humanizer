import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Humanizer Pro Max", page_icon="🎓")

# --- KOD CSS: KEKALKAN UI BERSIH ---
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
# -----------------------------------

st.title("🎓 Academic Humanizer (Nuclear Mode)")
st.markdown("Mod ini memecahkan struktur ayat AI sepenuhnya untuk elak ZeroGPT.")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Assignment Di Sini:", height=250, placeholder="Paste perenggan demi perenggan...")

# 4. Logik Pemprosesan
if st.button("Humanize Agresif"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # --- PROMPT "NUCLEAR" (Sangat Strict) ---
            prompt = f"""
            You are a Master's degree student editing a paper. Your goal is to rewrite the text below so it CANNOT be detected as AI.
            
            Strict Instructions to beat ZeroGPT:
            1. **STRUCTURE ATTACK:** Do not just replace words. You must COMBINE two short sentences into one complex sentence, or SPLIT one long sentence into two punchy ones. Change the rhythm completely.
            2. **NO ROBOTIC TRANSITIONS:** BANNED WORDS: "Moreover," "Furthermore," "In conclusion," "It is worth noting," "Significantly," "Consequently," "Delve." If you use these, I will fail.
            3. **USE "HEDGING":** Instead of absolute facts, use phrases like "It seems plausible that," "This suggests," "One might argue that," "Data indicates."
            4. **USE FIRST PERSON PLURAL:** Where appropriate for academic context, use "We," "Our analysis," or "This paper argues" instead of strictly passive voice like "It was observed."
            5. **DENSITY:** Make the text denser and more specific. Remove fluff.
            
            Original Text to Rewrite:
            {text_input}
            """

            # Temperature 1.0 = Sangat Kreatif (Susah ZeroGPT teka)
            config = genai.types.GenerationConfig(temperature=1.0)

            with st.spinner('Sedang merombak struktur ayat...'):
                response = model.generate_content(prompt, generation_config=config)
                
                st.success("Siap! Sila semak semula.")
                st.write("### Hasil:")
                st.write(response.text)
                
                st.info("💡 Tips: Jika masih detect, cuba ubah sedikit secara manual perkataan pertama dalam setiap perenggan.")

        except Exception as e:
            st.error(f"Ralat: {e}")
