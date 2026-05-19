import streamlit as st
import json
from fpdf import FPDF

# Configuración base
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# CSS para estilo nítido
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    div[data-testid="stTextInput"] label p {color: #ffffff !important; font-size: 16px !important; font-weight: bold !important;}
    .stTextInput input {color: white !important; background-color: #1c2541 !important;}
    div[data-testid="stNumberInput"] input {text-align: center !important; background-color: #ffffff !important; color: #000000 !important; font-weight: bold;}
    .vs-texto {color: #ffbc42 !important; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE LIMPIEZA: Definimos los keys y los reiniciamos
def limpiar_todo():
    # Limpiamos el nombre
    st.session_state["nombre_input"] = ""
    # Limpiamos todos los marcadores (l01, v01, etc.)
    for i in range(1, 73):
        idx = str(i).zfill(2)
        st.session_state[f"l{idx}"] = 0
        st.session_state[f"v{idx}"] = 0
    st.rerun()

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")

# Input con key para control de estado
nombre = st.text_input("Nombre del Participante:", key="nombre_input")

# [Calendario idéntico...]
def obtener_calendario():
    return {"GRUPO A": [("01", "11/06 13:00", "México", "Sudáfrica"), ("02", "11/06 20:00", "Corea del Sur", "Chequia")]} # Añada aquí el resto

calendario = obtener_calendario()

for grupo, juegos in calendario.items():
    with st.expander(grupo):
        for juego in juegos:
            cols = st.columns([2, 1, 0.5, 1, 2])
            cols[0].write(f"{juego[2]} vs {juego[3]}")
            # Asignamos el key correspondiente al número de partido
            loc = st.number_input("L", min_value=0, value=0, key=f"l{juego[0]}", label_visibility="collapsed")
            cols[2].markdown('<p class="vs-texto">vs</p>', unsafe_allow_html=True)
            vis = st.number_input("V", min_value=0, value=0, key=f"v{juego[0]}", label_visibility="collapsed")

# Botones
col1, col2, col3 = st.columns(3)
if col3.button("🧹 LIMPIAR PRONÓSTICOS"):
    limpiar_todo()
