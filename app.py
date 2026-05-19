import streamlit as st
import json
from fpdf import FPDF

# Configuración base (mantenida idéntica)
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS quirurgico: solo ajustamos tamaño uniforme de casillas y centrado del vs
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    
    /* Forzar color blanco en el texto del input */
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    
    /* MODIFICACIÓN QUIRÚRGICA: Forzar mismo tamaño para las casillas de marcador */
    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        width: 60px !important; /* Ancho fijo para consistencia */
    }
    
    /* MODIFICACIÓN QUIRÚRGICA: Centrado absoluto del vs */
    .vs-text {
        text-align: center; 
        font-weight: bold; 
        color: #ffbc42; 
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        margin-top: 5px; /* Ajuste fino */
    }
    
    h2 {color: #ffbc42 !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

# [Código previo de obtener_calendario mantenido idéntico con todos los grupos]
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

# Función PDF mantenida intacta
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

# Interfaz: mantenemos la estructura de columnas original + expander
for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            # MODIFICACIÓN QUIRÚRGICA: Nueva estructura de columnas para centrado absoluto
            # cols = st.columns([4, 2, 1, 2, 4]) # Anterior
            cols = st.columns([3, 1.5, 1, 1.5, 3]) # Nueva distribución para equilibrar vs
            cols[0].write(f"P{juego[0]} | {juego[1]}")
            cols[1].write(f"**{juego[2]}**")
            
            # Marcador Local
            loc = cols[2].number_input("L", min_value=0, key=f"l{juego[0]}", label_visibility="collapsed")
            
            # El "vs" se coloca en una columna central dedicada para centrado absoluto
            cols[2].markdown('<div class="vs-text">vs</div>', unsafe_allow_html=True)
            
            # Marcador Visitante
            vis = cols[3].number_input("V", min_value=0, key=f"v{juego[0]}", label_visibility="collapsed")
            
            cols[4].write(f"**{juego[3]}**")
            pronosticos[juego[0]] = {"local": loc, "visitante": vis}

# Botones finales intactos
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
