import streamlit as st
from PIL import Image
import pytesseract
import google.generativeai as genai

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # ajuste para seu caminho

genai.configure(api_key="SUA_CHAVE_AQUI")

def extrair_texto(imagem):
    texto = pytesseract.image_to_string(imagem, lang="por")
    return texto

def processar_com_gemini(texto):
    prompt = f"""
Você é um especialista em direito imobiliário. O texto a seguir foi extraído via OCR de um documento cartorial. Extraia e organize:

- Nome do comprador
- CPF ou CNPJ do comprador
- Nome do vendedor
- CPF ou CNPJ do vendedor
- Valor do imóvel
- Data da escritura
- Número da matrícula do imóvel
- Endereço completo do imóvel
- Nome do cartório e cidade

Texto extraído:
\"\"\"
{texto}
\"\"\"
"""
    model = genai.GenerativeModel('gemini-1.5-pro')
    resposta = model.generate_content(prompt)
    return resposta.text

st.title("🧾 Extração de dados de documentos cartoriais")

arquivo = st.file_uploader("Envie uma imagem da escritura", type=["jpg", "jpeg", "png"])

if arquivo:
    imagem = Image.open(arquivo)
    st.image(imagem, caption="Imagem enviada", use_column_width=True)

    with st.spinner("Extraindo texto via OCR..."):
        texto_ocr = extrair_texto(imagem)
        st.text_area("Texto extraído:", texto_ocr, height=200)

    if st.button("Processar com IA"):
        with st.spinner("Enviando ao Gemini..."):
            resposta = processar_com_gemini(texto_ocr)
            st.markdown("### 📄 Resposta estruturada:")
            st.write(resposta)
