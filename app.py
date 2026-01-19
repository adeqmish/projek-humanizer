import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="My Humanizer", page_icon="🤖")
st.title("🤖 AI Text Humanizer (Anti-Detect)")

# Setup API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Masukkan API Key:", type="password")

text_input = st.text_area("Masukkan Teks:", height=200)

if st.button("Humanize Sekarang"):
    if not api_key:
        st.error("Masukkan API Key dulu.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # GUNA GEMINI 1.5 FLASH
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            Rewrite this text to bypass AI detection (ZeroGPT).
            Make it sound natural, use varied sentence lengths (burstiness), 
            and avoid robotic words. Keep original meaning.
            
            Text: {text_input}
            """
            
            with st.spinner('Sedang memproses...'):
                response = model.generate_content(prompt)
                st.success("Siap!")
                st.write(response.text)
                st.code(response.text, language=None)
                
        except Exception as e:
            st.error(f"Ralat: {e}")
            
            # DEBUGGING: Kalau ralat lagi, ini akan tunjuk model apa yang available
            st.warning("Senarai model yang dikesan di server:")
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        st.write(f"- {m.name}")
            except:
                st.write("Gagal dapatkan senarai model.")
