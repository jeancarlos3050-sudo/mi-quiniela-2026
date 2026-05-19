import streamlit as st
import json
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# --- CSS INTEGRADO ---
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    div[data-testid="stColumn"] {display: flex; align-items: center; justify-content: center;}
    div[data-testid="stNumberInput"] {width: 70px !important; margin: 0 auto !important;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; text-align: center;}
    .team-local {text-align: right; font-weight: bold;}
    .team-visitante {text-align: left; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE LIMPIEZA TOTAL ---
if st.query_params.get("reset") == "true":
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()

def recargar_total():
    st.query_params["reset"] = "true"
    st.rerun()

# --- FUNCIÓN PDF MEJORADA ---
def generar_pdf(nombre_u, pronosticos, calendario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(190, 10, txt=f"Quiniela Mundial 2026: {nombre_u}", ln=True, align='C', fill=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(25, 10, "Partido", border=1, fill=True)
    pdf.cell(60, 10, "Local", border=1, fill=True)
    pdf.cell(20, 10, "Goles", border=1, align='C', fill=True)
    pdf.cell(60, 10, "Visitante", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Arial", size=11)
    for grupo, juegos in calendario.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(165, 8, grupo, ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for juego in juegos:
            id_p = juego[0]
            if id_p in pronosticos:
                p = pronosticos[id_p]
                pdf.cell(25, 8, f"#{id_p}", border=1)
                pdf.cell(60, 8, juego[2], border=1)
                pdf.cell(20, 8, f"{p['local']} - {p['visitante']}", border=1, align='C')
                pdf.cell(60, 8, juego[3], border=1)
                pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

# --- CALENDARIO COMPLETO ---
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

# --- INTERFAZ ---
st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            cols = st.columns([2, 1, 0.5, 1, 2])
            cols[0].markdown(f"**{juego[1]}**", unsafe_allow_html=True)
            loc = cols[1].number_input("L", min_value=0, step=1, key=f"L{juego[0]}")
            cols[2].markdown('<p class="vs-texto">vs</p>', unsafe_allow_html=True)
            vis = cols[3].number_input("V", min_value=0, step=1, key=f"V{juego[0]}")
            cols[4].markdown(f"**{juego[2]}**", unsafe_allow_html=True)
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

# --- EXPORTACIÓN ---
st.write("---")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💾 GUARDAR JSON"):
        st.download_button("📥 Descargar", json.dumps({"nombre": nombre, "datos": pronosticos}), "quiniela.json")
with c2:
    if st.button("📄 GENERAR PDF"):
        if nombre:
            st.download_button("📥 Descargar PDF", generar_pdf(nombre, pronosticos, calendario), "quiniela.pdf", mime="application/pdf")
with c3:
    if st.button("🧹 LIMPIAR TODO"):
        recargar_total()
