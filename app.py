import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS para el diseño profesional
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    h1 {color: #ffbc42 !important; text-align: center;}
    h2 {color: #ffbc42 !important; border-bottom: 2px solid #ffbc42; padding-bottom: 10px;}
    .partido-box {
        background-color: #1c2541; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 10px; 
        border: 1px solid #3a506b;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante:")

# Función que contiene todos los partidos
def obtener_calendario():
    return {
        "GRUPO A": [
            {"#": "01", "hora": "11/06 - 13:00 h", "local": "México", "visitante": "Sudáfrica"},
            {"#": "02", "hora": "11/06 - 20:00 h", "local": "Corea del Sur", "visitante": "Chequia"},
            {"#": "03", "hora": "18/06 - 19:00 h", "local": "México", "visitante": "Corea del Sur"},
            {"#": "04", "hora": "18/06 - 12:00 h", "local": "Chequia", "visitante": "Sudáfrica"},
            {"#": "05", "hora": "24/06 - 22:00 h", "local": "México", "visitante": "Chequia"},
            {"#": "06", "hora": "24/06 - 22:00 h", "local": "Sudáfrica", "visitante": "Corea del Sur"}
        ]
        # Puedes seguir añadiendo más grupos aquí siguiendo esta misma estructura
    }

calendario = obtener_calendario()
pronosticos = {}

# Generar la interfaz
for grupo, juegos in calendario.items():
    st.subheader(grupo)
    for juego in juegos:
        st.markdown('<div class="partido-box">', unsafe_allow_html=True)
        # Distribución de columnas: 4 de info, 1 de gol local, 1 vs, 1 de gol visitante, 4 de info
        cols = st.columns([4, 2, 1, 2, 4])
        
        cols[0].write(f"Partido {juego['#']} | {juego['hora']}")
        cols[1].write(f"**{juego['local']}**")
        
        # Inputs compactos (number_input)
        loc = cols[2].number_input("L", min_value=0, max_value=20, key=f"l{juego['#']}", label_visibility="collapsed")
        # Usamos una columna vacía o texto para el 'vs'
        cols[2].write("vs")
        vis = cols[2].number_input("V", min_value=0, max_value=20, key=f"v{juego['#']}", label_visibility="collapsed")
        
        cols[3].write(f"**{juego['visitante']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        pronosticos[juego['#']] = {"local": loc, "visitante": vis}

# Guardar
if st.button("💾 GUARDAR PRONÓSTICOS"):
    if nombre:
        data = {"participante": nombre, "pronosticos": pronosticos}
        st.download_button(
            label="📥 Descargar Archivo JSON", 
            data=json.dumps(data), 
            file_name=f"Quiniela_{nombre.replace(' ', '_')}.json"
        )
    else:
        st.error("¡Por favor ingresa tu nombre!")
