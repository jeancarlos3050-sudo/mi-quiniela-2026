import streamlit as st
import json
from fpdf import FPDF

# Configuración base
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS para el diseño
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    div[data-testid="stColumn"] {display: flex; align-items: center; justify-content: center;}
    div[data-testid="stNumberInput"] {width: 70px !important; margin: 0 auto !important;}
    div[data-testid="stNumberInput"] input {text-align: center !important; width: 70px !important; background-color: #ffffff !important; color: #000000 !important; font-weight: bold; border-radius: 4px !important; padding: 2px !important;}
    div[data-testid="stNumberInput"] label {display: none !important;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; font-size: 16px; text-align: center; margin: 0 !important; padding: 0 !important; line-height: 1;}
    .team-local {text-align: right; font-weight: bold; width: 100%; padding-right: 10px; white-space: nowrap;}
    .team-visitante {text-align: left; font-weight: bold; width: 100%; padding-left: 10px; white-space: nowrap;}
    h2 {color: #ffbc42 !important;}
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE LIMPIEZA CORRECTA
def limpiar_datos():
    st.session_state["nombre_input"] = ""
    for key in st.session_state.keys():
        if key.startswith("l") or key.startswith("v"):
            st.session_state[key] = 0

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# Input del nombre
nombre = st.text_input("Nombre Completo del Participante:", key="nombre_input")

def obtener_calendario():
    return {
        "GRUPO A": [("01", "11/06 13:00", "México", "Sudáfrica"), ("02", "11/06 20:00", "Corea del Sur", "Chequia"), ("03", "18/06 19:00", "México", "Corea del Sur"), ("04", "18/06 12:00", "Chequia", "Sudáfrica"), ("05", "24/06 22:00", "México", "Chequia"), ("06", "24/06 22:00", "Sudáfrica", "Corea del Sur")],
        "GRUPO B": [("07", "12/06 13:00", "Canadá", "Bosnia-Herzegovina"), ("08", "13/06 13:00", "Qatar", "Suiza"), ("09", "18/06 13:00", "Suiza", "Bosnia-Herzegovina"), ("10", "18/06 16:00", "Canadá", "Qatar"), ("11", "24/06 13:00", "Bosnia-Herzegovina", "Qatar"), ("12", "24/06 13:00", "Suiza", "Canadá")],
        "GRUPO C": [("13", "13/06 16:00", "Brasil", "Marruecos"), ("14", "14/06 19:00", "Haití", "Escocia"), ("15", "19/06 16:00", "Escocia", "Marruecos"), ("16", "20/06 19:00", "Brasil", "Haití"), ("17", "24/06 16:00", "Marruecos", "Haití"), ("18", "24/06 16:00", "Escocia", "Brasil")],
        "GRUPO D": [("19", "13/06 19:00", "EE.UU.", "Paraguay"), ("20", "14/06 22:00", "Australia", "Turquía"), ("21", "19/06 13:00", "EE.UU.", "Australia"), ("22", "20/06 22:00", "Turquía", "Paraguay"), ("23", "26/06 20:00", "Paraguay", "Australia"), ("24", "26/06 20:00", "Turquía", "EE.UU.")],
        "GRUPO E": [("25", "14/06 11:00", "Alemania", "Curazao"), ("26", "15/06 17:00", "Costa de Marfil", "Ecuador"), ("27", "20/06 14:00", "Alemania", "Costa de Marfil"), ("28", "21/06 18:00", "Ecuador", "Curazao"), ("29", "25/06 14:00", "Curazao", "Costa de Marfil"), ("30", "25/06 14:00", "Ecuador", "Alemania")],
        "GRUPO F": [("31", "14/06 14:00", "Países Bajos", "Japón"), ("32", "15/06 20:00", "Suecia", "Túnez"), ("33", "20/06 11:00", "Países Bajos", "Suecia"), ("34", "21/06 22:00", "Túnez", "Japón"), ("35", "26/06 17:00", "Japón", "Suecia"), ("36", "26/06 17:00", "Túnez", "Países Bajos")],
        "GRUPO G": [("37", "15/06 13:00", "Bélgica", "Egipto"), ("38", "16/06 19:00", "Irán", "Nueva Zelanda"), ("39", "21/06 13:00", "Bélgica", "Irán"), ("40", "22/06 19:00", "Nueva Zelanda", "Egipto"), ("41", "27/06 21:00", "Egipto", "Irán"), ("42", "27/06 21:00", "Nueva Zelanda", "Bélgica")],
        "GRUPO H": [("43", "15/06 10:00", "España", "Cabo Verde"), ("44", "15/06 16:00", "Arabia Saudita", "Uruguay"), ("45", "21/06 10:00", "España", "Arabia Saudita"), ("46", "21/06 16:00", "Uruguay", "Cabo Verde"), ("47", "27/06 18:00", "Cabo Verde", "Arabia Saudita"), ("48", "27/06 18:00", "Uruguay", "España")],
        "GRUPO I": [("49", "16/06 13:00", "Francia", "Senegal"), ("50", "16/06 16:00", "Irak", "Noruega"), ("51", "22/06 15:00", "Francia", "Irak"), ("52", "23/06 18:00", "Noruega", "Senegal"), ("53", "26/06 13:00", "Noruega", "Francia"), ("54", "26/06 13:00", "Senegal", "Irak")],
        "GRUPO J": [("55", "17/06 19:00", "Argentina", "Argelia"), ("56", "17/06 22:00", "Austria", "Jordania"), ("57", "22/06 11:00", "Argentina", "Austria"), ("58", "23/06 21:00", "Jordania", "Argelia"), ("59", "28/06 20:00", "Argelia", "Austria"), ("60", "28/06 20:00", "Jordania", "Argentina")],
        "GRUPO K": [("61", "17/06 11:00", "Portugal", "RD Congo"), ("62", "18/06 20:00", "Uzbekistán", "Colombia"), ("63", "23/06 11:00", "Portugal", "Uzbekistán"), ("64", "24/06 20:00", "Colombia", "RD Congo"), ("65", "28/06 17:30", "Colombia", "Portugal"), ("66", "28/06 17:30", "RD Congo", "Uzbekistán")],
        "GRUPO L": [("67", "17/06 14:00", "Inglaterra", "Croacia"), ("68", "18/06 17:00", "Ghana", "Panamá"), ("69", "23/06 14:00", "Inglaterra", "Ghana"), ("70", "24/06 17:00", "Panamá", "Croacia"), ("71", "27/06 15:00", "Croacia", "Ghana"), ("72", "27/06 15:00", "Panamá", "Inglaterra")]
    }

def generar_pdf(nombre_u, data_p):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Quiniela Mundial 2026: {nombre_u}", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    for id_p, res in data_p.items():
        pdf.cell(200, 8, txt=f"Partido {id_p}: {res['local']} vs {res['visitante']}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            cols = st.columns([2.5, 2.5, 1.2, 0.6, 1.2, 2.5])
            cols[0].markdown(f"P{juego[0]} | {juego[1]}")
            cols[1].markdown(f'<div class="team-local">{juego[2]}</div>', unsafe_html=True)
            # Clave única obligatoria para evitar conflictos
            loc = st.number_input("L", min_value=0, step=1, key=f"l{juego[0]}")
            cols[3].markdown('<p class="vs-texto">vs</p>', unsafe_html=True)
            vis = st.number_input("V", min_value=0, step=1, key=f"v{juego[0]}")
            cols[5].markdown(f'<div class="team-visitante">{juego[3]}</div>', unsafe_html=True)
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

st.write("---")
# BOTONES: El botón de limpiar usa el callback "on_click"
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💾 GUARDAR JSON"):
        if nombre:
            data_final = {"participante": nombre, "pronosticos": pronosticos}
            st.download_button("📥 Descargar JSON", json.dumps(data_final), file_name=f"Quiniela_{nombre.replace(' ', '_')}.json")
with c2:
    if st.button("📄 GENERAR PDF"):
        if nombre:
            pdf_bytes = generar_pdf(nombre, pronosticos)
            st.download_button("📥 Descargar PDF", pdf_bytes, file_name=f"Quiniela_{nombre.replace(' ', '_')}.pdf", mime="application/pdf")
        else:
            st.error("¡Ingresa tu nombre!")
with c3:
    # Este es el cambio clave que evita el error
    st.button("🧹 LIMPIAR TODO", on_click=limpiar_datos)
