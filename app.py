import streamlit as st
import json
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    div[data-testid="stNumberInput"] {width: 70px !important; margin: 0 auto !important;}
    div[data-testid="stNumberInput"] input {text-align: center !important; width: 70px !important; background-color: #ffffff !important; color: #000000 !important; font-weight: bold; border-radius: 4px !important; padding: 2px !important;}
    div[data-testid="stNumberInput"] label {display: none !important;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; font-size: 16px; text-align: center;}
    .team-local {text-align: right; font-weight: bold; width: 100%; padding-right: 10px;}
    .team-visitante {text-align: left; font-weight: bold; width: 100%; padding-left: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# --- LÓGICA DE RECARGA TOTAL ---
# Esta parte maneja el parámetro de limpieza en la URL
if st.query_params.get("reset") == "true":
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()

def recargar_total():
    st.query_params["reset"] = "true"
    st.rerun()

# --- INPUT NOMBRE ---
nombre = st.text_input("Nombre del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [("01", "México", "Sudáfrica"), ("02", "Corea del Sur", "Chequia"), ("03", "México", "Corea del Sur"), ("04", "Chequia", "Sudáfrica"), ("05", "México", "Chequia"), ("06", "Sudáfrica", "Corea del Sur")],
        "GRUPO B": [("07", "Canadá", "Bosnia"), ("08", "Qatar", "Suiza"), ("09", "Suiza", "Bosnia"), ("10", "Canadá", "Qatar"), ("11", "Bosnia", "Qatar"), ("12", "Suiza", "Canadá")],
        "GRUPO C": [("13", "Brasil", "Marruecos"), ("14", "Haití", "Escocia"), ("15", "Escocia", "Marruecos"), ("16", "Brasil", "Haití"), ("17", "Marruecos", "Haití"), ("18", "Escocia", "Brasil")],
        "GRUPO D": [("19", "EE.UU.", "Paraguay"), ("20", "Australia", "Turquía"), ("21", "EE.UU.", "Australia"), ("22", "Turquía", "Paraguay"), ("23", "Paraguay", "Australia"), ("24", "Turquía", "EE.UU.")],
        "GRUPO E": [("25", "Alemania", "Curazao"), ("26", "Costa de Marfil", "Ecuador"), ("27", "Alemania", "Costa de Marfil"), ("28", "Ecuador", "Curazao"), ("29", "Curazao", "Costa de Marfil"), ("30", "Ecuador", "Alemania")],
        "GRUPO F": [("31", "Países Bajos", "Japón"), ("32", "Suecia", "Túnez"), ("33", "Países Bajos", "Suecia"), ("34", "Túnez", "Japón"), ("35", "Japón", "Suecia"), ("36", "Túnez", "Países Bajos")],
        "GRUPO G": [("37", "Bélgica", "Egipto"), ("38", "Irán", "Nueva Zelanda"), ("39", "Bélgica", "Irán"), ("40", "Nueva Zelanda", "Egipto"), ("41", "Egipto", "Irán"), ("42", "Nueva Zelanda", "Bélgica")],
        "GRUPO H": [("43", "España", "Cabo Verde"), ("44", "Arabia Saudita", "Uruguay"), ("45", "España", "Arabia Saudita"), ("46", "Uruguay", "Cabo Verde"), ("47", "Cabo Verde", "Arabia Saudita"), ("48", "Uruguay", "España")],
        "GRUPO I": [("49", "Francia", "Senegal"), ("50", "Irak", "Noruega"), ("51", "Francia", "Irak"), ("52", "Noruega", "Senegal"), ("53", "Noruega", "Francia"), ("54", "Senegal", "Irak")],
        "GRUPO J": [("55", "Argentina", "Argelia"), ("56", "Austria", "Jordania"), ("57", "Argentina", "Austria"), ("58", "Jordania", "Argelia"), ("59", "Argelia", "Austria"), ("60", "Jordania", "Argentina")],
        "GRUPO K": [("61", "Portugal", "RD Congo"), ("62", "Uzbekistán", "Colombia"), ("63", "Portugal", "Uzbekistán"), ("64", "Colombia", "RD Congo"), ("65", "Colombia", "Portugal"), ("66", "RD Congo", "Uzbekistán")],
        "GRUPO L": [("67", "Inglaterra", "Croacia"), ("68", "Ghana", "Panamá"), ("69", "Inglaterra", "Ghana"), ("70", "Panamá", "Croacia"), ("71", "Croacia", "Ghana"), ("72", "Panamá", "Inglaterra")]
    }

calendario = obtener_calendario()
pronosticos = {}

# Renderizado
for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            c1, c2, c3, c4 = st.columns([2, 1, 1, 2])
            c1.markdown(f'<div class="team-local">{juego[1]}</div>', unsafe_html=True)
            loc = c2.number_input(f"L{juego[0]}", min_value=0, step=1)
            vis = c3.number_input(f"V{juego[0]}", min_value=0, step=1)
            c4.markdown(f'<div class="team-visitante">{juego[2]}</div>', unsafe_html=True)
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

st.write("---")
# Botones
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 GUARDAR JSON"):
        if nombre:
            st.download_button("📥 Descargar", json.dumps({"participante": nombre, "datos": pronosticos}), "quiniela.json")
with col2:
    if st.button("📄 GENERAR PDF"):
        st.write("PDF generado")
with col3:
    # EL BOTÓN QUE BUSCABAS
    if st.button("🧹 LIMPIAR TODO"):
        recargar_total()
