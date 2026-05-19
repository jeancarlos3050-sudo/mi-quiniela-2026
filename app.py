import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS mejorados
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    h1 {color: #ffbc42 !important; text-align: center;}
    .partido-box {background-color: #1c2541; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 4px solid #ffbc42;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

def obtener_calendario_detallado():
    return {
        "GRUPO A": [
            {"#": "01", "hora": "11/06 - 13:00 h", "local": "México", "visitante": "Sudáfrica"},
            {"#": "02", "hora": "11/06 - 20:00 h", "local": "Corea del Sur", "visitante": "Chequia"},
            {"#": "03", "hora": "18/06 - 19:00 h", "local": "México", "visitante": "Corea del Sur"},
            {"#": "04", "hora": "18/06 - 12:00 h", "local": "Chequia", "visitante": "Sudáfrica"},
            {"#": "05", "hora": "24/06 - 22:00 h", "local": "México", "visitante": "Chequia"},
            {"#": "06", "hora": "24/06 - 22:00 h", "local": "Sudáfrica", "visitante": "Corea del Sur"}
        ]
        # Puedes seguir agregando los otros grupos aquí manteniendo esta misma estructura
    }

calendario = obtener_calendario_detallado()
pronosticos = {}

for grupo, juegos in calendario.items():
    st.subheader(grupo)
    for juego in juegos:
        st.markdown(f'<div class="partido-box">', unsafe_allow_html=True)
        cols = st.columns([4, 1, 1, 4])
        cols[0].write(f"Partido {juego['#']} | {juego['hora']}")
        cols[1].write(f"**{juego['local']}**")
        loc = cols[2].number_input("L", min_value=0, key=f"l{juego['#']}", label_visibility="collapsed")
        vis = cols[2].number_input("V", min_value=0, key=f"v{juego['#']}", label_visibility="collapsed")
        cols[3].write(f"**{juego['visitante']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        pronosticos[juego['#']] = {"local": loc, "visitante": vis}

if st.button("💾 GUARDAR PRONÓSTICOS"):
    if nombre:
        data = {"participante": nombre, "pronosticos": pronosticos}
        st.download_button("📥 Descargar Archivo JSON", json.dumps(data), file_name=f"Quiniela_{nombre.replace(' ', '_')}.json")
