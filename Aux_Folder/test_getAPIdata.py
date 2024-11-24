import pandas as pd
from sodapy import Socrata

APP_TOKEN = "czv2Rg4vWxlK0uOxX50rOb4z6"
client = Socrata("www.datos.gov.co", APP_TOKEN)

# Datos: Telefonía Móvil trafico de voz por proveedor
results = client.get("67wf-gj42", where="trimestre='3' AND a_o='2022'", limit=10)
results_df = pd.DataFrame.from_records(results)
print(results_df.head())


# Datos: Internet Móvil, abonados por proveedor
results = client.get("ezyw-egbj", where="trimestre='3' AND a_o='2022'", limit=10)

results_df = pd.DataFrame.from_records(results)
print(results_df.head())