import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: #ffffff;}
    .vs-text {text-align: center; font-weight: bold; color: #ffbc42; padding: 10px 0;}
    h2 {color: #ffbc42 !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [("01", "11/06 13h", "México", "Sudáfrica"), ("02", "12/06 20h", "Corea del Sur", "Chequia"), ("03", "18/06 19h", "México", "Corea del Sur"), ("04", "18/06 12h", "Chequia", "Sudáfrica"), ("05", "24/06 22h", "México", "Chequia"), ("06", "24/06 22h", "Sudáfrica", "Corea del Sur")],
        "GRUPO B": [("07", "12/06 13h", "Canadá", "Bosnia-Herzegovina"), ("08", "13/06 13h", "Qatar", "Suiza"), ("09", "18/06 13h", "Suiza", "Bosnia-Herzegovina"), ("10", "18/06 16h", "Canadá", "Qatar"), ("11", "24/06 13h", "Bosnia-Herzegovina", "Qatar"), ("12", "24/06 13h", "Suiza", "Canadá")],
        "GRUPO C": [("13", "13/06 16h", "Brasil", "Marruecos"), ("14", "14/06 19h", "Haití", "Escocia"), ("15", "19/06 16h", "Escocia", "Marruecos"), ("16", "20/06 19h", "Brasil", "Haití"), ("17", "24/06 16h", "Marruecos", "Haití"), ("18", "24/06 16h", "Escocia", "Brasil")],
        "GRUPO D": [("19", "13/06 19h", "EE.UU.", "Paraguay"), ("20", "14/06 22h", "Australia", "Turquía"), ("21", "19/06 13h", "EE.UU.", "Australia"), ("22", "20/06 22h", "Turquía", "Paraguay"), ("23", "26/06 20h", "Paraguay", "Australia"), ("24", "26/06 20h", "Turquía", "EE.UU.")],
        "GRUPO E": [("25", "14/06 11h", "Alemania", "Curazao"), ("26", "15/06 17h", "Costa de Marfil", "Ecuador"), ("27", "20/06 14h", "Alemania", "Costa de Marfil"), ("28", "21/06 18h", "Ecuador", "Curazao"), ("29", "25/06 14h", "Curazao", "Costa de Marfil"), ("30", "25/06 14h", "Ecuador", "Alemania")],
        "GRUPO F": [("31", "14/06 14h", "Países Bajos", "Japón"), ("32", "15/06 20h", "Suecia", "Túnez"), ("33", "20/06 11h", "Países Bajos", "Suecia"), ("34", "21/06 22h", "Túnez", "Japón"), ("35", "26/06 17h", "Japón", "Suecia"), ("36", "26/06 17h", "Túnez", "Países Bajos")],
        "GRUPO G": [("37", "15/06 13h", "Bélgica", "Egipto"), ("38", "16/06 19h", "Irán", "Nueva Zelanda"), ("39", "21/06 13h", "Bélgica", "Irán"), ("40", "22/06 19h", "Nueva Zelanda", "Egipto"), ("41", "27/06 21h", "Egipto", "Irán"), ("42", "27/06 21h", "Nueva Zelanda", "Bélgica")],
        "GRUPO H": [("43", "15/06 10h", "España", "Cabo Verde"), ("44", "15/06 16h", "Arabia Saudita", "Uruguay"), ("45", "21/06 10h", "España", "Arabia Saudita"), ("46", "21/06 16h", "Uruguay", "Cabo Verde"), ("47", "27/06 18h", "Cabo Verde", "Arabia Saudita"), ("48", "27/06 18h", "Uruguay", "España")],
        "GRUPO I": [("49", "16/06 13h", "Francia", "Senegal"), ("50", "16/06 16h", "Irak", "Noruega"), ("51", "22/06 15h", "Francia", "Irak"), ("52", "23/06 18h", "Noruega", "Senegal"), ("53", "26/06 13h", "Noruega", "Francia"), ("54", "26/06 13h", "Senegal", "Irak")],
        "GRUPO J": [("55", "17/06 19h", "Argentina", "Argelia"), ("56", "17/06 22h", "Austria", "Jordania"), ("57", "22/06 11h", "Argentina", "Austria"), ("58", "23/06 21h", "Jordania", "Argelia"), ("59", "28/06 20h", "Argelia", "Austria"), ("60", "28/06 20h", "Jordania", "Argentina")],
        "GRUPO K": [("61", "17/06 11h", "Portugal", "RD Congo"), ("62", "18/06 20h", "Uzbekistán", "Colombia"), ("63", "23/06 11h", "Portugal", "Uzbekistán"), ("64", "24/06 20h", "Colombia", "RD Congo"), ("65", "28/06 17h", "Colombia", "Portugal"), ("66", "28/06 17h", "RD Congo", "Uzbekistán")],
        "GRUPO L": [("67", "17/06 14h", "Inglaterra", "Croacia"), ("68", "18/06 17h", "Ghana", "Panamá"), ("69", "23/06 14h", "Inglaterra", "Ghana"), ("70", "24/06 17h", "Panamá", "Croacia"), ("71", "27/06 15h", "Croacia", "Ghana"), ("72", "27/06 15h", "Panamá", "Inglaterra")]
    }

calendario = obtener_calendario()
pronosticos = {}

# Generación dinámica usando Expanders
for grupo, partidos in calendario.items():
    with st.expander(f"📌 {grupo}"): # Esta es la función de contraer/desplegar
        for p in partidos:
            cols = st.columns([3, 2, 1, 2, 3])
            cols[0].write(f"P{p[0]} | {p[1]}")
            cols[1].write(f"**{p[2]}**")
            loc = cols[2].number_input("L", key=f"l{p[0]}", min_value=0, label_visibility="collapsed")
            cols[2].markdown('<div class="vs-text">vs</div>', unsafe_allow_html=True)
            vis = cols[3].number_input("V", key=f"v{p[0]}", min_value=0, label_visibility="collapsed")
            cols[4].write(f"**{p[3]}**")
            pronosticos[p[0]] = {"local": loc, "visitante": vis}

if st.button("💾 GUARDAR Y FINALIZAR"):
    if nombre:
        data = {"participante": nombre, "pronosticos": pronosticos}
        st.download_button("📥 Descargar JSON", json.dumps(data), f"Quiniela_{nombre.replace(' ', '_')}.json")
        st.success("¡Pronósticos capturados! Presiona Ctrl+P para guardar como PDF.")
    else:
        st.error("Por favor, ingresa tu nombre.")
