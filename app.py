import streamlit as st # type: ignore
from utils import *
from graficos import *

# Configuración

st.set_page_config(layout="centered")
st.title("Dashboard de LesBi App")
# Cargar y limpiar datos
data_file = "data/encuesta_mujeres.csv"
df = pd.read_csv(data_file)
df_clean, conteo_vinculos, conteo_actividades, conteo_bioseguridad, otros_actividades, otros_vinculos, otros_bioseguridad = limpiar_datos(df)

# Sidebar de navegación
st.sidebar.title("Navegación")
tabs = [
    "📊 Inicio - Visión General",
    "🧑‍🤝‍🧑 Perfil y Características",
    "🔄 Análisis Cruzado de Variables"
]
selected_tab = st.sidebar.radio("Ir a:", tabs)

# Tab 1: Introducción
if selected_tab == "📊 Inicio - Visión General":
    st.markdown("""                
        Bienvenidos al dashboard de Lesbi App. 
                
        En este espacio podrás explorar:
                

        👥 El perfil de nuestros participantes: Conociendo quiénes son, qué edad tienen y cómo se conectan con nuestro proyecto.

        💡 Sus opiniones y percepciones: Qué piensan sobre nuestras propuestas y actividades, y cómo evalúan su experiencia.

        🎭 Su participación en los eventos: Cómo viven y se sienten dentro de las actividades que organizamos.

        ❤️ Áreas de mejora: Identificar oportunidades para seguir creciendo juntos y hacer de Lesbi App un proyecto cada vez más inclusivo y enriquecedor.
    """)
    respuestas = len(df_clean)
    st.subheader(f"Total de respuestas a la encuesta: {respuestas}")

# Tab 2: Perfil y Características
elif selected_tab == "🧑‍🤝‍🧑 Perfil y Características":
    st.header("Análisis inicial encuestadxs") 
    st.markdown("""Explora el perfil de quienes participan en Lesbi App: desde su identidad de género, edad y lugar de residencia, hasta sus experiencias y percepciones sobre el proyecto. Esta sección permite conocer mejor a la comunidad para atender sus necesidades y fortalecer sus vínculos, tanto de amistad como románticos.""")   
    barras_columna = ['Identidad genero mapeada', 'Identidad genero mapeada', 'lugar_residencia_mapeada',  'Opinion apps no amorosas','Nivel educativo','apps_citas_mapeada']
    torta_columnas = ['Grupo Etareo','recibir_novedades','Facilidad conocer LesBi', 'Facilidad conocer hetero']
    barras_conteo = {
    'Conteo actividades': conteo_actividades,
    'Conteo vinculos': conteo_vinculos,
    'Conteo Medidas bioseguridad': conteo_bioseguridad
    }

    for col in df_clean.columns:
        if col in torta_columnas:
            st.subheader(col)
            grafico_torta(df_clean, col)
        elif col in barras_columna:
            st.subheader(col)
            grafico_barras(df_clean, col, orientacion='horizontal')
    for nombre, df_conteo in barras_conteo.items():
        st.subheader(nombre)
        grafico_barras_conteo2(df_conteo, 'opcion', 'cantidad')
    st.write("Respuestas no matcheadas en actividades:")
    st.write(otros_actividades)
    st.write("Respuestas no matcheadas en vinculos:")
    st.write(otros_vinculos)
    st.write("Respuestas no matcheadas en bioseguridad:")
    st.write(otros_bioseguridad)


# Tab 3: Cruces entre variables
elif selected_tab == "🔄 Análisis Cruzado de Variables":
    st.markdown("""Aquí podrás realizar análisis cruzados entre diferentes variables para descubrir patrones y relaciones dentro de la comunidad. Esta sección ayuda a identificar tendencias relevantes, puntos comunes y diferencias, aportando una visión más profunda que orienta las mejoras y nuevas propuestas para Lesbi App.""")
    combinaciones_validas = {
        'Identidad genero mapeada': [
            'Vinculos faltantes', 'Vinculos buscados', 'Facilidad conocer LesBi',
            'Facilidad conocer hetero', 'Opinion apps no amorosas',
            'Medidas bioseguridad', 'Actividades preferidas'
        ],
        'Identidad personal': [
            'Vinculos faltantes', 'Vinculos buscados', 'Facilidad conocer LesBi',
            'Facilidad conocer hetero', 'Opinion apps no amorosas',
            'Medidas bioseguridad', 'Actividades preferidas', 'Lugar residencia', 'Recibir novedades'
        ],
        'Apps citas': [
            'Vinculos faltantes', 'Vinculos buscados', 'Facilidad conocer LesBi',
            'Facilidad conocer hetero', 'Opinion apps no amorosas', 'Nivel educativo'
        ],
        'Grupo Etareo': [
            'Nivel educativo', 'Convivencia', 'Vinculos faltantes', 'Vinculos buscados',
            'Facilidad conocer LesBi', 'Facilidad conocer hetero', 'Opinion apps no amorosas',
            'Medidas bioseguridad', 'Actividades preferidas', 'Lugar residencia', 'Recibir novedades'
        ]
    }

    graficos_cruzados(df_clean, combinaciones_validas)

addFooter()
