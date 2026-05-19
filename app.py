import streamlit as st
import json
from fpdf import FPDF

# Configuración
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS para mantener la estética
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    .stNumberInput {width: 70px !important;}
    </style>
""", unsafe_allow_html=True)

# 1. FUNCIÓN DE LIMPIEZA SEGURA
def limpiar_todo():
    st.session_state.clear()
    st.rerun()

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# Input del nombre (asignado a session_state)
if 'nombre_usuario' not in st.session_state:
    st.session_state.nombre_usuario = ""

nombre = st.text_input("Nombre del Participante:", value=st.session_state.nombre_usuario)
st.session_state.nombre_usuario = nombre

# 2. CALENDARIO COMPLETO
calendario = {
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

# 3. RENDERIZADO SIN COLUMNAS GLOBALES (Evita el TypeError)
for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            # Creamos un layout más sencillo que no dependa de objetos cols persistentes
            st.write(f"**P{juego[0]}**: {juego[1]} vs {juego[2]}")
            c1, c2 = st.columns(2)
            c1.number_input(f"L{juego[0]}", key=f"L{juego[0]}", min_value=0)
            c2.number_input(f"V{juego[0]}", key=f"V{juego[0]}", min_value=0)

# 4. BOTONES
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("💾 Guardar"):
        st.write("Guardando...")

with col_btn2:
    if st.button("📄 PDF"):
        st.write("Generando...")

with col_btn3:
    # Este botón llama a la función de limpieza sin errores
    if st.button("🧹 LIMPIAR TODO"):
        limpiar_todo()
