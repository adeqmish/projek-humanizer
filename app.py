import streamlit as st
import google.generativeai as genai
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="My Humanizer", page_icon="🤖")

st.title("🤖 AI Text Humanizer (Anti-Detect)")
st.markdown("Masukkan teks AI, tekan butang, dan dapatkan teks gaya manusia.")

# 2. Setup API Key (Auto-detect dari Server atau Manual)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Backup kalau kawan nak guna key sendiri
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
            # Setup Model
            genai.configure(api_key=api_key)
            
            # PENTING: Guna model 'gemini-1.5-flash' sebab ia laju & jimat kuota
            model = genai.GenerativeModel('gemini-pro')
            
            # Prompt Rahsia (Arahan kepada AI)
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

            with st.spinner('Sedang menulis semula... (Tunggu sekejap)'):
                # Request ke Google
                response = model.generate_content(prompt)
                new_text = response.text
                
                # Paparkan Hasil
                st.success("Siap!")
                st.subheader("Hasil:")
                st.write(new_text)
                
                # Butang Copy Mudah
                st.code(new_text, language=None)
                
        except Exception as e:
            # Error Handling kalau terlebih limit
            if "429" in str(e):
                st.error("⚠️ Server sibuk (Rate Limit). Sila tunggu 1 minit dan cuba lagi.")
            else:
                st.error(f"Ralat berlaku: {e}")

# 5. Info Kaki Halaman
st.divider()

st.caption("Nota: Menggunakan Gemini 1.5 Flash Free Tier. Had penggunaan: 15 request/minit.")
