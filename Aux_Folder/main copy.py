import os
import subprocess
import sys
import streamlit as st
from fetch_data import fetch_data, fetch_providers, fetch_years
from process_data import process_data

# Instalar dependencias desde requirements.txt
def install_dependencies():
    """Instala las librerías requeridas desde requirements.txt."""
    if os.path.exists("requirements.txt"):
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        st.warning("El archivo requirements.txt no se encontró. Por favor verifica.")

# Instalar dependencias antes de cualquier otra importación
install_dependencies()

# Configuración de la aplicación
st.set_page_config(page_title="Análisis de Servicios Móviles en Colombia")

# Título y descripción inicial
st.title("Sistema de Información para la analítica de datos de Servicios Móviles en Colombia")
st.write("""
Bienvenido a esta aplicación interactiva para analizar datos de servicios móviles en Colombia. 
Selecciona los parámetros de análisis y haz clic en **Cargar Datos** para obtener la información.
""")

# Selección de tabla
table = st.selectbox("Selecciona la Tabla de Datos", ["telefonia_movil", "internet_movil"], key="table")

# Obtener lista de proveedores
st.write("Cargando proveedores disponibles desde la API...")
providers = fetch_providers(table)

# Selección de proveedores con persistencia automática en st.session_state
selected_providers = st.multiselect(
    "Selecciona Proveedores",
    providers,
    default=st.session_state.get("selected_providers", []),  # Usar el estado persistente si existe
    key="selected_providers"  # Esto actualiza automáticamente el estado
)

# Consultar los años con datos disponibles desde la API
st.write("Cargando años disponibles desde la API...")
available_years = fetch_years(table)  # Consulta dinámica de años disponibles
years = st.multiselect(
    "Selecciona los Años",
    available_years,  # Mostrar solo los años obtenidos de la API
    default=st.session_state.get("selected_years", []),  # Usar el estado persistente si existe
    key="selected_years"  # Esto actualiza automáticamente el estado
)

# Botón para cargar datos
if st.button("Cargar Datos"):
    if not st.session_state.selected_providers:
        st.warning("Por favor selecciona al menos un proveedor.")
    elif not st.session_state.selected_years:
        st.warning("Por favor selecciona al menos un año.")
    else:
        # Construir filtros para la consulta
        filters = {}
        if st.session_state.selected_providers:
            # Construir filtro de proveedores usando IN
            providers_list = ", ".join([f"\"{p}\"" for p in st.session_state.selected_providers])
            filters["proveedor"] = f"IN ({providers_list})"
        if st.session_state.selected_years:
            # Construir filtro para años usando IN
            years_list = ", ".join([f"\"{y}\"" for y in st.session_state.selected_years])
            filters["a_o"] = f"IN ({years_list})"

        # Obtener y procesar los datos desde la API
        st.write("Cargando datos desde la API...")
        raw_data = fetch_data(table, filters=filters, limit=1000)
        data = process_data(raw_data, table)

        # Mostrar datos procesados
        st.write("### Muestra de los Datos Procesados:")
        st.dataframe(data)
