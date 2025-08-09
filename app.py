import streamlit as st
import unicodedata
import re

# Tu función de transliteración (copiada del script original)
def normalize_strong(text):
    return unicodedata.normalize('NFD', text)

def replace_diptongos(text):
    text = re.sub(r'α[\u0300-\u036f]*ι', 'e', text)
    text = re.sub(r'Α[\u0300-\u036f]*ι', 'E', text)
    text = re.sub(r'ε[\u0300-\u036f]*ι', 'i', text)
    text = re.sub(r'Ε[\u0300-\u036f]*ι', 'I', text)
    text = re.sub(r'ο[\u0300-\u036f]*ι', 'i', text)
    text = re.sub(r'Ο[\u0300-\u036f]*ι', 'I', text)
    text = re.sub(r'υ[\u0300-\u036f]*ι', 'i', text)
    text = re.sub(r'Υ[\u0300-\u036f]*ι', 'I', text)
    text = re.sub(r'ο[\u0300-\u036f]*υ', 'u', text)
    text = re.sub(r'Ο[\u0300-\u036f]*υ', 'U', text)
    text = re.sub(r'α[\u0300-\u036f]*υ', 'af', text)
    text = re.sub(r'Α[\u0300-\u036f]*υ', 'Af', text)
    text = re.sub(r'ε[\u0300-\u036f]*υ', 'eu', text)
    text = re.sub(r'Ε[\u0300-\u036f]*υ', 'Eu', text)
    text = re.sub(r'η[\u0300-\u036f]*υ', 'iu', text)
    text = re.sub(r'Η[\u0300-\u036f]*υ', 'Iu', text)
    text = re.sub(r'ε[\u0300-\u036f]*ο[\u0300-\u036f]*υ', 'eú', text)
    text = re.sub(r'Ε[\u0300-\u036f]*ο[\u0300-\u036f]*υ', 'Eú', text)
    return text

def postprocess_gamma(text):
    text = text.replace("gé", "yé").replace("gí", "yí")
    text = text.replace("ge", "ye").replace("gi", "yi")
    text = text.replace("Gé", "Yé").replace("Gí", "Yí")
    text = text.replace("Ge", "Ye").replace("Gi", "Yi")
    return text

basic_mapping = {
    'α': 'a', 'β': 'v', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'η': 'i',
    'θ': 'z', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ὸ': 'ó',
    'ντ': 'd', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'ῶ': 'ó',
    'τ': 't', 'υ': 'i', 'φ': 'f', 'χ': 'j', 'ψ': 'ps', 'ω': 'o', 'ζ': 'dz', 'ῶ': 'ó',
    'Α': 'A', 'Β': 'V', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Dz', 'Η': 'I',
    'Θ': 'Z', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X',
    'Ο': 'O', 'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'I',
    'Φ': 'F', 'Χ': 'J', 'Ψ': 'Ps', 'Ω': 'O',
    '.': '.', ',': ',', ';': '?', '·': ':', ' ': ' ', '\n': '\n',
    '’': "'", '᾽': ''
}
circunflejo_map = {
    'ο͂': 'ó',
    'Ο͂': 'Ó',
    'ῶ': 'ó',
    'Ω͂': 'Ó',
    'ῦ': 'ú',
    'Υ͂': 'Ú',
    'ῆ': 'í',
    'Η͂': 'Í',
    'ῖ': 'í',
    'Ι͂': 'Í',
    'ᾶ': 'á',
    'Α͂': 'Á',
    'ε͂': 'é',
    'Ε͂': 'É',
}

def transliterate_modern_greek_v20(text_koine):
    text = normalize_strong(text_koine)
    for koiné_char, accented_char in circunflejo_map.items():
        text = text.replace(koiné_char, accented_char)

    text = replace_diptongos(text)
    sorted_keys = sorted(basic_mapping.keys(), key=len, reverse=True)
    result = []
    i = 0
    while i < len(text):
        matched = False
        for key in sorted_keys:
            if text[i:i+len(key)] == key:
                result.append(basic_mapping[key])
                i += len(key)
                matched = True
                break
        if not matched:
            result.append(text[i])
            i += 1
    translit = ''.join(result)
    translit = postprocess_gamma(translit)
    translit = unicodedata.normalize('NFC', translit)
    translit = ''.join(c for c in translit if unicodedata.category(c) != 'Mn')
    return translit

# Interfaz Streamlit
st.title("Transliterador de Griego Koiné a Pronunciación Moderna")
st.markdown(
    """
    <p style="font-size:16px;">
        <strong>Por Gustavo Uliarte</strong>
        <a href="https://www.facebook.com/Asistente3Juan15/" target="_blank" style="text-decoration:none;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" 
                 alt="Facebook" width="20" style="vertical-align:middle; margin-left:10px;">
        </a> Asistente3Juan15 - en desarrollo.
    </p>
    """,
    unsafe_allow_html=True
)
input_text = st.text_area("Pega el texto griego aquí:", height=200)

if st.button("Transliterar"):
    if input_text.strip():
        result = transliterate_modern_greek_v20(input_text)
        st.text_area("Resultado en pronunciación moderna:", value=result, height=200)
    else:
        st.warning("Por favor, ingresa texto griego para transliterar.")

