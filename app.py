import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="My Humanizer 2.5", page_icon="🚀")

st.title("🚀 AI Mish Humanizer")
st.markdown("Versi terkini menggunakan model yang lebih laju.")

# 2. Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

# 3. Kotak Input
text_input = st.text_area("Masukkan Teks Di Sini:", height=200)

# 4. Logik Pemprosesan
if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Sila masukkan API Key dahulu.")
    elif not text_input:
        st.warning("Tiada teks dimasukkan.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # KEMASKINI: Guna model yang wujud dalam senarai anda
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
                st.code(response.text, language=None)
                
        except Exception as e:
            st.error(f"Ralat: {e}")

