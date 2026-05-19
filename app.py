import streamlit as st
import json
from fpdf import FPDF

st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide")

st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    h2 {color: #ffbc42 !important;}
    .vs-text {display: flex; align-items: center; justify-content: center; font-weight: bold; margin-top: 25px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS COMPLETOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    # Estructura maestra con los 72 partidos
    return {
        "GRUPO A": [{"#": f"{i:02d}", "hora": "11/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(1, 7)],
        "GRUPO B": [{"#": f"{i:02d}", "hora": "12/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(7, 13)],
        "GRUPO C": [{"#": f"{i:02d}", "hora": "13/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(13, 19)],
        "GRUPO D": [{"#": f"{i:02d}", "hora": "14/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(19, 25)],
        "GRUPO E": [{"#": f"{i:02d}", "hora": "15/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(25, 31)],
        "GRUPO F": [{"#": f"{i:02d}", "hora": "16/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(31, 37)],
        "GRUPO G": [{"#": f"{i:02d}", "hora": "17/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(37, 43)],
        "GRUPO H": [{"#": f"{i:02d}", "hora": "18/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(43, 49)],
        "GRUPO I": [{"#": f"{i:02d}", "hora": "19/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(49, 55)],
        "GRUPO J": [{"#": f"{i:02d}", "hora": "20/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(55, 61)],
        "GRUPO K": [{"#": f"{i:02d}", "hora": "21/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(61, 67)],
        "GRUPO L": [{"#": f"{i:02d}", "hora": "22/06", "local": f"Equipo {i}", "visitante": f"Equipo {i+1}"} for i in range(67, 73)]
    }

def generar_pdf(nombre_u, data_p, calendario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Comprobante: {nombre_u}", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(20, 10, "Partido", border=1)
    pdf.cell(100, 10, "Encuentro", border=1)
    pdf.cell(30, 10, "Pronostico", border=1)
    pdf.ln()
    pdf.set_font("Arial", size=9)
    for grupo, juegos in calendario.items():
        for juego in juegos:
            p = data_p.get(juego['#'], {"local": 0, "visitante": 0})
            pdf.cell(20, 7, f"P{juego['#']}", border=1)
            pdf.cell(100, 7, f"{juego['local']} vs {juego['visitante']}", border=1)
            pdf.cell(30, 7, f"{p['local']} - {p['visitante']}", border=1)
            pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}
for grupo, juegos in calendario.items():
    st.subheader(grupo)
    for juego in juegos:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 0.5, 2, 2])
        col1.write(f"P{juego['#']} ({juego['hora']})")
        col2.write(f"**{juego['local']}**")
        loc = col3.number_input("L", key=f"l{juego['#']}", label_visibility="collapsed")
        col3.markdown('<div class="vs-text">vs</div>', unsafe_allow_html=True)
        vis = col4.number_input("V", key=f"v{juego['#']}", label_visibility="collapsed")
        col5.write(f"**{juego['visitante']}**")
        pronosticos[juego['#']] = {"local": loc, "visitante": vis}

if st.button("💾 GUARDAR Y GENERAR PDF"):
    if nombre:
        st.download_button("📥 Descargar PDF", generar_pdf(nombre, pronosticos, calendario), file_name=f"{nombre}_Quiniela.pdf")
    else:
        st.error("Ingrese su nombre.")
