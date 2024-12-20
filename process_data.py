import pandas as pd
from fetch_data import fetch_data

def process_data(data, table):
    """
    Preprocesa los datos de Telefonía Móvil para análisis:
    - Limpia y convierte columnas de consumo a valores numéricos.
    - Calcula la columna 'Periodo' como fecha de inicio del trimestre.
    - Elimina filas donde ambos consumos son cero.
    - Ordena los datos por 'Periodo'.

    Args:
        data (pd.DataFrame): Datos originales de Telefonía Móvil.

    Returns:
        pd.DataFrame: Datos preprocesados.
    """
    # Crear una copia del DataFrame original
    data = data.copy()

    if table == "telefonia_movil":
        # # Procesar datos de Telefonía Móvil
        numeric_columns = ["consumo_prepago", "consumo_pospago", "ingresos_operacionales"]
        for col in numeric_columns:
            if col in data.columns:
                # Procesar valores paso a paso para evitar errores
                data[col] = data[col].astype(str)  # Convertir a string

                data[col] = (
                    data[col]
                    .str.replace('"', '', regex=False)           # Eliminar comillas dobles si existen
                    .str.replace(r"\.", "", regex=True)          # Eliminar puntos como separadores de miles
                    .str.replace(",", ".", regex=False)          # Reemplazar coma decimal por punto
                )
                # Convertir finalmente a float
                data[col] = data[col].astype(float)
    
    elif table == "internet_movil":

        # Procesar datos de Internet Móvil
        data["no_abonados"] = pd.to_numeric(data["no_abonados"], errors="coerce")

    # Convertir Año y Trimestre a strings para concatenar
    data["a_o"] = data["a_o"].astype(str)
    data["trimestre"] = data["trimestre"].astype(str)

    # Crear una lista de los primeros días de cada trimestre
    primeros_dias_trimestre = ["01-01", "04-01", "07-01", "10-01"]

    # Mapear el trimestre a su correspondiente primer día
    data["Periodo"] = data.apply(
        lambda row: pd.to_datetime(
            row["a_o"] + "-" + primeros_dias_trimestre[int(row["trimestre"]) - 1]
        ),
        axis=1,
    )
    # Ordenar datos por la columna 'Periodo'
    data = data.sort_values(by="Periodo").reset_index(drop=True)

    # Añadir el nombre comercial de algunas empresas
    data["proveedor"] = data["proveedor"].replace(
        {"COLOMBIA TELECOMUNICACIONES S.A. E.S.P.": "MOVISTAR (COLOMBIA TELECOMUNICACIONES S.A. E.S.P.)"}
    )

    data["proveedor"] = data["proveedor"].replace(
        {"COLOMBIA MOVIL  S.A ESP": "TIGO (COLOMBIA MOVIL S.A ESP)"}
    )

    data["proveedor"] = data["proveedor"].replace(
        {"COMUNICACION CELULAR S A COMCEL S A": "CLARO (COMUNICACION CELULAR S A COMCEL S A)"}
    )

    data["proveedor"] = data["proveedor"].replace(
        {"PARTNERS TELECOM COLOMBIA SAS": "WOM (PARTNERS TELECOM COLOMBIA SAS)"}
    )

    data["proveedor"] = data["proveedor"].replace(
        {"EMPRESA DE TELECOMUNICACIONES DE BOGOTA S.A. ESP": "ETB (EMPRESA DE TELECOMUNICACIONES DE BOGOTA S.A. ESP)"}
    )

    # Eliminar filas con valores faltantes o inválidos
    data.dropna(inplace=True)
    return data

################################### Ejemplo de uso SIN traer datos de la API ###################################
# if __name__ == "__main__":
#     # Datos de ejemplo (Telefonía Móvil)
#     data_telefonia = pd.DataFrame({
#         "a_o": [2022, 2022],
#         "trimestre": [3, 3],
#         "proveedor": ["COMCEL", "TIGO"],
#         "consumo_prepago": ["1000,00", "2000,00"],
#         "consumo_pospago": ["3000,00", "4000,00"],
#         "ingresos_operacionales": ["5000,00", "6000,00"]
#     })
#     print("Datos procesados - Telefonía Móvil:")
#     print(process_data(data_telefonia, "telefonia_movil"))

#     # Datos de ejemplo (Internet Móvil)
#     data_internet = pd.DataFrame({
#         "a_o": [2022, 2022],
#         "trimestre": [1, 1],
#         "proveedor": ["COMCEL", "TIGO"],
#         "segmento": ["PREPAGO", "POSPAGO"],
#         "terminal": ["4G", "3G"],
#         "tecnolog_a": ["4G", "3G"],
#         "no_abonados": ["100", "200"]
#     })
#     print("\nDatos procesados - Internet Móvil:")
#     print(process_data(data_internet, "internet_movil"))

################################### Ejemplo de uso CON datos via API ###################################
# if __name__ == "__main__":
#     print("Obteniendo y procesando datos de Telefonía Móvil...")
#     filters_telefonia = {"a_o": "2022", "trimestre": "3"}
#     data_telefonia = fetch_data("telefonia_movil", filters=filters_telefonia, limit=10)
#     processed_telefonia = process_data(data_telefonia, "telefonia_movil")
#     print("Datos procesados - Telefonía Móvil:")
#     print(processed_telefonia)

#     # Ejemplo 2: Datos de Internet Móvil (Proveedor específico)
#     print("\nObteniendo y procesando datos de Internet Móvil...")
#     filters_internet = {"proveedor": "COMUNICACION CELULAR S A COMCEL S A", "trimestre": "1"}
#     data_internet = fetch_data("internet_movil", filters=filters_internet, limit=10)
#     processed_internet = process_data(data_internet, "internet_movil")
#     print("Datos procesados - Internet Móvil:")
#     print(processed_internet)