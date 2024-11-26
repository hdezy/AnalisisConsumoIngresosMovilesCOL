import streamlit as st
import pandas as pd
import plotly.express as px

import pandas as pd

def preprocess_telefonia_data(data):
    """
    Preprocesa los datos de Telefonía Móvil para análisis:
    - Limpia y convierte columnas de consumo a valores numéricos.
    - Elimina filas donde ambos consumos son cero.
    - Agrega una columna 'Periodo' con la fecha de inicio de cada trimestre.

    Args:
        data (pd.DataFrame): Datos originales de Telefonía Móvil.

    Returns:
        pd.DataFrame: Datos preprocesados.
    """
    # Convertir columnas a valores numéricos
    data = data.copy()  # Crear una copia del DataFrame original

    # Imprimir valores iniciales para consumo_prepago
    print("Valores iniciales de consumo_prepago:")
    print(data[["a_o","trimestre","consumo_prepago","consumo_pospago","ingresos_operacionales"]].head(10))


    # data['consumo_prepago'] = data["consumo_prepago"].astype(str).str.replace(",", ".", regex=False).str.replace(r"\.", "", regex=True).astype(float)
    # data['consumo_prepago'] = data["consumo_prepago"].astype(str).str.replace('"', '', regex=False).str.split(",").str[0].str.replace(r"\.", "", regex=True).astype(float)
    # data['consumo_prepago'] = data["consumo_prepago"].astype(str).str.replace('"', '', regex=False).str.replace(",", ".", regex=False).str.replace(r"\.", "", regex=True)
    data['consumo_prepago'] = data["consumo_prepago"].astype(str).str.replace('"', '', regex=False).str.replace(",", ".", regex=False).str.replace(r"\.(?=\d{3}($|\.))", "", regex=True)
    data['consumo_pospago'] = data["consumo_pospago"].astype(str).str.replace(",", ".", regex=False).str.replace(r"\.", "", regex=True).astype(float)
    data['ingresos_operacionales'] = data["ingresos_operacionales"].astype(str).str.replace(",", ".", regex=False).str.replace(r"\.", "", regex=True).astype(float)

    # Imprimir valores iniciales para consumo_prepago
    print("Valores procesados de consumo_prepago:")
    print(data[["a_o","trimestre","consumo_prepago","consumo_pospago","ingresos_operacionales"]].head(10))

    data['consumo_prepago'] = data["consumo_prepago"].astype(float)

    # Imprimir valores iniciales para consumo_prepago
    print("Valores ultraprocesados de consumo_prepago:")
    print(data[["a_o","trimestre","consumo_prepago","consumo_pospago","ingresos_operacionales"]].head(10))

    # Reemplazar valores nulos por 0
    data['consumo_prepago'] = data['consumo_prepago'].fillna(0)
    data['consumo_pospago'] = data['consumo_pospago'].fillna(0)

    
    # Convertir Año y Trimestre a strings para concatenar
    data['a_o'] = data['a_o'].astype(str)
    data['trimestre'] = data['trimestre'].astype(str)

    # Crear una lista de los primeros días de cada trimestre
    # primeros_dias_trimestre = ['01-01', '04-01', '07-01', '10-01']
    primeros_dias_trimestre = ['03-01', '06-01', '09-01', '12-01']

    # Mapear el trimestre a su correspondiente primer día
    data['Periodo'] = data.apply(
        lambda row: pd.to_datetime(row['a_o'] + '-' + primeros_dias_trimestre[int(row['trimestre'])-1]),
        axis=1
    )

    # Ordenar datos por la columna 'Periodo'
    data = data.sort_values(by='Periodo').reset_index(drop=True)

    # Verificar tipos de datos
    # print(data.dtypes)

    # Verificar agrupación y sumas manualmente
    grouped_data = data.groupby("Periodo")[["consumo_prepago", "consumo_pospago", "ingresos_operacionales"]].sum()
    print(grouped_data)

    return data

def sumar_por_periodo(data):
    """
    Agrupa los datos por periodo y suma las columnas de consumo.
    Args:
        data (pd.DataFrame): Datos preprocesados.
    Returns:
        pd.DataFrame: Datos agrupados por periodo con las sumas totales.
    """
    # Asegurarse de que las columnas de consumo no tengan valores nulos
    data['consumo_prepago'] = data['consumo_prepago'].fillna(0)
    data['consumo_pospago'] = data['consumo_pospago'].fillna(0)

    # Imprimir datos antes de la agrupación
    print("Datos antes de la agrupación:")
    print(data[['Periodo', 'consumo_prepago', 'consumo_pospago']].head(20))

    # Agrupar y sumar
    grouped_data = data.groupby("Periodo")[["consumo_prepago", "consumo_pospago"]].sum().reset_index()

    # Imprimir datos después de la agrupación
    print("Datos agrupados:")
    print(grouped_data.head(10))

    return grouped_data


# Sección: Gráficas/Tablas para Datos de Telefonía
def telefonia_visualizations(data):
    """
    Genera las gráficas y tablas específicas para los datos de Telefonía Móvil.
    """
    # Botón para generar gráficas/tablas
    #if st.button("Generar Gráficas de Telefonía Móvil"):
    
    ## Gráfica: Distribución de Ingresos por Segmento (Prepago vs Pospago)
    st.write("### Distribución de Ingresos por Segmento (Prepago vs Pospago)")
    st.write("""
    Este gráfico muestra cómo se distribuyen los ingresos operacionales totales entre los segmentos de Prepago y Pospago 
    para todos los proveedores en cada periodo.
    """)

    sumar_por_periodo(data)

    # Agrupar los datos por periodo y calcular la suma total de ingresos para cada segmento
    grouped_data = data.groupby("Periodo")[["consumo_prepago", "consumo_pospago"]].sum().reset_index()

    # Transformar datos al formato largo para la visualización
    melted_data = pd.melt(
        grouped_data,
        id_vars=["Periodo"],
        value_vars=["consumo_prepago", "consumo_pospago"],
        var_name="Segmento",
        value_name="Ingresos"
    )

    # Reemplazar valores de "Segmento" para mejor visualización
    melted_data["Segmento"] = melted_data["Segmento"].replace({
        "consumo_prepago": "Prepago",
        "consumo_pospago": "Pospago"
    })

    # Crear gráfico de barras con Plotly
    fig = px.bar(
        melted_data,
        x="Periodo",
        y="Ingresos",
        color="Segmento",
        barmode="group",
        labels={"Ingresos": "Ingresos Operacionales ($)", "Periodo": "Periodo"},
        title="Distribución Total de Ingresos por Segmento (Prepago vs Pospago)",
        height=600,
    )

    # Mostrar gráfico
    st.plotly_chart(fig)

    ## Gráfica: Evolución del Consumo de Voz en Pospago
    st.write("### Evolución del Consumo de Voz en Prepago por Proveedor")
    fig_prepago = px.line(
        data,
        x="Periodo",
        y="consumo_prepago",
        color="proveedor",
        labels={"consumo_prepago": "Consumo (MM)", "Periodo": "Periodo", "proveedor": "Proveedor"},
        title="Evolución del Consumo de Voz en Prepago por Proveedor"
    )
    st.plotly_chart(fig_prepago)

    # Gráfica: Evolución del Consumo de Voz en Pospago
    st.write("### Evolución del Consumo de Voz en Pospago por Proveedor")
    fig_pospago = px.line(
        data,
        x="Periodo",
        y="consumo_pospago",
        color="proveedor",
        labels={"consumo_pospago": "Consumo (MM)", "Periodo": "Periodo", "proveedor": "Proveedor"},
        title="Evolución del Consumo de Voz en Pospago por Proveedor"
    )
    st.plotly_chart(fig_pospago)

# Sección: Gráficas/Tablas para Datos de Internet
def internet_visualizations(data):
    """
    Genera las gráficas y tablas específicas para los datos de Internet Móvil.
    """
    st.title("Gráficas y Tablas: Datos de Internet Móvil")

    # Botón para generar gráficas/tablas
    if st.button("Generar Gráficas de Internet Móvil"):
        st.write("### Gráfica 1: Distribución de Abonados por Tecnología")
        # Ejemplo de gráfica
        fig2 = px.bar(data, x="proveedor", y="no_abonados", color="tecnolog_a",
                      title="Distribución de Abonados por Tecnología",
                      labels={"no_abonados": "Número de Abonados", "tecnolog_a": "Tecnología"})
        st.plotly_chart(fig2)

        st.write("### Tabla 1: Resumen de Abonados por Segmento y Tecnología")
        # Ejemplo de tabla
        abonados_summary = data.groupby(["segmento", "tecnolog_a"])[["no_abonados"]].sum().reset_index()
        st.dataframe(abonados_summary)

# Sección: Gráficas/Tablas Combinadas (Telefonía e Internet Móvil)
def combined_visualizations(telefonia_data, internet_data):
    """
    Genera las gráficas y tablas combinadas utilizando datos de Telefonía e Internet Móvil.
    """
    st.title("Gráficas y Tablas Combinadas: Telefonía e Internet Móvil")

    # Botón para generar gráficas/tablas
    if st.button("Generar Gráficas Combinadas"):
        st.write("### Gráfica 1: Relación entre Abonados de Internet y Consumo de Voz")
        # Ejemplo de gráfica
        combined_data = pd.merge(telefonia_data, internet_data, on="proveedor", how="inner")
        fig3 = px.scatter(combined_data, x="no_abonados", y="consumo_prepago",
                          size="ingresos_operacionales", color="proveedor",
                          title="Relación entre Abonados de Internet y Consumo de Voz",
                          labels={"no_abonados": "Abonados de Internet", "consumo_prepago": "Consumo de Voz (MM)"})
        st.plotly_chart(fig3)

        st.write("### Tabla 1: Resumen Combinado de Métricas por Proveedor")
        # Ejemplo de tabla combinada
        combined_summary = combined_data.groupby("proveedor")[["no_abonados", "ingresos_operacionales"]].sum()
        st.dataframe(combined_summary)

# Función principal para ejecutar las visualizaciones
def main_visualizations():
    """
    Función principal para gestionar las secciones de visualización.
    """
    st.sidebar.title("Secciones de Visualización")
    section = st.sidebar.selectbox("Selecciona la Sección", ["Telefonía", "Internet", "Combinadas"])

    # Verificar si los datos están disponibles en la sesión
    telefonia_data = st.session_state.get("telefonia_data", None)
    internet_data = st.session_state.get("internet_data", None)

    # Seleccionar y mostrar la sección correspondiente
    if section == "Telefonía" and telefonia_data is not None:
        telefonia_data = preprocess_telefonia_data(telefonia_data)
        telefonia_visualizations(telefonia_data)
    elif section == "Internet" and internet_data is not None:
        internet_visualizations(internet_data)
    elif section == "Combinadas" and telefonia_data is not None and internet_data is not None:
        combined_visualizations(telefonia_data, internet_data)
    else:
        st.warning("No se encontraron datos para esta sección. Por favor, carga los datos desde la API en el menú principal.")
