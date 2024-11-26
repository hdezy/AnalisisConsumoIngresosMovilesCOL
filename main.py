import os
import streamlit as st
from fetch_data import fetch_data
from process_data import process_data
from visualization import main_visualizations  # Importa la función principal de visualización

# Instalar dependencias desde requirements.txt
def install_dependencies():
    """Instala las librerías requeridas desde requirements.txt."""
    import subprocess
    import sys

    try:
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            st.warning("El archivo requirements.txt no se encontró. Por favor verifica.")
    except Exception as e:
        st.error(f"Error al instalar dependencias: {e}")

# Instalar dependencias antes de cualquier otra importación
install_dependencies()

# Configuración de la aplicación
st.set_page_config(page_title="Análisis de Servicios Móviles en Colombia")

# Título y descripción inicial
st.title("Sistema de Información para el Análisis de Patrones de Consumo e Ingresos en Servicios Móviles de Colombia")
st.write("""
Esta aplicación permite analizar patrones de consumo e ingresos en servicios móviles en Colombia, 
incluyendo telefonía móvil e internet móvil.
""")

# Verificar si ya se han cargado los datos
if "telefonia_data" in st.session_state and "internet_data" in st.session_state:
    main_visualizations()  # Llamar a la función principal de visualización
else: 
    # Botón para cargar datos
    if st.button("Cargar Datos desde la API") :

        telefonia_message = st.empty()  # Crear un marcador de posición
        telefonia_message.write("Cargando datos de **Telefonía Móvil**...")
        telefonia_data = fetch_data("telefonia_movil", limit=10_000)  # Reemplaza con el límite adecuado
        telefonia_data = process_data(telefonia_data, "telefonia_movil")
        telefonia_message.empty()  # Eliminar el marcador de posición
        st.session_state.telefonia_data = telefonia_data
        st.dataframe(telefonia_data.head())

        internet_message = st.empty()  # Crear un marcador de posición
        internet_message.write("Cargando datos de **Internet Móvil**...")
        internet_data = fetch_data("internet_movil", limit=10_000)  # Reemplaza con el límite adecuado
        internet_data = process_data(internet_data, "internet_movil")
        internet_message.empty()  # Eliminar el marcador de posición
        st.session_state.internet_data = internet_data
        st.dataframe(internet_data.head()) # Muestra algunos de los datos cargados

        st.button("Realizar análisis de los datos")
    else:
        st.info("Haz clic en **Cargar Datos desde la API** para comenzar.")
