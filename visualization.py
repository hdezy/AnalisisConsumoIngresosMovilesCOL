import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

# Sección: Gráficas/Tablas para Datos de Telefonía
def telefonia_visualizations(data):
    
    """ Genera las gráficas y tablas específicas para los datos de Telefonía Móvil. """
  
    st.write("## Análisis de datos de Telefonía Móvil")
    ##################### Gráfica Distribución Total de Ingresos por Segmento (Prepago vs Pospago) #####################
    grouped_data = data.groupby("Periodo")[["consumo_prepago", "consumo_pospago"]].sum().reset_index() # Agrupar los datos por periodo y calcular la suma total de ingresos para cada segmento

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
    fig_IO_pre_pos = px.bar(
        melted_data,
        x="Periodo",
        y="Ingresos",
        color="Segmento",
        barmode="group",
        labels={"Ingresos": "Ingresos Operacionales ($)", "Periodo": "Periodo"},
        height=600,
    )

    fig_IO_pre_pos.update_layout(
    title={
        "text": "Distribución Total de Ingresos por Segmento (Prepago vs Pospago)",  # Define el texto del título
        "font": {"size": 22},  # Tamaño de la fuente del título
        "x": 0.5,  # Posición horizontal del título (0 es izquierda, 1 es derecha, 0.5 es centrado)
        "xanchor": "center",  # Asegura que esté anclado al centro
    }
    )
    
    st.plotly_chart(fig_IO_pre_pos)    # Mostrar gráfico

    ##################### Gráfica Evolución del Consumo de Voz en Prepago #####################
    fig_prepago = px.line(
        data,
        x="Periodo",
        y="consumo_prepago",
        color="proveedor",
        labels={"consumo_prepago": "Consumo (MM)", "Periodo": "Periodo", "proveedor": "Proveedor"},
    )

    fig_prepago.update_layout(
    title={
        "text": "Evolución del Consumo de Voz en Prepago por Proveedor",  # Define el texto del título
        "font": {"size": 22},  # Tamaño de la fuente del título
        "x": 0.5,  # Posición horizontal del título (0 es izquierda, 1 es derecha, 0.5 es centrado)
        "xanchor": "center",  # Asegura que esté anclado al centro
    }
    )

    st.plotly_chart(fig_prepago)     # Mostrar gráfico

    ##################### Gráfica Evolución del Consumo de Voz en Pospago #####################
    fig_pospago = px.line(
        data,
        x="Periodo",
        y="consumo_pospago",
        color="proveedor",
        labels={"consumo_pospago": "Consumo (MM)", "Periodo": "Periodo", "proveedor": "Proveedor"},
    )

    fig_pospago.update_layout(
    title={
        "text": "Evolución del Consumo de Voz en Pospago por Proveedor",  # Define el texto del título
        "font": {"size": 22},  # Tamaño de la fuente del título
        "x": 0.5,  # Posición horizontal del título (0 es izquierda, 1 es derecha, 0.5 es centrado)
        "xanchor": "center",  # Asegura que esté anclado al centro
    }
    )

    st.plotly_chart(fig_pospago)     # Mostrar gráfico

    ##################### Gráfico: Relación entre el consumo en prepago y pospago. Los puntos se colorean por proveedor. #####################
    # Crear gráfico de dispersión
    fig_correlation = px.scatter(
        data,
        x="consumo_prepago",
        y="consumo_pospago",
        color="proveedor",
        labels={
            "consumo_prepago": "Consumo en Prepago (MM)",
            "consumo_pospago": "Consumo en Pospago (MM)",
            "proveedor": "Proveedor",
            "Periodo": "Periodo"
        },
        hover_data=["Periodo"]  # Mostrar periodo al pasar el cursor
    )

    # Ajustar diseño del gráfico
    fig_correlation.update_layout(
        xaxis_title="Consumo en Prepago (MM)",
        yaxis_title="Consumo en Pospago (MM)",
        legend_title="Proveedor",
        height=600,
        title={
        "text": "Relación entre Consumo en Prepago y Pospago por Proveedor",  # Define el texto del título
        "font": {"size": 22},  # Tamaño de la fuente del título
        "x": 0.5,  # Posición horizontal del título (0 es izquierda, 1 es derecha, 0.5 es centrado)
        "xanchor": "center",  # Asegura que esté anclado al centro
        }
    )

    st.plotly_chart(fig_correlation)     # Mostrar gráfico

    ##################### Tabla: Ranking de Proveedores por Ingresos #####################
    # Agrupar los datos por proveedor y calcular ingresos acumulados
    ranking_data = data.groupby("proveedor")[["ingresos_operacionales"]].sum().reset_index()
    ranking_data = ranking_data.sort_values(by="ingresos_operacionales", ascending=False).reset_index(drop=True)
    ranking_data.index += 1  # Agregar numeración al índice para el ranking

    st.write("#### Ranking de Proveedores por Ingresos Operacionales")
    st.table(ranking_data.rename(columns={
        "proveedor": "Proveedor",
        "ingresos_operacionales": "Ingresos Operacionales Totales ($)"
    }))

def internet_visualizations(data):
    
    """ Genera visualizaciones para la distribución de abonados por tecnología y segmento. """

    st.write("## Análisis de datos de Internet Móvil")
    
    # Filtrar datos para cada segmento
    prepago_data = data[data["segmento"] == "PREPAGO"]
    pospago_data = data[data["segmento"] == "POSPAGO"]
    
    # Agrupar por Periodo y Tecnología para sumar el número de abonados
    prepago_grouped = prepago_data.groupby(["Periodo", "tecnolog_a"])[["no_abonados"]].sum().reset_index()
    pospago_grouped = pospago_data.groupby(["Periodo", "tecnolog_a"])[["no_abonados"]].sum().reset_index()
    
    # Agrupar por Periodo y Segmento para calcular la cantidad total de abonados
    abonados_total = data.groupby(["Periodo", "segmento"])[["no_abonados"]].sum().reset_index() 

    ##################### Gráfico de líneas: Total de abonados en prepago y pospago en el tiempo #####################
    fig_total_abonados = px.line(
        abonados_total,
        x="Periodo",
        y="no_abonados",
        color="segmento",
        labels={
            "no_abonados": "Número de Abonados",
            "Periodo": "Periodo",
            "segmento": "Segmento"
        }
    )

    fig_total_abonados.update_layout(
        title={
            "text": "Evolución Total de Abonados en Prepago y Pospago",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        }
    )
    st.plotly_chart(fig_total_abonados)     # Mostrar gráfico

    ##################### Gráfico de barras: Abonados por Tecnología en Prepago #####################
    abonados_tecnologia = data.groupby(["Periodo", "segmento", "tecnolog_a"])[["no_abonados"]].sum().reset_index() # Agrupar por Periodo, Segmento y Tecnología

    prepago_tecnologia = abonados_tecnologia[abonados_tecnologia["segmento"] == "PREPAGO"]

    fig_barras_prepago = px.bar(
        prepago_tecnologia,
        x="Periodo",
        y="no_abonados",
        color="tecnolog_a",
        labels={
            "no_abonados": "Número de Abonados",
            "Periodo": "Periodo",
            "tecnolog_a": "Tecnología"
        }
    )

    fig_barras_prepago.update_layout(
        title={
            "text": "Distribución de Abonados por Tecnología en Prepago",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        },
        barmode="stack",  # Barras apiladas
        height=600
    )
    st.plotly_chart(fig_barras_prepago)     # Mostrar gráfico

    ##################### Gráfico de barras: Abonados por Tecnología en Pospago #####################
    pospago_tecnologia = abonados_tecnologia[abonados_tecnologia["segmento"] == "POSPAGO"]

    fig_barras_pospago = px.bar(
        pospago_tecnologia,
        x="Periodo",
        y="no_abonados",
        color="tecnolog_a",
        labels={
            "no_abonados": "Número de Abonados",
            "Periodo": "Periodo",
            "tecnolog_a": "Tecnología"
        }
    )

    fig_barras_pospago.update_layout(
        title={
            "text": "Distribución de Abonados por Tecnología en Pospago",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        },
        barmode="stack",  # Barras apiladas
        height=600
    )
    st.plotly_chart(fig_barras_pospago)      # Mostrar gráfico 

    ##################### Gráfico de torta: Distribución de Abonados por Proveedor (Prepago) #####################
    # Crear gráfico de torta para Prepago
    fig_torta_prepago = px.pie(
        data_frame=prepago_data.groupby("proveedor", as_index=False).agg({"no_abonados": "sum"}),
        values="no_abonados",
        names="proveedor",
        labels={"no_abonados": "Número de Abonados", "proveedor": "Proveedor"}
    )

    fig_torta_prepago.update_traces(textinfo="percent+label")  # Mostrar porcentaje y nombre del proveedor
    fig_torta_prepago.update_layout(
        title={
            "text": "Distribución de Abonados por Proveedor (Prepago)",  # Título actualizado
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        }
    )

    st.plotly_chart(fig_torta_prepago)     # Mostrar gráfico

    ##################### Gráfico de torta: Distribución de Abonados por Proveedor (Pospago) #####################
    fig_torta_pospago = px.pie(
        data_frame=pospago_data.groupby("proveedor", as_index=False).agg({"no_abonados": "sum"}),
        values="no_abonados",
        names="proveedor",
        labels={"no_abonados": "Número de Abonados", "proveedor": "Proveedor"}
    )

    fig_torta_pospago.update_traces(textinfo="percent+label")  # Mostrar porcentaje y nombre del proveedor
    fig_torta_pospago.update_layout(
        title={
            "text": "Distribución de Abonados por Proveedor (Pospago)",  # Título actualizado
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        }
    )

    st.plotly_chart(fig_torta_pospago)     # Mostrar gráfico


    ##################### Tabla: Ranking de Proveedores por Cantidad de Abonados #####################
    ranking_data = data.groupby("proveedor")[["no_abonados"]].sum().reset_index()
    ranking_data = ranking_data.sort_values(by="no_abonados", ascending=False).reset_index(drop=True) # Ordenar los datos en orden descendente por la cantidad de abonados

    # Renombrar columnas para mejor visualización
    ranking_data.rename(columns={
        "proveedor": "Proveedor",
        "no_abonados": "# Total de Abonados"
    }, inplace=True)

    # Mostrar la tabla en Streamlit
    st.write("### Ranking de Proveedores por Cantidad de Abonados")
    st.table(ranking_data)

# Sección: Gráficas/Tablas Combinadas (Telefonía e Internet Móvil)
def combined_visualizations(telefonia_data, internet_data):
    """ Genera las gráficas y tablas combinadas utilizando datos de Telefonía e Internet Móvil. """
    st.write("## Análisis de datos de ambos segmentos, Telefonía e Internet Móvil")
    
    ##################### Evolución del Número de Abonados vs. Consumo de Voz #####################
    # Agrupaciones necesarias
    internet_grouped = internet_data.groupby("Periodo")[["no_abonados"]].sum().reset_index() # Agrupar datos de internet por periodo
    telefonia_grouped = telefonia_data.groupby("Periodo")[["consumo_prepago", "consumo_pospago"]].sum().reset_index() # Agrupar datos de telefonía por periodo
    telefonia_grouped["consumo_total"] = telefonia_grouped["consumo_prepago"] + telefonia_grouped["consumo_pospago"] # Combinar datos de consumo (prepago y pospago)
    combined_data = pd.merge(internet_grouped, telefonia_grouped[["Periodo", "consumo_total"]], on="Periodo", how="inner") # Fusionar ambas tablas por la columna 'Periodo'

    # Normalización de las columnas de abonados y consumo total
    combined_data["Cant_usuarios_Internet"] = combined_data["no_abonados"] / combined_data["no_abonados"].max()
    combined_data["Ingresos_Telefonia"] = combined_data["consumo_total"] / combined_data["consumo_total"].max()

    # Crear gráfico de líneas con dos ejes Y
    fig = px.line(
        combined_data,
        x="Periodo",
        y=["Cant_usuarios_Internet", "Ingresos_Telefonia"],
        labels={
            "value": "Valor Normalizado",
            "variable": "Métrica",
            "Periodo": "Periodo"
        }
    )

    # Actualizar el diseño del gráfico
    fig.update_layout(
        title={
            "text": "Evolución de los Servicios Móviles",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center"
        },
        yaxis_title="Valor Normalizado",
        legend_title="Métrica",
        height=600
    )

    st.plotly_chart(fig)     # Mostrar gráfico

    ##################### Ranking Combinado de Proveedores #####################
    # Calcular métricas combinadas
    telefonia_grouped = telefonia_data.groupby("proveedor").agg(
        {
            "consumo_prepago": "sum",
            "consumo_pospago": "sum",
            "ingresos_operacionales": "sum"
        }
    ).reset_index()

    internet_grouped = internet_data.groupby("proveedor").agg(
        {
            "no_abonados": "sum"
        }
    ).reset_index()

    # Fusionar métricas de telefonía e internet por proveedor
    combined_data = pd.merge(
        telefonia_grouped,
        internet_grouped,
        on="proveedor",
        how="outer"
    )

    combined_data.fillna(0, inplace=True) # Llenar valores faltantes con 0

    # Calcular puntuación combinada con pesos personalizados para cada métrica
    combined_data["puntuacion"] = (
        combined_data["consumo_prepago"] * 0.3 +
        combined_data["consumo_pospago"] * 0.3 +
        combined_data["ingresos_operacionales"] * 0.2 +
        combined_data["no_abonados"] * 0.2
    )

    combined_data = combined_data.sort_values(by="puntuacion", ascending=False)     # Ordenar por puntuación

    ###################### Ranking Combinado de Proveedoresl ##########################
    # Agrupación por tecnología
    internet_tech_grouped = internet_data.groupby(["proveedor", "tecnolog_a"]).agg(
        {"no_abonados": "sum"}
    ).reset_index()

    # Seleccionar tecnología predominante
    internet_tech_predominant = internet_tech_grouped.loc[ internet_tech_grouped.groupby("proveedor")["no_abonados"].idxmax()][["proveedor", "tecnolog_a"]]

    # Fusionar la tecnología predominante con el ranking combinado
    combined_data = pd.merge(
        combined_data,
        internet_tech_predominant,
        on="proveedor",
        how="left"
    )

    # Gráfico de barras horizontales para el ranking combinado
    fig_ranking = px.bar(
        combined_data,
        x="puntuacion",
        y="proveedor",
        color="tecnolog_a",
        orientation="h",
        labels={
            "puntuacion": "Puntuación Combinada",
            "proveedor": "Proveedor",
            "tecnolog_a": "Tecnología Predominante"
        },
        color_discrete_sequence=px.colors.qualitative.Plotly,
        height=800
    )

    fig_ranking.update_layout(
        title={
            "text": "Ranking Combinado de Proveedores",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="Puntuación Combinada",
        yaxis_title="Proveedor",
        legend_title="Tecnología Predominante",
    )

    st.plotly_chart(fig_ranking)     # Mostrar gráfico

    st.write(""" La puntuación fue calculada con la siguiente ponderación "consumo_prepago" * 0.3 + "consumo_pospago" * 0.3 + "ingresos_operacionales" * 0.2 + "no_abonados"] * 0.2 """)

    ##################### Relación entre Abonados de Internet y Consumo de Voz en Telefonía #####################
    internet_grouped = internet_data.groupby("Periodo")[["no_abonados"]].sum().reset_index() # Agrupar datos de internet por periodo
    telefonia_grouped = telefonia_data.groupby("Periodo")[["consumo_prepago", "consumo_pospago"]].sum().reset_index() # Agrupar datos de telefonía por periodo
    combined_data = pd.merge(internet_grouped, telefonia_grouped, on="Periodo", how="inner") # Fusionar ambas tablas por la columna 'Periodo'

    # Transformar datos al formato largo para segmentar prepago y pospago
    melted_data = pd.melt(
        combined_data,
        id_vars=["Periodo", "no_abonados"],
        value_vars=["consumo_prepago", "consumo_pospago"],
        var_name="Segmento",
        value_name="Consumo"
    )

    # Reemplazar valores para claridad en el eje Segmento
    melted_data["Segmento"] = melted_data["Segmento"].replace({
        "consumo_prepago": "Prepago",
        "consumo_pospago": "Pospago"
    })

    # Crear gráfico de dispersión
    fig_scatter = px.scatter(
        melted_data,
        x="no_abonados",
        y="Consumo",
        color="Segmento",
        size="Consumo",
        labels={
            "no_abonados": "Cantidad de usuarios de Internet Móvil",
            "Consumo": "Ingresos por Telefonía Móvil (MM)",
            "Segmento": "Segmento"
        },
        hover_data={"Periodo": True},
        title="Relación entre Abonados de Internet y Consumo de Voz en Telefonía"
    )

    fig_scatter.update_layout(
        title={
            "text": "Relación entre Abonados de Internet y Consumo de Voz en Telefonía",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="Cantidad de usuarios de Internet Móvil",
        yaxis_title="Ingresos de Telefonía Móvil ($)",
        height=600
    )

    st.plotly_chart(fig_scatter)     # Mostrar gráfico

    st.write(""" Permite identificar los periodos en que hubo más usuarios consumidores de telefonía e internet """)

    ##################### Clustering de Proveedores #####################
    # Combinar datos por proveedor
    combined_data = telefonia_data.groupby("proveedor")[["consumo_prepago", "consumo_pospago", "ingresos_operacionales"]].sum()
    internet_abonados = internet_data.groupby("proveedor")[["no_abonados"]].sum()
    clustering_data = combined_data.join(internet_abonados, how="inner").reset_index()

    # Estandarizar los datos
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data[["consumo_prepago", "consumo_pospago", "ingresos_operacionales", "no_abonados"]])

    # K-Means Clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clustering_data["Cluster"] = kmeans.fit_predict(scaled_data)

    # Visualización con PCA para reducción a 2D
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(scaled_data)
    clustering_data["PCA1"] = reduced_data[:, 0]
    clustering_data["PCA2"] = reduced_data[:, 1]

    # Gráfico interactivo
    fig_kmeans = px.scatter(
        clustering_data,
        x="PCA1",
        y="PCA2",
        color="Cluster",
        hover_data={"proveedor": True, "Cluster": True, "PCA1": False, "PCA2": False},
        labels={"Cluster": "Grupo", "PCA1": "Componente Principal 1", "PCA2": "Componente Principal 2"}
    )

    fig_kmeans.update_layout(
        title={
            "text": "Análisis de Segmentación (Clustering) de Proveedores usando K-Means",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="Cantidad de usuarios de Internet Móvil",
        yaxis_title="Ingresos de Telefonía Móvil ($)",
        height=600
    )

    st.plotly_chart(fig_kmeans)     # Mostrar gráfico
    st.write(""" Se muestran los proveedores agrupados según sus patrones de consumo e ingresos. Esto permite a identificar líderes (Grupo 2), medianos (Grupo 1) y proveedores de bajo rendimiento (Grupo 0).""")

# Función principal para ejecutar las visualizaciones
def main_visualizations():
    
    """ Función principal para gestionar las secciones de visualización. """
    
    st.sidebar.title("Secciones de Visualización")
    section = st.sidebar.selectbox("Selecciona la Sección", ["Telefonía", "Internet", "Internet vs Telefonía"])

    # Verificar si los datos están disponibles en la sesión
    telefonia_data = st.session_state.get("telefonia_data", None)
    internet_data = st.session_state.get("internet_data", None)

    # Seleccionar y mostrar la sección correspondiente
    if section == "Telefonía" and telefonia_data is not None:
        telefonia_visualizations(telefonia_data)
    elif section == "Internet" and internet_data is not None:
        internet_visualizations(internet_data)
    elif section == "Internet vs Telefonía" and telefonia_data is not None and internet_data is not None:
        combined_visualizations(telefonia_data, internet_data)
    else:
        st.warning("Elige una sección para comenzar...")
