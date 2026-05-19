import streamlit as st
import json
from fpdf import FPDF
from datetime import datetime

# Configuración base del sistema
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS para diseño y visibilidad
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    /* Ajuste de visibilidad para el label del nombre */
    div[data-testid="stTextInput"] label {
        color: white !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important;
    }
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; font-size: 16px; text-align: center; margin-top: 20px;}
    .team-local {text-align: right; font-weight: bold; margin-top: 20px;}
    .team-visitante {text-align: left; font-weight: bold; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [("01", "11/06 13:00", "México", "Sudáfrica"), ("02", "11/06 20:00", "Corea del Sur", "Chequia"), ("03", "18/06 19:00", "México", "Corea del Sur"), ("04", "18/06 12:00", "Chequia", "Sudáfrica"), ("05", "24/06 22:00", "México", "Chequia"), ("06", "24/06 22:00", "Sudáfrica", "Corea del Sur")],
        "GRUPO B": [("07", "12/06 13:00", "Canadá", "Bosnia"), ("08", "13/06 13:00", "Qatar", "Suiza"), ("09", "18/06 13:00", "Suiza", "Bosnia"), ("10", "18/06 16:00", "Canadá", "Qatar"), ("11", "24/06 13:00", "Bosnia", "Qatar"), ("12", "24/06 13:00", "Suiza", "Canadá")],
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

def generar_pdf(nombre_u, data_p, cal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt=f"Quiniela: {nombre_u}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 10, txt=f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(15, 10, "ID", 1, 0, 'C', True)
    pdf.cell(30, 10, "Fecha", 1, 0, 'C', True)
    pdf.cell(60, 10, "Local", 1, 0, 'C', True)
    pdf.cell(25, 10, "Pron.", 1, 0, 'C', True)
    pdf.cell(60, 10, "Visitante", 1, 1, 'C', True)
    
    pdf.set_font("Arial", size=10)
    for grupo, partidos in cal.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(190, 8, grupo, 1, 1, 'L', True)
        pdf.set_font("Arial", size=10)
        for p in partidos:
            res = data_p.get(p[0], {"local": 0, "visitante": 0})
            pdf.cell(15, 8, p[0], 1)
            pdf.cell(30, 8, p[1], 1)
            pdf.cell(60, 8, p[2], 1)
            pdf.cell(25, 8, f"{res['local']}-{res['visitante']}", 1, 0, 'C')
            pdf.cell(60, 8, p[3], 1, 1)
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}

for grupo, partidos in calendario.items():
    with st.expander(grupo):
        for p in partidos:
            cols = st.columns([1, 2, 1, 0.5, 1, 2])
            cols[0].write(f"P{p[0]}")
            cols[1].markdown(f'<div class="team-local">{p[2]}</div>', unsafe_html=True)
            with cols[2]:
                l = st.number_input("L", 0, key=f"l{p[0]}", label_visibility="collapsed")
            cols[3].markdown('<div class="vs-texto">vs</div>', unsafe_html=True)
            with cols[4]:
                v = st.number_input("V", 0, key=f"v{p[0]}", label_visibility="collapsed")
            cols[5].markdown(f'<div class="team-visitante">{p[3]}</div>', unsafe_html=True)
            pronosticos[p[0]] = {"local": l, "visitante": v}

c1, c2 = st.columns(2)
if c1.button("💾 GUARDAR JSON"):
    if nombre:
        st.download_button("Descargar JSON", json.dumps({"participante": nombre, "pronosticos": pronosticos}), f"Quiniela_{nombre.replace(' ', '_')}.json")
    else:
        st.error("Ingrese su nombre")
if c2.button("📄 GENERAR PDF"):
    if nombre:
        st.download_button("Descargar PDF", generar_pdf(nombre, pronosticos, calendario), f"Quiniela_{nombre.replace(' ', '_')}.pdf", "application/pdf")
    else:
        st.error("Ingrese su nombre")
