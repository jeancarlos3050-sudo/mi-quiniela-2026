import streamlit as st
import json
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    .partido-box {background-color: #1c2541; padding: 10px; border-radius: 5px; margin-bottom: 8px; border: 1px solid #3a506b;}
    div[data-testid="stNumberInput"] {width: 60px !important;}
    h2 {color: #ffbc42 !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [
            {"#": "01", "hora": "11/06 13:00", "local": "México", "visitante": "Sudáfrica"},
            {"#": "02", "hora": "11/06 20:00", "local": "Corea del Sur", "visitante": "Chequia"},
            {"#": "03", "hora": "18/06 19:00", "local": "México", "visitante": "Corea del Sur"},
            {"#": "04", "hora": "18/06 12:00", "local": "Chequia", "visitante": "Sudáfrica"},
            {"#": "05", "hora": "24/06 22:00", "local": "México", "visitante": "Chequia"},
            {"#": "06", "hora": "24/06 22:00", "local": "Sudáfrica", "visitante": "Corea del Sur"}
        ],
        "GRUPO B": [
            {"#": "07", "hora": "12/06 13:00", "local": "Canadá", "visitante": "Bosnia-Herzegovina"},
            {"#": "08", "hora": "13/06 13:00", "local": "Qatar", "visitante": "Suiza"},
            {"#": "09", "hora": "18/06 13:00", "local": "Suiza", "visitante": "Bosnia-Herzegovina"},
            {"#": "10", "hora": "18/06 16:00", "local": "Canadá", "visitante": "Qatar"},
            {"#": "11", "hora": "24/06 13:00", "local": "Bosnia-Herzegovina", "visitante": "Qatar"},
            {"#": "12", "hora": "24/06 13:00", "local": "Suiza", "visitante": "Canadá"}
        ],
        "GRUPO C": [
            {"#": "13", "hora": "13/06 16:00", "local": "Brasil", "visitante": "Marruecos"},
            {"#": "14", "hora": "14/06 19:00", "local": "Haití", "visitante": "Escocia"},
            {"#": "15", "hora": "19/06 16:00", "local": "Escocia", "visitante": "Marruecos"},
            {"#": "16", "hora": "20/06 19:00", "local": "Brasil", "visitante": "Haití"},
            {"#": "17", "hora": "24/06 16:00", "local": "Marruecos", "visitante": "Haití"},
            {"#": "18", "hora": "24/06 16:00", "local": "Escocia", "visitante": "Brasil"}
        ],
        "GRUPO D": [
            {"#": "19", "hora": "13/06 19:00", "local": "EE.UU.", "visitante": "Paraguay"},
            {"#": "20", "hora": "14/06 22:00", "local": "Australia", "visitante": "Turquía"},
            {"#": "21", "hora": "19/06 13:00", "local": "EE.UU.", "visitante": "Australia"},
            {"#": "22", "hora": "20/06 22:00", "local": "Turquía", "visitante": "Paraguay"},
            {"#": "23", "hora": "26/06 20:00", "local": "Paraguay", "visitante": "Australia"},
            {"#": "24", "hora": "26/06 20:00", "local": "Turquía", "visitante": "EE.UU."}
        ],
        "GRUPO E": [
            {"#": "25", "hora": "14/06 11:00", "local": "Alemania", "visitante": "Curazao"},
            {"#": "26", "hora": "15/06 17:00", "local": "Costa de Marfil", "visitante": "Ecuador"},
            {"#": "27", "hora": "20/06 14:00", "local": "Alemania", "visitante": "Costa de Marfil"},
            {"#": "28", "hora": "21/06 18:00", "local": "Ecuador", "visitante": "Curazao"},
            {"#": "29", "hora": "25/06 14:00", "local": "Curazao", "visitante": "Costa de Marfil"},
            {"#": "30", "hora": "25/06 14:00", "local": "Ecuador", "visitante": "Alemania"}
        ],
        "GRUPO F": [
            {"#": "31", "hora": "14/06 14:00", "local": "Países Bajos", "visitante": "Japón"},
            {"#": "32", "hora": "15/06 20:00", "local": "Suecia", "visitante": "Túnez"},
            {"#": "33", "hora": "20/06 11:00", "local": "Países Bajos", "visitante": "Suecia"},
            {"#": "34", "hora": "21/06 22:00", "local": "Túnez", "visitante": "Japón"},
            {"#": "35", "hora": "26/06 17:00", "local": "Japón", "visitante": "Suecia"},
            {"#": "36", "hora": "26/06 17:00", "local": "Túnez", "visitante": "Países Bajos"}
        ],
        "GRUPO G": [
            {"#": "37", "hora": "15/06 13:00", "local": "Bélgica", "visitante": "Egipto"},
            {"#": "38", "hora": "16/06 19:00", "local": "Irán", "visitante": "Nueva Zelanda"},
            {"#": "39", "hora": "21/06 13:00", "local": "Bélgica", "visitante": "Irán"},
            {"#": "40", "hora": "22/06 19:00", "local": "Nueva Zelanda", "visitante": "Egipto"},
            {"#": "41", "hora": "27/06 21:00", "local": "Egipto", "visitante": "Irán"},
            {"#": "42", "hora": "27/06 21:00", "local": "Nueva Zelanda", "visitante": "Bélgica"}
        ],
        "GRUPO H": [
            {"#": "43", "hora": "15/06 10:00", "local": "España", "visitante": "Cabo Verde"},
            {"#": "44", "hora": "15/06 16:00", "local": "Arabia Saudita", "visitante": "Uruguay"},
            {"#": "45", "hora": "21/06 10:00", "local": "España", "visitante": "Arabia Saudita"},
            {"#": "46", "hora": "21/06 16:00", "local": "Uruguay", "visitante": "Cabo Verde"},
            {"#": "47", "hora": "27/06 18:00", "local": "Cabo Verde", "visitante": "Arabia Saudita"},
            {"#": "48", "hora": "27/06 18:00", "local": "Uruguay", "visitante": "España"}
        ],
        "GRUPO I": [
            {"#": "49", "hora": "16/06 13:00", "local": "Francia", "visitante": "Senegal"},
            {"#": "50", "hora": "16/06 16:00", "local": "Irak", "visitante": "Noruega"},
            {"#": "51", "hora": "22/06 15:00", "local": "Francia", "visitante": "Irak"},
            {"#": "52", "hora": "23/06 18:00", "local": "Noruega", "visitante": "Senegal"},
            {"#": "53", "hora": "26/06 13:00", "local": "Noruega", "visitante": "Francia"},
            {"#": "54", "hora": "26/06 13:00", "local": "Senegal", "visitante": "Irak"}
        ],
        "GRUPO J": [
            {"#": "55", "hora": "17/06 19:00", "local": "Argentina", "visitante": "Argelia"},
            {"#": "56", "hora": "17/06 22:00", "local": "Austria", "visitante": "Jordania"},
            {"#": "57", "hora": "22/06 11:00", "local": "Argentina", "visitante": "Austria"},
            {"#": "58", "hora": "23/06 21:00", "local": "Jordania", "visitante": "Argelia"},
            {"#": "59", "hora": "28/06 20:00", "local": "Argelia", "visitante": "Austria"},
            {"#": "60", "hora": "28/06 20:00", "local": "Jordania", "visitante": "Argentina"}
        ],
        "GRUPO K": [
            {"#": "61", "hora": "17/06 11:00", "local": "Portugal", "visitante": "RD Congo"},
            {"#": "62", "hora": "18/06 20:00", "local": "Uzbekistán", "visitante": "Colombia"},
            {"#": "63", "hora": "23/06 11:00", "local": "Portugal", "visitante": "Uzbekistán"},
            {"#": "64", "hora": "24/06 20:00", "local": "Colombia", "visitante": "RD Congo"},
            {"#": "65", "hora": "28/06 17:30", "local": "Colombia", "visitante": "Portugal"},
            {"#": "66", "hora": "28/06 17:30", "local": "RD Congo", "visitante": "Uzbekistán"}
        ],
        "GRUPO L": [
            {"#": "67", "hora": "17/06 14:00", "local": "Inglaterra", "visitante": "Croacia"},
            {"#": "68", "hora": "18/06 17:00", "local": "Ghana", "visitante": "Panamá"},
            {"#": "69", "hora": "23/06 14:00", "local": "Inglaterra", "visitante": "Ghana"},
            {"#": "70", "hora": "24/06 17:00", "local": "Panamá", "visitante": "Croacia"},
            {"#": "71", "hora": "27/06 15:00", "local": "Croacia", "visitante": "Ghana"},
            {"#": "72", "hora": "27/06 15:00", "local": "Panamá", "visitante": "Inglaterra"}
        ]
    }

def generar_pdf(nombre_u, data_p):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Quiniela Mundial 2026: {nombre_u}", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.ln(10)
    for id_p, res in data_p.items():
        pdf.cell(200, 8, txt=f"Partido {id_p}: {res['local']} - {res['visitante']}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    st.subheader(grupo)
    for juego in juegos:
        cols = st.columns([4, 2, 1, 2, 4])
        cols[0].write(f"P{juego['#']} | {juego['hora']}")
        cols[1].write(f"**{juego['local']}**")
        loc = cols[2].number_input("L", min_value=0, key=f"l{juego['#']}", label_visibility="collapsed")
        cols[2].write("vs")
        vis = cols[3].number_input("V", min_value=0, key=f"v{juego['#']}", label_visibility="collapsed")
        cols[4].write(f"**{juego['visitante']}**")
        pronosticos[juego['#']] = {"local": loc, "visitante": vis}

c1, c2 = st.columns(2)
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
            st.error("¡Ingresa tu nombre primero!")
