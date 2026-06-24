"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
from pathlib import Path
import re

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    for col in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']:
        df[col] = df[col].str.strip().str.lower()
        # NUEVO: unificar _ y - como espacio, y colapsar espacios múltiples
        df[col] = (
            df[col]
            .str.replace(r'[_\-]+', ' ', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )

    # 2. Limpiar monto_del_credito (quitar $, comas, convertir a float)
    df['monto_del_credito'] = (
        df['monto_del_credito'].astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .str.strip()
        .astype(float)
        )

    # 3. Estandarizar fecha_de_beneficio (detecta el formato y normaliza)
    def parse_fecha(f):
        f = f.strip()
        if re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', f):
            return pd.to_datetime(f, format='%Y/%m/%d', errors='coerce')
        return pd.to_datetime(f, format='%d/%m/%Y', errors='coerce')

    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(parse_fecha)

    # 4. Marcar valores inválidos como faltantes
    df.loc[df['estrato'] == 0, 'estrato'] = pd.NA
    df.loc[df['comuna_ciudadano'] > 16, 'comuna_ciudadano'] = pd.NA

    # 5. Ahora sí, tratar nulos
    df = df.dropna(subset=['tipo_de_emprendimiento', 'barrio'])
    # (o imputar con "no especificado" en vez de eliminar)

    # 6. Eliminar duplicados (ya con datos normalizados)
    df = df.drop_duplicates(keep='first')
    
    ruta_output = Path("files/output")
    ruta_output.mkdir(parents=True, exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";")

    print(df.comuna_ciudadano.value_counts().to_list())

    return

pregunta_01()