import os
import subprocess
import sys
import streamlit as st
from fetch_data import fetch_data, fetch_providers, fetch_years
from process_data import process_data
from visualization import plot_consumption, plot_income, plot_abonados

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
Puedes explorar gráficos sobre consumo, ingresos, y número de abonados por proveedor, segmento, y tecnología. 
Por favor, haz clic en el botón de abajo para comenzar el análisis.
""")

# Persistencia del estado con st.session_state
if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False

if st.button("Iniciar Análisis") or st.session_state.analysis_started:
    st.session_state.analysis_started = True  # Mantener el estado

    st.write("### Selecciona los Parámetros para el Análisis")

    # Selección de tabla
    table = st.selectbox("Selecciona la Tabla de Datos", ["telefonia_movil", "internet_movil"], key="table")

    # Obtener lista de años disponibles
    st.write("Cargando años disponibles desde la API...")
    years = fetch_years(table)
    year = st.selectbox("Selecciona el Año", years, key="year")

    # Obtener lista de proveedores según la tabla seleccionada
    st.write("Cargando proveedores disponibles desde la API...")
    providers = fetch_providers(table)

    # Establecer el primer proveedor como valor por defecto
    if "selected_providers" not in st.session_state:
        st.session_state.selected_providers = []

    # Crear el widget de selección múltiple usando el estado actual
    selected_providers = st.multiselect(
        "Selecciona Proveedores",
        providers,
        key="selected_providers"
)

    # Selección de trimestre
    trimestre = st.selectbox("Selecciona el Trimestre", ["1", "2", "3", "4"], key="trimestre")

    # Construir filtros para la consulta
    filters = {"a_o": str(year), "trimestre": trimestre}
    if selected_providers:
        filters["proveedor"] = selected_providers[0]  # Solo el primer proveedor seleccionado

    # Obtener y procesar los datos desde la API
    st.write("Cargando datos desde la API...")
    raw_data = fetch_data(table, filters=filters, limit=1000)
    data = process_data(raw_data, table)

    # Mostrar datos procesados
    st.write("### Muestra de los Datos Procesados:")
    st.write(data.head())

    # Visualizaciones según la tabla seleccionada
    if table == "telefonia_movil":
        st.write("### Gráficos de Consumo e Ingresos Operacionales")
        plot_consumption(data, selected_providers)
        plot_income(data, selected_providers)
    elif table == "internet_movil":
        st.write("### Gráficos de Abonados por Tecnología y Segmento")
        plot_abonados(data, selected_providers)
else:
    st.write("Haz clic en el botón para iniciar el análisis.")
