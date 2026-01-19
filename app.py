import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="My Humanizer", page_icon="🤖")

st.title("🤖 AI Text Humanizer (Anti-Detect)")
st.markdown("Masukkan teks AI, tekan butang, dan dapatkan teks gaya manusia.")

# 2. Setup API Key (Auto-detect dari Server atau Manual)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key (jika tiada dalam sistem):", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Di Sini:", height=200, placeholder="Paste teks ChatGPT/Gemini anda di sini...")

# 4. Logik Pemprosesan
if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            # Setup Konfigurasi
            genai.configure(api_key=api_key)
            
            # KITA GUNA GEMINI-PRO (Model Paling Stabil)
            model = genai.GenerativeModel('gemini-pro')

            # Prompt Rahsia
            prompt = f"""
            You are an expert ghostwriter. Rewrite the following text to bypass AI detectors like ZeroGPT.
            
            Strategy to use:
            1. BURSTINESS: Mix extremely short sentences with longer, complex sentences. 
            2. PERPLEXITY: Use varied vocabulary. Avoid robotic transitions like "Moreover", "In conclusion", "Furthermore".
            3. TONE: Write in a natural, conversational tone suitable for the context.
            4. LANGUAGE: Keep the same language as the original text.
            
            Original Text:
            {text_input}
            """

            with st.spinner('Sedang menulis semula...'):
                response = model.generate_content(prompt)
                new_text = response.text
                
                st.success("Siap!")
                st.subheader("Hasil:")
                st.write(new_text)
                st.code(new_text, language=None)
                
        except Exception as e:
            st.error(f"Ralat berlaku: {e}")

st.divider()
st.caption("Powered by Gemini Pro")
