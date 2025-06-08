import pandas as pd

def limpiar_datos(df):
    columnas_renombradas = {
    '¿Cómo te identificas en relación con el genero femenino?  ': "Identidad género",
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
    df = df.rename(columns=columnas_renombradas)

    bins = [0, 20, 30, 40, 50, 100] 
    labels = ['<20', '21-30', '31-40', '41-50', '50+'] 
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce') 
    df['Grupo Etareo'] = pd.cut(df['edad'], bins=bins, labels=labels, right=True)

    # Limpiar columnas innecesarias
    columnas_a_quitar = [
        'edad',
        #'Marca temporal',
        'Dirección de correo electrónico'
    ]
    for col in columnas_a_quitar:
        if col in df.columns:
            df = df.drop(columns=col)   

    map_genero = {
        "Mujer cis (me asignaron el género femenino al nacer y me identifico como mujer)": "Mujer cis",
        "Mujer trans (me asignaron otro género al nacer y me identifico como mujer)": "Mujer trans",
        "Persona no binaria con experiencia femenina": "No binaria fem"
    }
    df["Identidad género_mapeada"] = df["Identidad género"].map(map_genero).fillna("Otra")
    map_identidad = {
        "Lesbiana": "lesbiana",
        "Bisexual": "bisexual",
        "Pansexual": "pansexual",
        "Heterosexual": "heterosexual"
    }
    df["Identidad genero mapeada"] = df["Identidad personal"].map(map_identidad).fillna("otra")

    map_residencia = {
        "Ciudad Autónoma de Buenos Aires (CABA)": "CABA",
        "Gran Buenos Aires (GBA) - Zona Norte (ej. Vicente López, San Isidro, Tigre, San Fernando, Pilar, Escobar, etc.)": "PBA Norte",
        "Gran Buenos Aires (GBA) - Zona Oeste (ej. Morón, La Matanza, Tres de Febrero, Ituzaingó, Hurlingham, Merlo, Moreno, etc.)": "PBA Oeste",
        "Gran Buenos Aires (GBA) - Zona Sur (ej. Avellaneda, Lanús, Lomas de Zamora, Quilmes, Almirante Brown, Esteban Echeverría, Ezeiza, Berazategui, Florencio Varela, etc.)": "PBA Sur",
        "AMBA, La Plata y alrededores (con fácil acceso a CABA)": "La Plata"
    }
    df["Lugar residencia_mapeada"] = df["Lugar residencia"].apply(
        lambda x: map_residencia[x] if x in map_residencia else x
    )
    #Mapeo uso otras apps
    map_apps = {
        "Si, use para hacer amigas nuevas": "Sí, Amistades",
        "Si, use para conocer a otras mujeres de forma romantica y/o sexual": "Sí, pareja",
        "Si usé, pero solo chatie con chicas y nunca superó la fase virtual": "Solo vínculo virtual",
        "Nunca use apps de ese estilo para conocer a otras mujeres, pero me interesaria": "No, pero quiero",
        "No, y no me interesa": "No"
    }
    df["Apps citas_mapeada"] = df["Apps citas"].map(map_apps).fillna("Otra")

    vinculos_opciones = {
        "Amistades con mujeres que estén dentro o fuera del colectivo LBT+": "amistades con mujeres que estén dentro o fuera del colectivo lbt+",
        "Amistades solo con mujeres que formen parte del colectivo LBT+": "amistades solo con mujeres que formen parte del colectivo lbt+",
        "Amistades solo con mujeres heterosexuales": "amistades solo con mujeres heterosexuales",
        "Redes de apoyo emocional o afectivos": "redes de apoyo emocional o afectivos",
        "Pareja o vínculo romántico/sexoafectivo": "pareja o vínculo romántico/sexoafectivo",
        "Participar en actividades o encuentros sociales/culturales/recreativos": "participar en actividades o encuentros sociales/culturales/recreativos",
        "Sexo ocasional": "sexo ocasional"
    }


    actividades_opciones = {
        "Charlas virtuales o presenciales": "charlas virtuales o presenciales",
        "Foros o grupos temáticos": "foros o grupos temáticos",
        "Encuentros o salidas grupales durante el día en mi zona": "encuentros o salidas grupales durante el día en mi zona",
        "Encuentros o salidas grupales durante la noche en mi zona": "encuentros o salidas grupales durante la noche en mi zona",
        "Actividades de militancia o activismo": "actividades de militancia o activismo",
        "Espacios para compartir arte o escritura": "espacios para compartir arte o escritura",
        "Grupos para organizar actividades deportivas o recreativas": "grupos para organizar actividades deportivas o recreativas",
        "Fiestas de mujeres": "fiestas de mujeres"
    }


    medidas_bioseguridad_opciones = {
    "Verificación de identidad (por foto o redes sociales vinculadas)": "verificación de identidad",
    "Posibilidad de denunciar y bloquear usuarias fácilmente": "denunciar y bloquear",
    "Chat seguro con opción de reportar mensajes": "chat seguro",
    "Función para compartir ubicación con una persona de confianza al tener un encuentro": "compartir ubicación",
    "Posibilidad de puntuar un evento o anfitriona, una vez finalizado el mismo": "puntuar evento o anfitriona",
    "Otra…": "otra"
    }


    def preparar_conteo_actividades(df, columna, opciones_dict):
        # Convertir todas las respuestas en listas, separando por coma
        df[columna] = df[columna].astype(str).str.lower()
        df[columna] = df[columna].apply(lambda x: [op.strip() for op in x.split(",")])

        # Inicializamos el conteo para cada opción
        conteo = {clave: 0 for clave in opciones_dict.keys()}

        # Contamos cuántas veces aparece cada opción en las respuestas
        for lista_respuestas in df[columna]:
            for clave, texto_opcion in opciones_dict.items():
                # Verificamos si alguna opción de la lista incluye el texto de la opción buscada
                if any(texto_opcion.lower() in respuesta for respuesta in lista_respuestas):
                    conteo[clave] += 1

        # Creamos DataFrame resultado
        df_conteo = pd.DataFrame({
            'opcion': list(conteo.keys()),
            'cantidad': list(conteo.values())
        }).sort_values(by='cantidad', ascending=False)

        # Calculamos porcentaje para referencia
        total = df_conteo['cantidad'].sum()
        if total > 0:
            df_conteo['porcentaje'] = df_conteo['cantidad'] / total * 100
        else:
            df_conteo['porcentaje'] = 0

 

        return df_conteo
    
    conteo_vinculos = preparar_conteo_actividades(df, 'Vinculos buscados', vinculos_opciones)
    conteo_actividades = preparar_conteo_actividades(df, 'Actividades preferidas', actividades_opciones)
    conteo_medidas_bioseguridad = preparar_conteo_actividades(df, 'Medidas bioseguridad', medidas_bioseguridad_opciones)

    def detectar_respuestas_no_matcheadas(df, columna, opciones_dict):
        no_matcheadas = []

        for respuesta in df[columna].dropna():
            if isinstance(respuesta, list):
                texto = ", ".join(respuesta).lower()
            else:
                texto = str(respuesta).lower()

            coincidencias = [
                clave for clave in opciones_dict.keys()
                if clave.lower() in texto
            ]
            if not coincidencias:
                # Convertimos respuesta a string para poder hacer set
                if isinstance(respuesta, list):
                    no_matcheadas.append(", ".join(respuesta))
                else:
                    no_matcheadas.append(str(respuesta))

        return list(set(no_matcheadas))


    otros_actividades = detectar_respuestas_no_matcheadas(df, 'Vinculos buscados', vinculos_opciones)
    otros_vinculos = detectar_respuestas_no_matcheadas(df, 'Actividades preferidas', actividades_opciones)
    otros_bioseguridad= detectar_respuestas_no_matcheadas(df, 'Medidas bioseguridad', conteo_medidas_bioseguridad)
    return df, conteo_vinculos, conteo_actividades, conteo_medidas_bioseguridad, otros_actividades, otros_vinculos, otros_bioseguridad
