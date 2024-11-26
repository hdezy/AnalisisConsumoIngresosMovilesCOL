import pandas as pd
from fetch_data import fetch_data

def process_data(data, table):
    """
    Procesa los datos obtenidos desde la API según la tabla seleccionada.

    Args:
        data (pd.DataFrame): Datos obtenidos desde la API.
        table (str): Tabla seleccionada ('telefonia_movil' o 'internet_movil').

    Returns:
        pd.DataFrame: Datos procesados.
    """
    if table == "telefonia_movil":
        # # Procesar datos de Telefonía Móvil
        # data["consumo_prepago"] = pd.to_numeric(
        #     data["consumo_prepago"].astype(str).str.replace(",", ""),
        #     errors="coerce"
        # ) / 1_000_000

        # data["consumo_pospago"] = pd.to_numeric(
        #     data["consumo_pospago"].astype(str).str.replace(",", ""),
        #     errors="coerce"
        # ) / 1_000_000

        # data["ingresos_operacionales"] = pd.to_numeric(
        #     data["ingresos_operacionales"].astype(str).str.replace(",", ""),
        #     errors="coerce"
        # ) / 1_000_000
        
        numeric_columns = ["consumo_prepago", "consumo_pospago", "ingresos_operacionales"]
        for col in numeric_columns:
            if col in data.columns:
                # Procesar valores paso a paso para evitar errores
                data[col] = data[col].astype(str)  # Convertir a string
                print(f"Valores originales en {col}:\n", data[col].head(10))  # Verificar valores iniciales

                data[col] = (
                    data[col]
                    .str.replace('"', '', regex=False)           # Eliminar comillas dobles si existen
                    .str.replace(r"\.", "", regex=True)          # Eliminar puntos como separadores de miles
                    .str.replace(",", ".", regex=False)          # Reemplazar coma decimal por punto
                )
                print(f"Valores limpiados como texto {col}:\n", data[col].head(10))  # Verificar limpieza

                # Convertir finalmente a float
                data[col] = data[col].astype(float)
                print(f"Valores convertidos en número {col}:\n", data[col].head(10))  # Verificar valores finales

    elif table == "internet_movil":
            # Procesar datos de Internet Móvil
        data["no_abonados"] = pd.to_numeric(data["no_abonados"], errors="coerce")

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