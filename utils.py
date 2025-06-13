import pandas as pd
from thefuzz import process


COLUMNAS_RENOMBRADAS = {
    '¿Cómo te identificas en relación con el genero femenino?  ': "Identidad genero",
    '¿Con cuál de las siguientes identidades te sentís más identificada?': "Identidad sexual",
    '¿Dónde vivís actualmente?': "Lugar residencia",
    '¿Cuál es tu nivel educativo alcanzado?': 'Nivel educativo',
    '¿Con quien vivís?': "Convivencia",
    ' ¿Qué edad tenés? ': "edad",
    '¿Qué tipo de vínculos estás buscando actualmente con otras mujeres?': "Vinculos buscados",
    '*PARA QUIENES SE CONSIDERAN LESBIANAS O BISEXUALES:\r\n¿Qué tan fácil te resulta conocer a otras mujeres lesbianas o bisexuales en tu zona?': "Facilidad conocer LesBi",
    '*PARA QUIENES SE CONSIDERAN HETEROSEXUALES\r\n¿Qué tan fácil te resulta conocer a otras mujeres para entablar nuevas amistades?': "Facilidad conocer hetero",
    '¿Usaste alguna vez apps tipo Tinder, Ok Cupid, Happn o redes sociales para conocer a otras mujeres? ': "Apps citas",
    '¿Qué sentís que te falta hoy en cuanto a vínculos con otras mujeres?': "Vinculos faltantes",
    '¿Cómo te sentirías usando una aplicación pensada exclusivamente para fomentar vínculos entre mujeres que no se centre en lo amoroso?': "Opinion apps no amorosas",
    '¿Qué tipo de actividades o espacios te gustaría que promueva una app de este tipo?': "Actividades preferidas",
    'Siempre nos cuidamos entre nosotras, y pensando en eso quisiera saber: ¿Qué medidas de bioseguridad te gastaría que tenga una aplicación de este estilo? ': "Medidas bioseguridad",
    '¿Te gustaría recibir novedades del avance del proyecto?': "Recibir novedades"
}

MAP_GENERO = {"Mujer cis (me asignaron el género femenino al nacer y me identifico como mujer)": "Mujer cis", 
              "Mujer trans (me asignaron otro género al nacer y me identifico como mujer)": "Mujer trans", 
              "Persona no binaria con experiencia femenina": "No binaria fem"}
MAP_IDENTIDAD_SEXUAL = {"Lesbiana": "Lesbiana", "Bisexual": "Bisexual", "Pansexual": "Pansexual", "Heterosexual": "Heterosexual"}
MAP_RESIDENCIA = {"Ciudad Autónoma de Buenos Aires (CABA)": "CABA", "Gran Buenos Aires (GBA) - Zona Norte (ej. Vicente López, San Isidro, Tigre, San Fernando, Pilar, Escobar, etc.)": "PBA Norte", "Gran Buenos Aires (GBA) - Zona Oeste (ej. Morón, La Matanza, Tres de Febrero, Ituzaingó, Hurlingham, Merlo, Moreno, etc.)": "PBA Oeste", "Gran Buenos Aires (GBA) - Zona Sur (ej. Avellaneda, Lanús, Lomas de Zamora, Quilmes, Almirante Brown, Esteban Echeverría, Ezeiza, Berazategui, Florencio Varela, etc.)": "PBA Sur", "AMBA, La Plata y alrededores (con fácil acceso a CABA)": "La Plata"}
MAP_APPS_CITAS = {"Si, use para hacer amigas nuevas": "Sí, Amistades", 
                  "Si, use para conocer a otras mujeres de forma romantica y/o sexual": "Sí, pareja", 
                  "Si usé, pero solo chatie con chicas y nunca superó la fase virtual": "Solo vínculo virtual", 
                  "Nunca use apps de ese estilo para conocer a otras mujeres, pero me interesaria": "No, pero quiero", 
                  "No, y no me interesa": "No"}

MAPEO_ACTIVIDADES_AGRUPADAS = {
    'Encuentros diurnos': ['Encuentros o salidas grupales durante el día en mi zona (ej: picnics, paseos culturales, ferias)'], 
    'Encuentros nocturnos': ['Encuentros o salidas grupales durante la noche en mi zona  (ej: bares tranquilos, eventos culturales, cenas)'], 
    'Deporte': ['Grupos para organizar actividades deportivas o recreativas'], 
    'Fiestas': ['Fiestas de mujeres'], 
    'Charlas': ['Charlas virtuales o presenciales'], 
    'Foros temáticos': ['Foros o grupos temáticos (ej: literatura, cine, deportes, maternidad, emprendimiento, bienestar, etc.)'], 
    'Cultura': ['Espacios para compartir arte o escritura'], 
    'Activismo': ['Conocer mujeres militantes o activistas con las cuales vincularte']
}
MAPEO_VINCULOS_AGRUPADOS = {
    'Vínculos de Amistad solo LBT+': ['Amistades solo con mujeres que formen parte del colectivo LBT+ (excluyente)'], 
    'Vínculos de Amistad solo hetero': ['Amistades solo con mujeres heterosexuales'], 
    'Vínculos de Amistad indistinto': ['Amistades con mujeres que esten dentro o fuera del colectivo LBT+ (no me interesa su identidad particularmente para comenzar una nueva amistad con alguien)'], 
    'Vínculos Sexo-Afectivos': ['Pareja o vínculo romántico/sexoafectivo','Sexo ocasional'], # Este ya estaba bien
    'Redes de apoyo': ['Redes de apoyo emocional o afectivos'], 
    'Participación Social': ['Participar en actividades o encuentros sociales/culturales/recreativos']
}
MAP_IDENTIDAD = {
    "Lesbiana": "Lesbiana", "Bisexual": "Bisexual",
    "Pansexual": "Pansexual", "Heterosexual": "Heterosexual"
}
orden_facilidad = ['Muy fácil', 'Algo fácil', 'Difícil', 'Muy dificil', 'Imposible', 'Nunca lo intenté']
MAPEO_FACILIDAD_NUM = {
    'Muy fácil': 5,
    'Algo fácil': 4,
    'Difícil': 3,
    'Muy dificil': 2,  
    'Imposible': 1,
    'Nunca lo intenté': 0 
}



def _agrupar_respuestas_multiples(respuestas_str, mapeo):
    if pd.isna(respuestas_str): return None
    respuestas_individuales = [r.strip() for r in respuestas_str.split(',')]
    grupos_encontrados = set()
    for resp in respuestas_individuales:
        for grupo, lista_respuestas in mapeo.items():
            if resp in lista_respuestas:
                grupos_encontrados.add(grupo)
                break
    return ', '.join(sorted(list(grupos_encontrados)))

def _contar_combinaciones(series, top_n=15):
    conteo = series.dropna().value_counts().nlargest(top_n)
    df_conteo = conteo.reset_index()
    df_conteo.columns = ['opcion', 'cantidad']
    return df_conteo

def _contar_respuestas_individuales(series, umbral_otras=1):
    """
    Toma una serie con respuestas múltiples, las separa, cuenta cada una,
    y agrupa las menos frecuentes en una categoría "Otras".
    """
    respuestas_explotadas = series.dropna().str.split(r'\s*,\s*').explode().str.strip()
    conteo = respuestas_explotadas.value_counts()
    
    total_otras = conteo[conteo <= umbral_otras].sum()
    conteo_principal = conteo[conteo > umbral_otras]
    
    if total_otras > 0:
        conteo_principal['Otras respuestas minoritarias'] = total_otras
        
    df_conteo = conteo_principal.reset_index()
    df_conteo.columns = ['opcion', 'cantidad']
    return df_conteo

def limpiar_y_procesar_datos(df):
    df = df.rename(columns=COLUMNAS_RENOMBRADAS)

    bins = [0, 20, 30, 40, 50, 100]
    labels = ['<20', '21-30', '31-40', '41-50', '50+']
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    df['Grupo Etareo'] = pd.cut(df['edad'], bins=bins, labels=labels, right=True)

    df["Identidad genero"] = df["Identidad genero"].map(MAP_GENERO).fillna("Otra")
    df["Identidad sexual"] = df["Identidad sexual"].map(MAP_IDENTIDAD).fillna("Otra")
    df["Lugar residencia"] = df["Lugar residencia"].map(MAP_RESIDENCIA).fillna("Otro")
    df["Apps citas"] = df["Apps citas"].map(MAP_APPS_CITAS).fillna("Otra")

    for col in ['Facilidad conocer LesBi', 'Facilidad conocer hetero']:
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=orden_facilidad, ordered=True)

    df['Facilidad LesBi Num'] = df['Facilidad conocer LesBi'].map(MAPEO_FACILIDAD_NUM)
    df['Facilidad Hetero Num'] = df['Facilidad conocer hetero'].map(MAPEO_FACILIDAD_NUM)
    
    # Crear columnas agrupadas
    df['Actividades Agrupadas'] = df['Actividades preferidas'].apply(_agrupar_respuestas_multiples, mapeo=MAPEO_ACTIVIDADES_AGRUPADAS)
    df['Vinculos Agrupados'] = df['Vinculos buscados'].apply(_agrupar_respuestas_multiples, mapeo=MAPEO_VINCULOS_AGRUPADOS)

    conteo_actividades_combinaciones = _contar_combinaciones(df['Actividades Agrupadas'])
    conteo_vinculos_combinaciones = _contar_combinaciones(df['Vinculos Agrupados'])

    conteo_actividades_individuales = _contar_respuestas_individuales(df['Actividades preferidas'])
    conteo_vinculos_individuales = _contar_respuestas_individuales(df['Vinculos buscados'])
    
    conteo_bioseguridad = _contar_respuestas_individuales(df['Medidas bioseguridad'])

    columnas_a_quitar = ['edad', 'Marca temporal', 'Dirección de correo electrónico']
    df_clean = df.drop(columns=[col for col in columnas_a_quitar if col in df.columns])

    return {
        "df_clean": df_clean,
        "conteo_vinculos_comb": conteo_vinculos_combinaciones,
        "conteo_actividades_comb": conteo_actividades_combinaciones,
        "conteo_vinculos_ind": conteo_vinculos_individuales,
        "conteo_actividades_ind": conteo_actividades_individuales,
        "conteo_bioseguridad": conteo_bioseguridad,
    }