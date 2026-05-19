import streamlit as st
import json
from fpdf import FPDF

# Configuración base del sistema
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS SEGURO Y COMPATIBLE
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

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

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

# --- FUNCIÓN PDF TIPO TABLA ---
def generar_pdf(nombre_u, data_p, cal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt=f"Quiniela Mundial 2026: {nombre_u}", ln=True, align='C')
    pdf.ln(5)
    
    # Encabezado de tabla
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(20, 10, "ID", border=1, fill=True, align='C')
    pdf.cell(65, 10, "Local", border=1, fill=True)
    pdf.cell(30, 10, "Pronostico", border=1, fill=True, align='C')
    pdf.cell(65, 10, "Visitante", border=1, fill=True)
    pdf.ln()
    
    # Datos
    pdf.set_font("Arial", size=10)
    for grupo, juegos in cal.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(180, 8, grupo, ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        for juego in juegos:
            id_p = juego[0]
            val = data_p.get(id_p, {"local": 0, "visitante": 0})
            pdf.cell(20, 8, id_p, border=1, align='C')
            pdf.cell(65, 8, juego[1], border=1)
            pdf.cell(30, 8, f"{val['local']} - {val['visitante']}", border=1, align='C')
            pdf.cell(65, 8, juego[2], border=1)
            pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            cols = st.columns([2.5, 2.5, 1.2, 0.6, 1.2, 2.5])
            cols[0].markdown(f"P{juego[0]}")
            cols[1].markdown(f'<div class="team-local">{juego[1]}</div>', unsafe_allow_html=True)
            with cols[2]:
                loc = st.number_input("L", min_value=0, step=1, key=f"l{juego[0]}", label_visibility="collapsed")
            cols[3].markdown('<p class="vs-texto">vs</p>', unsafe_allow_html=True)
            with cols[4]:
                vis = st.number_input("V", min_value=0, step=1, key=f"v{juego[0]}", label_visibility="collapsed")
            cols[5].markdown(f'<div class="team-visitante">{juego[2]}</div>', unsafe_allow_html=True)
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("💾 GUARDAR JSON"):
        if nombre:
            data_final = {"participante": nombre, "pronosticos": pronosticos}
            st.download_button("📥 Descargar JSON", json.dumps(data_final), file_name=f"Quiniela_{nombre.replace(' ', '_')}.json")
with c2:
    if st.button("📄 GENERAR PDF"):
        if nombre:
            pdf_bytes = generar_pdf(nombre, pronosticos, calendario)
            st.download_button("📥 Descargar PDF", pdf_bytes, file_name=f"Quiniela_{nombre.replace(' ', '_')}.pdf", mime="application/pdf")
        else:
            st.error("¡Ingresa tu nombre primero!")
