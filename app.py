import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS para el diseño profesional
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    h1 {color: #ffbc42 !important; text-align: center;}
    .partido-box {
        background-color: #1c2541; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 10px; 
        border-left: 5px solid #ffbc42;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario():
    return {
        "GRUPO A": [
            {"#": "01", "hora": "11/06 - 13:00 h", "local": "México", "visitante": "Sudáfrica"},
            {"#": "02", "hora": "11/06 - 20:00 h", "local": "Corea del Sur", "visitante": "Chequia"}
            # Puedes añadir el resto de los partidos siguiendo este mismo formato
        ]
    }

calendario = obtener_calendario()
pronosticos = {}

for grupo, juegos in calendario.items():
    st.subheader(grupo)
    for juego in juegos:
        st.markdown(f'<div class="partido-box">', unsafe_allow_html=True)
        # Definimos 4 columnas: 3 para info, 1 para gol local, 1 para gol visitante, 3 para info visitante
        # Ajusta los números si necesitas más o menos espacio
        cols = st.columns([3.5, 1, 1, 3.5])
        
        cols[0].write(f"Partido {juego['#']} | {juego['hora']}")
        cols[1].write(f"**{juego['local']}**")
        
        # Inputs alineados al centro
        loc = cols[2].number_input("L", min_value=0, key=f"l{juego['#']}", label_visibility="collapsed")
        vis = cols[2].number_input("V", min_value=0, key=f"v{juego['#']}", label_visibility="collapsed")
        
        cols[3].write(f"**{juego['visitante']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        pronosticos[juego['#']] = {"local": loc, "visitante": vis}

if st.button("💾 GUARDAR PRONÓSTICOS"):
    if nombre:
        data = {"participante": nombre, "pronosticos": pronosticos}
        st.download_button(
            label="📥 Descargar Archivo JSON", 
            data=json.dumps(data), 
            file_name=f"Quiniela_{nombre.replace(' ', '_')}.json"
        )
    else:
        st.warning("Por favor, ingresa tu nombre antes de guardar.")
