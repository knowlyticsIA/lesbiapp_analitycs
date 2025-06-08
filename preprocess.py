import pandas as pd
import json
from utils import limpiar_y_procesar_datos 

def main():
    ruta_csv_crudo = "data/encuesta_mujeres.csv"
    
    ruta_df_limpio = "data/cleaned_data.parquet"
    ruta_conteo_vinculos = "data/conteo_vinculos.parquet"
    ruta_conteo_actividades = "data/conteo_actividades.parquet"
    ruta_conteo_bioseguridad = "data/conteo_bioseguridad.parquet"
    ruta_respuestas_otras = "data/otras_respuestas.json"

    try:
        df_raw = pd.read_csv(ruta_csv_crudo)
        print(f"✅ Archivo '{ruta_csv_crudo}' cargado correctamente.")
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo '{ruta_csv_crudo}'. Asegúrate de que el archivo exista en la carpeta 'data'.")
        return

    print("⏳ Procesando y limpiando los datos... (Esto puede tardar un momento)")
    (
        df_clean, 
        conteo_vinculos, 
        conteo_actividades, 
        conteo_bioseguridad, 
        otros_actividades, 
        otros_vinculos, 
        otros_bioseguridad
    ) = limpiar_y_procesar_datos(df_raw)
    print("✅ Datos procesados.")

    try:
        df_clean.to_parquet(ruta_df_limpio)
        print(f"   -> Guardado: '{ruta_df_limpio}'")
        
        conteo_vinculos.to_parquet(ruta_conteo_vinculos)
        print(f"   -> Guardado: '{ruta_conteo_vinculos}'")
        
        conteo_actividades.to_parquet(ruta_conteo_actividades)
        print(f"   -> Guardado: '{ruta_conteo_actividades}'")
        
        conteo_bioseguridad.to_parquet(ruta_conteo_bioseguridad)
        print(f"   -> Guardado: '{ruta_conteo_bioseguridad}'")

        otras_data = {
            'actividades': otros_actividades,
            'vinculos': otros_vinculos,
            'bioseguridad': otros_bioseguridad
        }
        with open(ruta_respuestas_otras, 'w', encoding='utf-8') as f:
            json.dump(otras_data, f, ensure_ascii=False, indent=4)
        print(f"   -> Guardado: '{ruta_respuestas_otras}'")
        
        print("\n🎉 ¡Procesamiento completado con éxito!")
        print("Ahora puedes ejecutar tu dashboard con 'streamlit run app.py'")

    except Exception as e:
        print(f"❌ ERROR: Ocurrió un error al guardar los archivos. {e}")


if __name__ == "__main__":
    main()