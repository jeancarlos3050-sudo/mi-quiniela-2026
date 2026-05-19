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

# Lógica de reinicio: Borra el estado y recarga la app
def reset_app():
    st.session_state.clear()
    st.rerun()

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# Input de nombre
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [("01", "11/06 13:00", "México", "Sudáfrica"), ("02", "11/06 20:00", "Corea del Sur", "Chequia")],
        "GRUPO B": [("07", "12/06 13:00", "Canadá", "Bosnia-Herzegovina"), ("08", "13/06 13:00", "Qatar", "Suiza")]
        # Puedes seguir agregando los otros grupos aquí manteniendo la misma estructura
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

# Renderizado de partidos
for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            cols = st.columns([2.5, 2.5, 1.2, 0.6, 1.2, 2.5])
            cols[1].markdown(f'<div class="team-local">{juego[2]}</div>', unsafe_html=True)
            # Usamos keys dinámicas para que los inputs se creen frescos en cada carga
            loc = st.number_input(f"L{juego[0]}", min_value=0, step=1, key=f"loc_{juego[0]}")
            cols[3].markdown('<p class="vs-texto">vs</p>', unsafe_html=True)
            vis = st.number_input(f"V{juego[0]}", min_value=0, step=1, key=f"vis_{juego[0]}")
            cols[5].markdown(f'<div class="team-visitante">{juego[3]}</div>', unsafe_html=True)
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

st.write("---")
# Botones finales
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("💾 GUARDAR JSON"):
        if nombre:
            st.download_button("📥 Descargar JSON", json.dumps({"participante": nombre, "pronosticos": pronosticos}), file_name="pronostico.json")
with c2:
    if st.button("📄 GENERAR PDF"):
        if nombre:
            st.download_button("📥 Descargar PDF", generar_pdf(nombre, pronosticos), file_name="pronostico.pdf", mime="application/pdf")
with c3:
    # Este botón ejecuta la función que limpia todo el estado y recarga la app
    if st.button("🧹 LIMPIAR TODO"):
        reset_app()
