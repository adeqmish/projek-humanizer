import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Academic Humanizer Ultimate", page_icon="🎓")

# --- CSS UI BERSIH ---
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
# ---------------------

st.title("🎓 Academic Humanizer (Case Study Mode)")
st.markdown("Ubah teks kepada gaya analisis akademik (Third Person - 'Petronas/The Company').")

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
            model = genai.GenerativeModel('gemini-2.5-flash')

            banned_words = """
            delve, tapestry, landscape, realm, crucial, vital, pivotal, leveraging, fostering, 
            harnessing, underscore, moreover, furthermore, in conclusion, comprehensive, 
            nuance, multifaceted, testament, game-changer, dynamic, myriad, plethora, 
            spearhead, notable, significant, in essence, ultimately, it is important to note.
            """

            # --- PEMBAIKAN PENTING DI SINI (POINT NO. 3) ---
            prompt = f"""
            You are an academic researcher writing a case study about a company (e.g., PETRONAS). 
            Rewrite the text below to bypass AI detection (ZeroGPT) while maintaining an OBJECTIVE third-person tone.
            
            CRITICAL INSTRUCTIONS:
            1. **PERSPECTIVE SHIFT:** The original text might use "We" or "Our". You MUST change this to "Petronas", "The company", "The Group", or "Management". Do NOT use "We" or "I".
            2. **VOCABULARY BAN:** Do NOT use these AI words: [{banned_words}].
            3. **SENTENCE RHYTHM:** Mix short, direct sentences with longer, complex sentences to break the AI pattern.
            4. **ACTIVE VOICE (THIRD PERSON):** Instead of "It was decided by the company" (Passive), say "Petronas decided to" (Active). This is crucial for passing ZeroGPT.
            5. **NO MARKDOWN:** Do NOT use bold (**), italics, or bullet points. Write in standard plain text paragraphs.
            
            Original Text:
            {text_input}
            """

            with st.spinner('Sedang menukar "We" kepada "Petronas"...'):
                response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=creativity))
                
                st.success(f"Siap! (Tahap Kreativiti: {creativity})")
                
                # Kotak Copy (Tanpa Bold/Simbol)
                st.caption("Tekan ikon kertas (Copy) di bucu kanan kotak di bawah:")
                st.code(response.text, language=None)
                
                st.info("💡 Tips: Periksa semula nama khas (seperti nama projek/tempat) untuk pastikan ejaannya betul.")

        except Exception as e:
            st.error(f"Ralat: {e}")
