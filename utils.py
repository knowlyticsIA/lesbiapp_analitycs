import pandas as pd
from thefuzz import process

COLUMNAS_RENOMBRADAS = {
    '¿Cómo te identificas en relación con el genero femenino?  ': "Identidad genero",
    '¿Con cuál de las siguientes identidades te sentís más identificada?': "Identidad personal",
    '¿Dónde vivís actualmente?': "Lugar residencia",
    '¿Cuál es tu Nivel educativo alcanzado?': "Nivel educativo",
    '¿Con quien vivís?': "Convivencia",
    ' ¿Qué edad tenés? ': "edad",
    '¿Qué tipo de vínculos estás buscando actualmente con otras mujeres?': "Vinculos buscados",
    '*PARA QUIENES SE CONSIDERAN LESBIANAS O BISEXUALES:\n¿Qué tan fácil te resulta conocer a otras mujeres lesbianas o bisexuales en tu zona?': "Facilidad conocer LesBi",
    '*PARA QUIENES SE CONSIDERAN HETEROSEXUALES\n¿Qué tan fácil te resulta conocer a otras mujeres para entablar nuevas amistades?': "Facilidad conocer hetero",
    '¿Usaste alguna vez apps tipo Tinder, Ok Cupid, Happn o redes sociales para conocer a otras mujeres? ': "Apps citas",
    '¿Qué sentís que te falta hoy en cuanto a vínculos con otras mujeres?': "Vinculos faltantes",
    '¿Cómo te sentirías usando una aplicación pensada exclusivamente para fomentar vínculos entre mujeres que no se centre en lo amoroso?': "Opinion apps no amorosas",
    '¿Qué tipo de actividades o espacios te gustaría que promueva una app de este tipo?': "Actividades preferidas",
    'Siempre nos cuidamos entre nosotras, y pensando en eso quisiera saber: ¿Qué medidas de bioseguridad te gastaría que tenga una aplicación de este estilo? ': "Medidas bioseguridad",
    '¿Te gustaría recibir novedades del avance del proyecto?': "Recibir novedades"
}

MAP_GENERO = {
    "Mujer cis (me asignaron el género femenino al nacer y me identifico como mujer)": "Mujer cis",
    "Mujer trans (me asignaron otro género al nacer y me identifico como mujer)": "Mujer trans",
    "Persona no binaria con experiencia femenina": "No binaria fem"
}

MAP_IDENTIDAD = {
    "Lesbiana": "Lesbiana", "Bisexual": "Bisexual",
    "Pansexual": "Pansexual", "Heterosexual": "Heterosexual"
}

MAP_RESIDENCIA = {
    "Ciudad Autónoma de Buenos Aires (CABA)": "CABA",
    "Gran Buenos Aires (GBA) - Zona Norte (ej. Vicente López, San Isidro, Tigre, San Fernando, Pilar, Escobar, etc.)": "PBA Norte",
    "Gran Buenos Aires (GBA) - Zona Oeste (ej. Morón, La Matanza, Tres de Febrero, Ituzaingó, Hurlingham, Merlo, Moreno, etc.)": "PBA Oeste",
    "Gran Buenos Aires (GBA) - Zona Sur (ej. Avellaneda, Lanús, Lomas de Zamora, Quilmes, Almirante Brown, Esteban Echeverría, Ezeiza, Berazategui, Florencio Varela, etc.)": "PBA Sur",
    "AMBA, La Plata y alrededores (con fácil acceso a CABA)": "La Plata"
}

MAP_APPS_CITAS = {
    "Si, use para hacer amigas nuevas": "Sí, Amistades",
    "Si, use para conocer a otras mujeres de forma romantica y/o sexual": "Sí, pareja",
    "Si usé, pero solo chatie con chicas y nunca superó la fase virtual": "Solo vínculo virtual",
    "Nunca use apps de ese estilo para conocer a otras mujeres, pero me interesaria": "No, pero quiero",
    "No, y no me interesa": "No"
}

# --- DICCIONARIOS DE OPCIONES PARA PREGUNTAS MÚLTIPLES ---
VINCULOS_OPCIONES = [
    "Amistades con mujeres que estén dentro o fuera del colectivo LBT+",
    "Amistades solo con mujeres que formen parte del colectivo LBT+",
    "Amistades solo con mujeres heterosexuales",
    "Redes de apoyo emocional o afectivos",
    "Pareja o vínculo romántico/sexoafectivo",
    "Participar en actividades o encuentros sociales/culturales/recreativos",
    "Sexo ocasional"
]

ACTIVIDADES_OPCIONES = [
    "Charlas virtuales o presenciales", "Foros o grupos temáticos",
    "Encuentros o salidas grupales durante el día en mi zona",
    "Encuentros o salidas grupales durante la noche en mi zona",
    "Actividades de militancia o activismo", "Espacios para compartir arte o escritura",
    "Grupos para organizar actividades deportivas o recreativas", "Fiestas de mujeres"
]

BIOSEGURIDAD_OPCIONES = [
    "Verificación de identidad (por foto o redes sociales vinculadas)",
    "Posibilidad de denunciar y bloquear usuarias fácilmente",
    "Chat seguro con opción de reportar mensajes",
    "Función para compartir ubicación con una persona de confianza al tener un encuentro",
    "Posibilidad de puntuar un evento o anfitriona, una vez finalizado el mismo"
]

# --- FUNCIONES AUXILIARES DE LIMPIEZA ---

def _corregir_respuesta_otra(respuesta, opciones_validas, umbral=80):
    """
    Usa fuzzy matching para encontrar la mejor coincidencia para una respuesta de texto libre.
    
    Args:
        respuesta (str): El texto de la respuesta "otra".
        opciones_validas (list): Lista de opciones canónicas.
        umbral (int): Puntuación de similitud (0-100) para considerar una coincidencia.

    Returns:
        str: La opción válida si se encuentra una buena coincidencia, de lo contrario la respuesta original.
    """
    if not respuesta or pd.isna(respuesta):
        return None
    
    # process.extractOne devuelve (opción, puntaje). Nos quedamos con el mejor.
    mejor_match = process.extractOne(respuesta.lower(), [opt.lower() for opt in opciones_validas])
    
    if mejor_match and mejor_match[1] >= umbral:
        # Devolvemos la opción canónica original (con mayúsculas/minúsculas correctas)
        index = [opt.lower() for opt in opciones_validas].index(mejor_match[0])
        return opciones_validas[index]
    return respuesta # Si no hay buen match, devolvemos el texto original

def _procesar_respuestas_multiples(series, opciones_validas):
    """
    Limpia y cuenta las respuestas de una columna de selección múltiple.
    Corrige respuestas "otras" usando fuzzy matching.
    
    Args:
        series (pd.Series): La columna del DataFrame con las respuestas.
        opciones_validas (list): Lista de las opciones de respuesta predefinidas.

    Returns:
        tuple: Un DataFrame con el conteo de cada opción y una lista de respuestas no coincidentes.
    """
    conteo = {opcion: 0 for opcion in opciones_validas}
    respuestas_no_matcheadas = []
    
    # Nos aseguramos de trabajar con strings y eliminamos nulos
    series = series.dropna().astype(str)

    for respuesta_completa in series:
        # Separamos las distintas opciones elegidas por el usuario
        respuestas_individuales = [r.strip() for r in respuesta_completa.split(',')]
        
        for resp in respuestas_individuales:
            # Intentamos corregir la respuesta comparándola con las opciones válidas
            resp_corregida = _corregir_respuesta_otra(resp, opciones_validas)
            
            if resp_corregida in opciones_validas:
                conteo[resp_corregida] += 1
            elif resp: # Si no es una cadena vacía
                respuestas_no_matcheadas.append(resp)
    
    df_conteo = pd.DataFrame(list(conteo.items()), columns=['opcion', 'cantidad'])
    df_conteo = df_conteo.sort_values(by='cantidad', ascending=False).reset_index(drop=True)
    
    return df_conteo, list(set(respuestas_no_matcheadas))


def limpiar_y_procesar_datos(df):
    """
    Función principal que orquesta todo el proceso de limpieza y preparación de datos.
    
    Args:
        df (pd.DataFrame): El DataFrame original cargado del CSV.

    Returns:
        tuple: Contiene el DataFrame limpio y los diferentes conteos y listas de "otras".
    """
    # 1. Renombrar columnas para facilitar el manejo
    df = df.rename(columns=COLUMNAS_RENOMBRADAS)

    # 2. Crear columna de grupo etario
    bins = [0, 20, 30, 40, 50, 100]
    labels = ['<20', '21-30', '31-40', '41-50', '50+']
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    df['Grupo Etareo'] = pd.cut(df['edad'], bins=bins, labels=labels, right=True)

    # 3. Mapear valores de columnas categóricas a versiones limpias
    df["Identidad genero"] = df["Identidad genero"].map(MAP_GENERO).fillna("Otra")
    df["Identidad personal"] = df["Identidad personal"].map(MAP_IDENTIDAD).fillna("Otra")
    df["Lugar residencia"] = df["Lugar residencia"].map(MAP_RESIDENCIA).fillna("Otro")
    df["Apps citas"] = df["Apps citas"].map(MAP_APPS_CITAS).fillna("Otra")

    # 4. Procesar columnas con respuestas múltiples y corregir "otras"
    conteo_vinculos, otros_vinculos = _procesar_respuestas_multiples(df['Vinculos buscados'], VINCULOS_OPCIONES)
    conteo_actividades, otros_actividades = _procesar_respuestas_multiples(df['Actividades preferidas'], ACTIVIDADES_OPCIONES)
    conteo_bioseguridad, otros_bioseguridad = _procesar_respuestas_multiples(df['Medidas bioseguridad'], BIOSEGURIDAD_OPCIONES)

    # 5. Quitar columnas que ya no se necesitan
    columnas_a_quitar = ['edad', 'Marca temporal', 'Dirección de correo electrónico']
    df_clean = df.drop(columns=[col for col in columnas_a_quitar if col in df.columns])

    return (
        df_clean, 
        conteo_vinculos, 
        conteo_actividades, 
        conteo_bioseguridad, 
        otros_actividades, 
        otros_vinculos, 
        otros_bioseguridad
    )