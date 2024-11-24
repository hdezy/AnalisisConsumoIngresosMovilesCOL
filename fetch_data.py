import pandas as pd
from sodapy import Socrata

# App Token para la API
APP_TOKEN = "czv2Rg4vWxlK0uOxX50rOb4z6"  # Reemplázalo con tu token real

# IDs de las tablas en la API
TABLES = {
    "internet_movil": "ezyw-egbj",  # Reemplaza con el ID real
    "telefonia_movil": "67wf-gj42",  # ID proporcionado en tu ejemplo
}

# def fetch_data(table, filters=None, limit=1000):
#     """
#     Conecta a la API y obtiene datos según filtros dinámicos.

#     Args:
#         table (str): Tabla a consultar ('internet_movil' o 'telefonia_movil').
#         filters (dict): Diccionario de filtros (e.g., {"a_o": "2022", "trimestre": "3"}).
#         limit (int): Límite de registros a traer.

#     Returns:
#         pd.DataFrame: Datos obtenidos como DataFrame.
#     """
#     # Validar si la tabla es válida
#     if table not in TABLES:
#         raise ValueError(f"Tabla '{table}' no es válida. Opciones: {list(TABLES.keys())}")
    
#     # Construir la consulta de filtros
#     query = None
#     if filters:
#         query = " AND ".join([f"{key}='{value}'" for key, value in filters.items()])

#     # Conectar con la API y traer los datos
#     client = Socrata("www.datos.gov.co", APP_TOKEN)
#     results = client.get(TABLES[table], where=query, limit=limit)

#     # Convertir a DataFrame
#     return pd.DataFrame.from_records(results)

def fetch_data(table, filters=None, limit=1000):
    """
    Conecta a la API y obtiene datos según filtros dinámicos.

    Args:
        table (str): Tabla a consultar ('internet_movil' o 'telefonia_movil').
        filters (dict): Diccionario de filtros (e.g., {"a_o": "2022", "trimestre": "3"}).
        limit (int): Límite de registros a traer.

    Returns:
        pd.DataFrame: Datos obtenidos como DataFrame.
    """
    if table not in TABLES:
        raise ValueError(f"Tabla '{table}' no es válida. Opciones: {list(TABLES.keys())}")

    # Construir la cláusula WHERE
    query = None
    if filters:
        clauses = []
        for key, value in filters.items():
            if "IN (" in value:  # Detecta si el filtro usa IN
                clauses.append(f"{key} {value}")
            else:
                clauses.append(f"{key}='{value}'")
        query = " AND ".join(clauses)

    # Conectar con la API
    client = Socrata("www.datos.gov.co", APP_TOKEN)
    results = client.get(TABLES[table], where=query, limit=limit)
    return pd.DataFrame.from_records(results)



# Ejemplos de uso

## Obtener datos de Telefonía Móvil para el año 2022 y trimestre 3
# filters = {"a_o": "2022", "trimestre": "3"}
# data = fetch_data("telefonia_movil", filters=filters, limit=10)
# print("Datos de telefonía filtrados por año y trimestre:")
# print(data.head())

## Obtener datos de Telefonía Móvil para el año 2022 y trimestre 3
# filters = {
#     "proveedor": "COMUNICACION CELULAR S A COMCEL S A",
#     "a_o": "2022"
# }
# data = fetch_data("internet_movil", filters=filters, limit=10)
# print("Datos filtrados por proveedor y año:")
# print(data)


############################### Obtener Proveedores #################################

def fetch_providers(table):
    """
    Obtiene la lista única de proveedores disponibles desde la API.

    Args:
        table (str): Tabla a consultar ('internet_movil' o 'telefonia_movil').

    Returns:
        list: Lista de proveedores únicos.
    """
    # Validar si la tabla es válida
    if table not in TABLES:
        raise ValueError(f"Tabla '{table}' no es válida. Opciones: {list(TABLES.keys())}")

    # Consulta para traer sólo los proveedores únicos
    client = Socrata("www.datos.gov.co", APP_TOKEN)
    results = client.get(TABLES[table], select="DISTINCT proveedor", limit=1000)

    # Convertir resultados a DataFrame y retornar la lista de proveedores
    providers_df = pd.DataFrame.from_records(results)
    return providers_df["proveedor"].tolist()

# Ejemplos de uso
# providers = fetch_providers("telefonia_movil")
# print("Proveedores disponibles - Telefonía Móvil:")
# print(providers)

# providers = fetch_providers("internet_movil")
# print("Proveedores disponibles - Internet Móvil:")
# print(providers)

############################### Obtener lista de años con datos disponibles #################################

def fetch_years(table):
    """
    Obtiene la lista única de años disponibles desde la API.

    Args:
        table (str): Tabla a consultar ('internet_movil' o 'telefonia_movil').

    Returns:
        list: Lista de años únicos.
    """
    # Validar si la tabla es válida
    if table not in TABLES:
        raise ValueError(f"Tabla '{table}' no es válida. Opciones: {list(TABLES.keys())}")

    # Consulta para traer sólo los años únicos
    client = Socrata("www.datos.gov.co", APP_TOKEN)
    results = client.get(TABLES[table], select="DISTINCT a_o", limit=1000)

    # Convertir resultados a DataFrame y retornar la lista de años
    years_df = pd.DataFrame.from_records(results)
    return sorted(years_df["a_o"].astype(int).tolist())  # Convertir a enteros y ordenar
