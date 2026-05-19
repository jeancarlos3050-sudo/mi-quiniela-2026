import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="centered")

# Estilos CSS para el modo oscuro
st.markdown("""
    <style>
    .stApp {background-color: #0b132b; color: white;}
    h1 {color: #ffbc42 !important; text-align: center;}
    .stButton>button {width: 100%; background-color: #2a9d8f; color: white; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 MUNDIAL 2026: PRONÓSTICOS")
nombre = st.text_input("Nombre Completo del Participante")

# Función con los 72 partidos
def obtener_calendario():
    return {
        "Grupo A": [{"#": "01", "local": "México", "visitante": "Sudáfrica"}, {"#": "02", "local": "Corea del Sur", "visitante": "Chequia"}, {"#": "03", "local": "México", "visitante": "Corea del Sur"}, {"#": "04", "local": "Chequia", "visitante": "Sudáfrica"}, {"#": "05", "local": "México", "visitante": "Chequia"}, {"#": "06", "local": "Sudáfrica", "visitante": "Corea del Sur"}],
        "Grupo B": [{"#": "07", "local": "Canadá", "visitante": "Bosnia y Herzegovina"}, {"#": "08", "local": "Qatar", "visitante": "Suiza"}, {"#": "09", "local": "Canadá", "visitante": "Qatar"}, {"#": "10", "local": "Suiza", "visitante": "Bosnia y Herzegovina"}, {"#": "11", "local": "Suiza", "visitante": "Canadá"}, {"#": "12", "local": "Bosnia y Herzegovina", "visitante": "Qatar"}],
        "Grupo C": [{"#": "13", "local": "Brasil", "visitante": "Marruecos"}, {"#": "14", "local": "Haití", "visitante": "Escocia"}, {"#": "15", "local": "Brasil", "visitante": "Haití"}, {"#": "16", "local": "Escocia", "visitante": "Marruecos"}, {"#": "17", "local": "Escocia", "visitante": "Brasil"}, {"#": "18", "local": "Marruecos", "visitante": "Haití"}],
        "Grupo D": [{"#": "19", "local": "Estados Unidos", "visitante": "Paraguay"}, {"#": "20", "local": "Australia", "visitante": "Turquía"}, {"#": "21", "local": "Estados Unidos", "visitante": "Australia"}, {"#": "22", "local": "Turquía", "visitante": "Paraguay"}, {"#": "23", "local": "Estados Unidos", "visitante": "Turquía"}, {"#": "24", "local": "Paraguay", "visitante": "Australia"}],
        "Grupo E": [{"#": "25", "local": "Alemania", "visitante": "Curazao"}, {"#": "26", "local": "Costa de Marfil", "visitante": "Ecuador"}, {"#": "27", "local": "Alemania", "visitante": "Costa de Marfil"}, {"#": "28", "local": "Ecuador", "visitante": "Curazao"}, {"#": "29", "local": "Ecuador", "visitante": "Alemania"}, {"#": "30", "local": "Curazao", "visitante": "Costa de Marfil"}],
        "Grupo F": [{"#": "31", "local": "Países Bajos", "visitante": "Japón"}, {"#": "32", "local": "Suecia", "visitante": "Túnez"}, {"#": "33", "local": "Países Bajos", "visitante": "Suecia"}, {"#": "34", "local": "Túnez", "visitante": "Japón"}, {"#": "35", "local": "Japón", "visitante": "Suecia"}, {"#": "36", "local": "Túnez", "visitante": "Países Bajos"}],
        "Grupo G": [{"#": "37", "local": "Bélgica", "visitante": "Egipto"}, {"#": "38", "local": "Irán", "visitante": "Nueva Zelanda"}, {"#": "39", "local": "Bélgica", "visitante": "Irán"}, {"#": "40", "local": "Nueva Zelanda", "visitante": "Egipto"}, {"#": "41", "local": "Egipto", "visitante": "Irán"}, {"#": "42", "local": "Nueva Zelanda", "visitante": "Bélgica"}],
        "Grupo H": [{"#": "43", "local": "España", "visitante": "Cabo Verde"}, {"#": "44", "local": "Arabia Saudita", "visitante": "Uruguay"}, {"#": "45", "local": "España", "visitante": "Arabia Saudita"}, {"#": "46", "local": "Uruguay", "visitante": "Cabo Verde"}, {"#": "47", "local": "Cabo Verde", "visitante": "Arabia Saudita"}, {"#": "48", "local": "Uruguay", "visitante": "España"}],
        "Grupo I": [{"#": "49", "local": "Francia", "visitante": "Senegal"}, {"#": "50", "local": "Irak", "visitante": "Noruega"}, {"#": "51", "local": "Francia", "visitante": "Irak"}, {"#": "52", "local": "Noruega", "visitante": "Senegal"}, {"#": "53", "local": "Noruega", "visitante": "Francia"}, {"#": "54", "local": "Senegal", "visitante": "Irak"}],
        "Grupo J": [{"#": "55", "local": "Argentina", "visitante": "Argelia"}, {"#": "56", "local": "Austria", "visitante": "Jordania"}, {"#": "57", "local": "Argentina", "visitante": "Austria"}, {"#": "58", "local": "Jordania", "visitante": "Argelia"}, {"#": "59", "local": "Jordania", "visitante": "Argentina"}, {"#": "60", "local": "Argelia", "visitante": "Austria"}],
        "Grupo K": [{"#": "61", "local": "Portugal", "visitante": "RD Congo"}, {"#": "62", "local": "Uzbekistán", "visitante": "Colombia"}, {"#": "63", "local": "Portugal", "visitante": "Uzbekistán"}, {"#": "64", "local": "Colombia", "visitante": "RD Congo"}, {"#": "65", "local": "Colombia", "visitante": "Portugal"}, {"#": "66", "local": "RD Congo", "visitante": "Uzbekistán"}],
        "Grupo L": [{"#": "67", "local": "Inglaterra", "visitante": "Croacia"}, {"#": "68", "local": "Ghana", "visitante": "Panamá"}, {"#": "69", "local": "Inglaterra", "visitante": "Ghana"}, {"#": "70", "local": "Panamá", "visitante": "Croacia"}, {"#": "71", "local": "Panamá", "visitante": "Inglaterra"}, {"#": "72", "local": "Croacia", "visitante": "Ghana"}]
    }

calendario = obtener_calendario()
pronosticos = {}

# Interfaz dinámica
for grupo, juegos in calendario.items():
    with st.expander(f"📍 {grupo}"):
        for juego in juegos:
            c1, c2, c3 = st.columns([3, 2, 3])
            with c1: st.write(f"**{juego['local']}**")
            with c2:
                loc = st.number_input("L", min_value=0, key=f"l{juego['#']}")
                vis = st.number_input("V", min_value=0, key=f"v{juego['#']}")
            with c3: st.write(f"**{juego['visitante']}**")
            pronosticos[juego['#']] = {"local": loc, "visitante": vis}

# Guardar información
if st.button("💾 GUARDAR PRONÓSTICOS"):
    if nombre:
        data = {"participante": nombre, "pronosticos": pronosticos}
        st.download_button("📥 Descargar Archivo JSON", json.dumps(data), file_name=f"Quiniela_{nombre.replace(' ', '_')}.json")
    else:
        st.error("Por favor, ingresa tu nombre primero.")