import os
import subprocess
import sys
import streamlit as st
from fetch_data import fetch_data, fetch_providers
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

# Título de la aplicación
st.title("Sistema de Información para la analítica de datos de Servicios Móviles en Colombia")
st.write("""
Bienvenido a esta aplicación interactiva para analizar datos de servicios móviles en Colombia. 
Selecciona uno o más proveedores para explorar los datos disponibles.
""")

# Persistir el estado de la selección
if "selected_providers" not in st.session_state:
    st.session_state.selected_providers = []
if "available_years" not in st.session_state:
    st.session_state.available_years = []
if "available_trimestres" not in st.session_state:
    st.session_state.available_trimestres = []

# Selección de la tabla
table = st.selectbox("Selecciona la Tabla de Datos", ["telefonia_movil", "internet_movil"])

# Obtener lista de proveedores
st.write("Cargando proveedores desde la API...")
providers = fetch_providers(table)
selected_providers = st.multiselect(
    "Selecciona Proveedores",
    providers,
    default=st.session_state.selected_providers
)

# Actualizar años y trimestres disponibles cuando cambian los proveedores seleccionados
if set(selected_providers) != set(st.session_state.selected_providers):
    st.session_state.selected_providers = selected_providers
    if selected_providers:
        filtered_data = fetch_data(
            table,
            filters={"proveedor": f"({', '.join([f"'{p}'" for p in selected_providers])})"},
            limit=1000
        )
        st.session_state.available_years = filtered_data["a_o"].unique().tolist()
        st.session_state.available_trimestres = filtered_data["trimestre"].unique().tolist()
    else:
        st.session_state.available_years = []
        st.session_state.available_trimestres = []

# Selección de Año
year = st.selectbox("Selecciona el Año", st.session_state.available_years)

# Selección de Trimestre
trimestre = st.selectbox("Selecciona el Trimestre", st.session_state.available_trimestres)

# Botón para ejecutar análisis
if st.button("Ejecutar Análisis"):
    st.write("Cargando datos desde la API...")

    # Construir filtros para la consulta
    filters = {"a_o": year, "trimestre": trimestre}
    
    # Construir filtros para múltiples proveedores
    if selected_providers:
    # Construir filtro de proveedores usando IN
        providers_list = ", ".join([f"\"{p}\"" for p in selected_providers])
        filters["proveedor"] = f"IN ({providers_list})"

    # Obtener los datos de la API
    raw_data = fetch_data(table, filters=filters, limit=1000)
    data = process_data(raw_data, table)

    st.write("### Muestra de los Datos Procesados:")
    st.write(data.head())

    # Visualizaciones
    if table == "telefonia_movil":
        st.write("### Gráficos de Consumo e Ingresos Operacionales")
        plot_consumption(data, selected_providers)
        plot_income(data, selected_providers)
    elif table == "internet_movil":
        st.write("### Gráficos de Abonados por Tecnología y Segmento")
        plot_abonados(data, selected_providers)