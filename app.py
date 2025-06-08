import streamlit as st
import pandas as pd
import json
from graficos import *
from utils import *

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard LesBi App",
    page_icon="📊",
    layout="centered"
)

# --- FUNCIÓN DE CARGA DE DATOS PRE-PROCESADOS ---
@st.cache_data 
def cargar_datos_preprocesados():
    """
    Carga los datos ya limpios desde los archivos Parquet y JSON.
    Esta función es extremadamente rápida.
    """
    try:
        df_clean = pd.read_parquet("data/cleaned_data.parquet")
        conteo_vinculos = pd.read_parquet("data/conteo_vinculos.parquet")
        conteo_actividades = pd.read_parquet("data/conteo_actividades.parquet")
        conteo_bioseguridad = pd.read_parquet("data/conteo_bioseguridad.parquet")
        
        with open("data/otras_respuestas.json", 'r', encoding='utf-8') as f:
            otras_data = json.load(f)
        
        otros_actividades = otras_data['actividades']
        otros_vinculos = otras_data['vinculos']
        otros_bioseguridad = otras_data['bioseguridad']

        return (
            df_clean, 
            conteo_vinculos, 
            conteo_actividades, 
            conteo_bioseguridad, 
            otros_actividades, 
            otros_vinculos, 
            otros_bioseguridad
        )
    except FileNotFoundError:
        st.error(
            "🛑 No se encontraron los archivos de datos pre-procesados. "
            "Por favor, ejecuta el script 'python preprocesar_datos.py' en tu terminal primero."
        )
        return None, None, None, None, None, None, None

# --- CARGA DE DATOS ---
with st.spinner('Cargando datos del dashboard...'):
    (df_clean, conteo_vinculos, conteo_actividades, conteo_bioseguridad, 
     otros_actividades, otros_vinculos, otros_bioseguridad) = cargar_datos_preprocesados()
#Para ver las columnas mappeadas
#if df_clean is not None:
#    st.write("🕵️‍♂️ **Columnas disponibles en df_clean:**", df_clean.columns.tolist())

# --- UI PRINCIPAL ---
if df_clean is not None:
    st.title("Dashboard de Encuesta LesBi App")

    with st.sidebar:
        st.title("Navegación")
        tabs = [
            "📊 Inicio - Visión General",
            "🧑‍🤝‍🧑 Perfil y Características",
            "🔄 Análisis Cruzado de Variables",
            "🔬 Análisis de Dispersión"
        ]
        selected_tab = st.radio("Ir a:", tabs)

if selected_tab == "📊 Inicio - Visión General":
    st.header("Visión General del Proyecto")
    st.markdown("""                
        ¡Bienvenidxs al dashboard interactivo de Lesbi App! 
                
        Este espacio está diseñado para explorar los resultados de nuestra encuesta y entender mejor a nuestra comunidad. Aquí podrás navegar por:
                
        - **Perfil de participantes:** Quiénes son, qué edad tienen y cómo se conectan.
        - **Opiniones y percepciones:** Qué piensan de las propuestas y cómo evalúan su experiencia.
        - **Participación en eventos:** Cómo viven y sienten las actividades.
        - **Áreas de mejora:** Oportunidades para seguir creciendo y hacer de Lesbi App un proyecto más inclusivo.
    """)
    st.subheader(f"Total de Respuestas Válidas: {len(df_clean)}")
    st.info("Los datos han sido anonimizados y procesados para garantizar la privacidad de lxs participantes.")

elif selected_tab == "🧑‍🤝‍🧑 Perfil y Características":
    st.header("Perfil de lxs Encuestadxs")
    st.markdown("""
    Explora el perfil de quienes participan en Lesbi App: desde su identidad de género, edad y lugar de residencia, hasta sus experiencias y percepciones sobre el proyecto.
    """)

    # Definimos qué tipo de gráfico usar para cada columna
    columnas_torta = ['Grupo Etareo', 'recibir_novedades', 'Facilidad conocer LesBi', 'Facilidad conocer hetero']
    columnas_barras = ['Identidad genero', 'Identidad personal', 'Lugar residencia', 'Opinion apps no amorosas', 'Nivel educativo', 'apps_citas_mapeada']
    
    st.subheader("Características Demográficas y de Opinión")
    for col in df_clean.columns:
        if col in columnas_torta:
            st.write(f"**{col}**")
            plot_pie_chart(df_clean, col)
        elif col in columnas_barras:
            st.write(f"**{col}**")
            plot_bar_chart_normalized(df_clean, col, orientacion='horizontal')

    st.subheader("Preferencias de la Comunidad")
    conteos_multiples = {
        'Actividades Preferidas por la Comunidad': conteo_actividades,
        'Tipos de Vínculos Buscados': conteo_vinculos,
        'Medidas de Bioseguridad Solicitadas': conteo_bioseguridad
    }

    for titulo, df_conteo in conteos_multiples.items():
        st.write(f"**{titulo}**")
        plot_bar_chart_from_count(df_conteo, 'opcion', 'cantidad')

    with st.expander("Ver respuestas 'Otras' no clasificadas"):
        st.write("**Actividades no matcheadas:**", otros_actividades)
        st.write("**Vínculos no matcheados:**", otros_vinculos)
        st.write("**Bioseguridad no matcheada:**", otros_bioseguridad)

elif selected_tab == "🔄 Análisis Cruzado de Variables":
    st.header("Análisis Cruzado de Variables")
    st.markdown("""
    Aquí podrás realizar análisis cruzados para descubrir patrones y relaciones dentro de la comunidad. 
    Esta sección ayuda a identificar tendencias, orientando mejoras y nuevas propuestas.
    """)
    
    combinaciones_validas = {
        'Grupo Etareo': [
            'Nivel educativo', 'Convivencia', 'Vinculos Agrupados', 
            'Facilidad conocer LesBi', 'Facilidad conocer hetero', 'Opinion apps no amorosas',
            'Medidas bioseguridad', 'Actividades Agrupadas',
            'Lugar residencia', 'Recibir novedades'
        ],
        'Identidad genero': [
            'Vinculos Agrupados', 
            'Facilidad conocer LesBi', 'Facilidad conocer hetero',
            'Opinion apps no amorosas', 'Medidas bioseguridad',
            'Actividades Agrupadas' 
        ],
        'Identidad personal': [
            'Vinculos Agrupados', 
            'Facilidad conocer LesBi', 'Facilidad conocer hetero',
            'Opinion apps no amorosas', 'Medidas bioseguridad',
            'Actividades Agrupadas', 
            'Lugar residencia', 'Recibir novedades'
        ],
        'Apps citas': [
            'Vinculos Agrupados', 
            'Facilidad conocer LesBi', 'Facilidad conocer hetero',
            'Opinion apps no amorosas', 'Nivel educativo'
        ]
    }
    plot_crosstab_chart(df_clean, combinaciones_validas)

elif selected_tab == "🔬 Análisis de Dispersión":
    st.header("Análisis de Dispersión por Facilidad")
    st.markdown("""
    Esta sección te permite explorar la relación entre la facilidad para conocer a la comunidad LBT+ y a la comunidad heterosexual.
    
    Usa los selectores para definir los ejes y elige una tercera variable para colorear los puntos y descubrir patrones visuales.
                
    st.info("ℹ️ **Nota sobre el color:** Una burbuja más clara (amarilla) indica mayor facilidad, mientras que una más oscura (violeta) indica mayor dificultad.", icon="ℹ️")
    """)
    st.subheader("Selección de Variables")
    opciones_color = ['Facilidad LesBi Num', 'Facilidad Hetero Num']
    opciones_ejes = [
        'Lugar residencia', 
        'Grupo Etareo', 
        'Identidad genero', 
        'Identidad personal',
        'Convivencia',
        'Opinion apps no amorosas'
    ]
    col1, col2 = st.columns(2)
    with col1:
        var_x = st.selectbox("Elige la variable para el Eje X:", options=opciones_ejes, index=0, key='scatter_x')
    with col2:
        default_y_index = 1 if len(opciones_ejes) > 1 else 0
        var_y = st.selectbox("Elige la variable para el Eje Y:", options=opciones_ejes, index=default_y_index)

    if var_x != var_y:
        df_lbt_agg = df_clean.groupby([var_x, var_y]).agg(
            conteo=('Identidad personal', 'size'),
            facilidad_promedio=('Facilidad LesBi Num', 'mean')
        ).reset_index()

        df_hetero_agg = df_clean.groupby([var_x, var_y]).agg(
            conteo=('Identidad personal', 'size'),
            facilidad_promedio=('Facilidad Hetero Num', 'mean')
        ).reset_index()

        fig_lbt = create_categorical_bubble_chart(df_lbt_agg, var_x, var_y, 'conteo', 'facilidad_promedio', 'Facilidad para Conocer Comunidad LBT+', MAPEO_FACILIDAD_NUM)
        fig_hetero = create_categorical_bubble_chart(df_hetero_agg, var_x, var_y, 'conteo', 'facilidad_promedio', 'Facilidad para Conocer Comunidad Hetero', MAPEO_FACILIDAD_NUM)
        
        if fig_lbt:
            st.plotly_chart(fig_lbt, use_container_width=True)
            st.divider() 
            if fig_hetero:
                st.plotly_chart(fig_hetero, use_container_width=True)
    else:
        st.warning("Por favor, selecciona dos variables diferentes para los ejes X e Y.")



add_footer()
