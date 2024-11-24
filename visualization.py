import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def plot_consumption(data, selected_providers):
    """
    Genera gráficos del consumo de voz en prepago y pospago para los proveedores seleccionados.
    """
    # Filtrar datos por proveedores seleccionados
    data = data[data["proveedor"].isin(selected_providers)]

    # Gráfica del consumo de voz en prepago
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x="trimestre", y="consumo_prepago", hue="proveedor", ax=ax)
    ax.set_title("Consumo de Voz en Prepago")
    ax.set_ylabel("Consumo (Millones)")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Gráfica del consumo de voz en pospago
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x="trimestre", y="consumo_pospago", hue="proveedor", ax=ax)
    ax.set_title("Consumo de Voz en Pospago")
    ax.set_ylabel("Consumo (Millones)")
    plt.xticks(rotation=90)
    st.pyplot(fig)

def plot_income(data, selected_providers):
    """
    Genera un gráfico de los ingresos operacionales para los proveedores seleccionados.
    """
    # Filtrar datos por proveedores seleccionados
    data = data[data["proveedor"].isin(selected_providers)]

    # Gráfica de ingresos operacionales
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x="trimestre", y="ingresos_operacionales", hue="proveedor", ax=ax)
    ax.set_title("Ingresos Operacionales")
    ax.set_ylabel("Ingresos (Millones)")
    plt.xticks(rotation=90)
    st.pyplot(fig)

def plot_abonados(data, selected_providers):
    """
    Genera un gráfico del número de abonados por tecnología y segmento.
    """
    # Filtrar datos por proveedores seleccionados
    data = data[data["proveedor"].isin(selected_providers)]

    # Gráfica de abonados
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x="tecnolog_a", y="no_abonados", hue="segmento", ci=None, ax=ax)
    ax.set_title("Número de Abonados por Tecnología y Segmento")
    ax.set_ylabel("Número de Abonados")
    plt.xticks(rotation=90)
    st.pyplot(fig)

def plot_data_analysis(data):
    """
    Genera gráficos exploratorios para analizar los datos de ingresos.
    """
    # Boxplot: Comparación de ingresos entre proveedores y trimestres
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="proveedor", y="ingresos_operacionales", data=data, ax=ax)
    ax.set_title("Distribución de Ingresos por Proveedor")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Promedio móvil de ingresos operacionales
    data['promedio_movil_3'] = data['ingresos_operacionales'].rolling(window=3).mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=data, x="trimestre", y="promedio_movil_3", hue="proveedor", ax=ax)
    ax.set_title("Promedio Móvil de 3 Trimestres de Ingresos Operacionales")
    plt.xticks(rotation=90)
    st.pyplot(fig)

def plot_proportion(data):
    """
    Muestra la proporción de ingresos entre prepago y pospago.
    """
    if 'consumo_prepago' in data.columns and 'consumo_pospago' in data.columns:
        data['proporcion_prepago'] = data['consumo_prepago'] / (data['consumo_prepago'] + data['consumo_pospago'])
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="proveedor", y="proporcion_prepago", data=data, ax=ax)
        ax.set_title("Proporción de Consumo en Prepago")
        ax.set_ylabel("Proporción Prepago")
        plt.xticks(rotation=90)
        st.pyplot(fig)

def plot_internet(data, selected_providers):
    """
    Genera un gráfico del número de abonados por tecnología y segmento.
    """
    # Filtrar datos por proveedores seleccionados
    data = data[data["proveedor"].isin(selected_providers)]

    # Gráfica de abonados
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x="tecnolog_a", y="no_abonados", hue="segmento", ci=None, ax=ax)
    ax.set_title("Número de Abonados por Tecnología y Segmento")
    ax.set_ylabel("Número de Abonados")
    plt.xticks(rotation=90)
    st.pyplot(fig)
