import streamlit as st
import json
from fpdf import FPDF
from datetime import datetime

# Configuración base
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS para alineación y colores
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; font-size: 16px; text-align: center;}
    .team-local {text-align: right; font-weight: bold; padding-right: 10px;}
    .team-visitante {text-align: left; font-weight: bold; padding-left: 10px;}
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
    pdf.set_font("Arial", size=9)
    pdf.cell(190, 5, txt=f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(5)
    
    # Anchos proporcionales
    w_id, w_f, w_loc, w_pr, w_vis = 10, 30, 60, 20, 70
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(w_id, 8, "ID", 1, 0, 'C', 1)
    pdf.cell(w_f, 8, "Fecha", 1, 0, 'C', 1)
    pdf.cell(w_loc, 8, "Local", 1, 0, 'L', 1)
    pdf.cell(w_pr, 8, "Pron.", 1, 0, 'C', 1)
    pdf.cell(w_vis, 8, "Visitante", 1, 1, 'L', 1)
    
    pdf.set_font("Arial", size=9)
    for grupo, juegos in cal.items():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(w_id+w_f+w_loc+w_pr+w_vis, 7, grupo, 1, 1, 'L', 1)
        pdf.set_font("Arial", size=9)
        for j in juegos:
            val = data_p.get(j[0], {"local": 0, "visitante": 0})
            pdf.cell(w_id, 7, j[0], 1, 0, 'C')
            pdf.cell(w_f, 7, j[1], 1, 0, 'C')
            pdf.cell(w_loc, 7, j[2], 1, 0, 'L')
            pdf.cell(w_pr, 7, f"{val['local']}-{val['visitante']}", 1, 0, 'C')
            pdf.cell(w_vis, 7, j[3], 1, 1, 'L')
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for j in juegos:
            cols = st.columns([0.5, 1.5, 2, 0.8, 0.8, 2])
            cols[0].write(f"P{j[0]}")
            cols[1].write(j[1])
            cols[2].write(j[2])
            pronosticos[j[0]] = {
                "local": cols[3].number_input("L", 0, None, 0, key=f"l{j[0]}", label_visibility="collapsed"),
                "visitante": cols[4].number_input("V", 0, None, 0, key=f"v{j[0]}", label_visibility="collapsed")
            }
            cols[5].write(j[3])

st.write("---")
if nombre and st.button("📄 GENERAR PDF"):
    st.download_button("📥 Descargar PDF", generar_pdf(nombre, pronosticos, calendario), f"Quiniela_{nombre}.pdf", "application/pdf")
