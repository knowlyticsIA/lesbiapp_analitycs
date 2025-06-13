import pandas as pd
import json
from utils import limpiar_y_procesar_datos

def cargar_datos_crudos(ruta):
    """Carga el archivo CSV inicial."""
    print(f"🔄 Cargando datos desde '{ruta}'...")
    try:
        df = pd.read_csv(ruta)
        print("✅ Archivo cargado correctamente.")
        return df
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo '{ruta}'.")
        return None

def guardar_artefactos(datos, rutas):
    """Guarda todos los dataframes y archivos procesados."""
    print("💾 Guardando archivos procesados...")
    try:
        datos["df_clean"].to_parquet(rutas["df_limpio"])
        datos["df_segmentado_edad"].to_parquet(rutas["segmento_edad"])
        
        datos["conteo_actividades_ind"].to_parquet(rutas["conteo_act_ind"])
        datos["conteo_vinculos_ind"].to_parquet(rutas["conteo_vinc_ind"])
        datos["conteo_bioseguridad"].to_parquet(rutas["conteo_bioseguridad"])

        print("✅ Archivos .parquet guardados.")
        print("\n🎉 ¡Procesamiento completado con éxito!")
    except Exception as e:
        print(f"❌ ERROR: Ocurrió un error al guardar los archivos. {e}")

def main():
    RUTAS = {
        "csv_crudo": "data/encuesta_mujeres.csv",
        "df_limpio": "data/cleaned_data.parquet",
        "segmento_edad": "data/segmento_20_50_data.parquet",
        "conteo_act_ind": "data/conteo_actividades_individuales.parquet",
        "conteo_vinc_ind": "data/conteo_vinculos_individuales.parquet",
        "conteo_bioseguridad": "data/conteo_bioseguridad.parquet"
    }
    df_raw = cargar_datos_crudos(RUTAS["csv_crudo"])
    if df_raw is None: return

    datos_procesados = limpiar_y_procesar_datos(df_raw)
    print("✅ Datos procesados.")

    print("🔪 Creando segmento por edad (20-50 años)...")
    grupos_etarios_target = ['21-30', '31-40', '41-50']
    df_segmentado = datos_procesados["df_clean"][
        datos_procesados["df_clean"]['Grupo Etareo'].isin(grupos_etarios_target)
    ].copy()
    datos_procesados["df_segmentado_edad"] = df_segmentado
    print(f"✅ Segmento creado con {len(df_segmentado)} filas.")

    guardar_artefactos(datos_procesados, RUTAS)
    print("\nAhora puedes ejecutar tu dashboard con 'streamlit run app.py'")

if __name__ == "__main__":
    main()