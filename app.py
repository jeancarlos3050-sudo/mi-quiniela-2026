import streamlit as st
import json
from fpdf import FPDF

st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# --- CSS BÁSICO ---
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# 1. Definición clara del calendario
def obtener_calendario():
    return {
        "GRUPO A": [("01", "México", "Sudáfrica"), ("02", "Corea del Sur", "Chequia")],
        "GRUPO B": [("07", "Canadá", "Bosnia")]
    }

# 2. Gestión de limpieza mediante un botón que usa st.rerun() puro
if st.button("🧹 LIMPIAR TODO"):
    st.session_state.clear()
    st.rerun()

nombre = st.text_input("Nombre Completo del Participante:")

# 3. Renderizado simple sin variables complejas que causen conflictos
calendario = obtener_calendario()

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            # Creamos columnas nuevas por cada iteración
            c1, c2, c3, c4 = st.columns([2, 1, 1, 2])
            c1.write(juego[1])
            c2.number_input(f"L{juego[0]}", key=f"L{juego[0]}")
            c3.number_input(f"V{juego[0]}", key=f"V{juego[0]}")
            c4.write(juego[2])

# 4. Botón de guardado simplificado
if st.button("💾 GUARDAR"):
    st.success("Guardado")
