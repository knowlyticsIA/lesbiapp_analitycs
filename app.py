import streamlit as st
import pandas as pd
import json
import plotly.express as px

from utils import MAPEO_FACILIDAD_NUM
from graficos import (
    plot_pie_chart, plot_bar_chart_normalized, plot_bar_chart_from_count,
    plot_crosstab_chart, create_heatmap, create_categorical_bubble_chart, add_footer
)

st.set_page_config(
    page_title="Dashboard LesBi App",
    page_icon="📊",
    layout="centered"
)

@st.cache_data
def cargar_datos_preprocesados():
    try:
        datos = {
            "df_clean": pd.read_parquet("data/cleaned_data.parquet"),
            "df_segmentado_edad": pd.read_parquet("data/segmento_20_50_data.parquet"),
            "conteo_actividades": pd.read_parquet("data/conteo_actividades_individuales.parquet"),
            "conteo_vinculos": pd.read_parquet("data/conteo_vinculos_individuales.parquet"),
            "conteo_bioseguridad": pd.read_parquet("data/conteo_bioseguridad.parquet")
        }
        return datos
    except Exception as e:
        st.error(f"🛑 Error: No se encontró el archivo {e.filename}. "
                 "Por favor, asegúrate de haber ejecutado el script 'preprocess.py' primero.")
        return None

datos = cargar_datos_preprocesados()

if datos:
    st.title("Dashboard de Encuesta LesBi App")

    with st.sidebar:
        st.title("Navegación")
        tabs = [
            "📊 Inicio - Visión General",
            "🧑‍🤝‍🧑 Perfil y Características",
            "🔄 Análisis Cruzado Flexible",
            "🔬 Análisis Segmento 20-50",
            "🔬 Diagrama de dispersión"
        ]
        selected_tab = st.radio("Ir a:", tabs)

    if selected_tab == "📊 Inicio - Visión General":
        st.header("Visión General del Proyecto")
        st.markdown("""
            ¡Bienvenidxs al dashboard interactivo de Lesbi App! 
            Este espacio está diseñado para explorar los resultados de nuestra encuesta y entender mejor a nuestra comunidad.
        """)
        st.subheader(f"Total de Respuestas Válidas: {len(datos['df_clean'])}")
        st.info("Los datos han sido anonimizados y procesados para garantizar la privacidad de lxs participantes.")

    elif selected_tab == "🧑‍🤝‍🧑 Perfil y Características":
        st.header("Perfil de lxs Encuestadxs")
        st.markdown("Explora el perfil de quienes participan en Lesbi App.")

        columnas_torta = ['Grupo Etareo', 'Recibir novedades', 'Facilidad conocer LesBi', 'Facilidad conocer hetero']
        columnas_barras = ['Identidad genero', 'Identidad sexual', 'Lugar residencia', 'Opinion apps no amorosas', 'Nivel educativo', 'apps_citas_mapeada']
        
        st.subheader("Características Demográficas y de Opinión")
        for col in datos['df_clean'].columns:
            if col in columnas_torta:
                st.write(f"**{col}**")
                plot_pie_chart(datos['df_clean'], col)
            elif col in columnas_barras:
                st.write(f"**{col}**")
                plot_bar_chart_normalized(datos['df_clean'], col, orientacion='horizontal')

        st.subheader("Preferencias de la Comunidad (Combinaciones más populares)")
        conteos_multiples = {
            'Combinaciones de Actividades Preferidas': datos['conteo_actividades'],
            'Combinaciones de Vínculos Buscados': datos['conteo_vinculos'],
            'Medidas de Bioseguridad Solicitadas': datos['conteo_bioseguridad']
        }
        for titulo, df_conteo in conteos_multiples.items():
            st.write(f"**{titulo}**")
            plot_bar_chart_from_count(df_conteo, 'opcion', 'cantidad')
        
        with st.expander("Ver respuestas 'Otras' no clasificadas"):
            st.write("**Otras medidas de bioseguridad mencionadas:**", datos['otros_bioseguridad'])

    elif selected_tab == "🔄 Análisis Cruzado Flexible":
        st.header("Análisis Cruzado Flexible")
        st.markdown("Selecciona dos variables cualesquiera para cruzarlas y analizar su relación.")
        
        lista_variables_analisis = sorted([col for col in datos['df_clean'].columns if col not in ['Vinculos buscados', 'Actividades preferidas', 'Medidas bioseguridad']])
        
        col1, col2 = st.columns(2)
        with col1:
            var_1 = st.selectbox("Selecciona la primera variable (Eje Y):", lista_variables_analisis, index=lista_variables_analisis.index('Actividades Agrupadas'))
        opciones_var_2 = [v for v in lista_variables_analisis if v != var_1]
        with col2:
            var_2 = st.selectbox("Selecciona la segunda variable (Segmento de color):", opciones_var_2, index=opciones_var_2.index('Grupo Etareo'))

        tipo_grafico = st.radio("Selecciona el tipo de visualización:", ("Gráfico de Barras (Porcentajes)", "Mapa de Calor (Conteos)"), horizontal=True)

        if st.button("Generar análisis"):
            if tipo_grafico == "Gráfico de Barras (Porcentajes)":
                plot_crosstab_chart(datos['df_clean'], columna_y=var_1, columna_hue=var_2)
            else:
                create_heatmap(datos['df_clean'], var_1, var_2)

    elif selected_tab == "🔬 Análisis Segmento 20-50":
        st.header("Análisis Enfocado: Segmento 20 a 50 Años")
        st.markdown("Análisis cruzado filtrado únicamente para las participantes entre 20 y 50 años.")
        st.info(f"Este análisis se basa en un total de **{len(datos['df_segmentado_edad'])}** respuestas.", icon="🎯")

        lista_variables_analisis = sorted([col for col in datos['df_segmentado_edad'].columns if col not in ['Vinculos buscados', 'Actividades preferidas', 'Medidas bioseguridad']])
        
        col1, col2 = st.columns(2)
        with col1:
            var_1_seg = st.selectbox("Selecciona la primera variable (Eje Y):", lista_variables_analisis, index=lista_variables_analisis.index('Actividades Agrupadas'), key='edad_var1')
        opciones_var_2_seg = [v for v in lista_variables_analisis if v != var_1_seg]
        with col2:
            var_2_seg = st.selectbox("Selecciona la segunda variable (Segmento de color):", opciones_var_2_seg, index=opciones_var_2_seg.index('Grupo Etareo'), key='edad_var2')

        tipo_grafico_seg = st.radio("Selecciona el tipo de visualización:", ("Gráfico de Barras (Porcentajes)", "Mapa de Calor (Conteos)"), horizontal=True, key='edad_radio')

        if st.button("Generar análisis en este segmento", key='edad_button'):
            df_segmentado = datos["df_segmentado_edad"]
            if tipo_grafico_seg == "Gráfico de Barras (Porcentajes)":
                plot_crosstab_chart(df_segmentado, columna_y=var_1_seg, columna_hue=var_2_seg)
            else:
                create_heatmap(df_segmentado, var_1_seg, var_2_seg)

    elif selected_tab == "🔬 Diagrama de dispersión":
        st.header("Análisis Comparativo de Facilidad (Burbujas)")
        st.markdown("Compara la facilidad para conocer gente LBT+ vs. Hetero. El tamaño de la burbuja indica el número de respuestas y el color la facilidad promedio.")
        st.info("ℹ️ **Nota sobre el color:** Una burbuja más clara (amarilla) indica mayor facilidad, mientras que una más oscura (violeta) indica mayor dificultad.", icon="ℹ️")

        opciones_ejes_bubble = ['Lugar residencia', 'Grupo Etareo', 'Identidad genero', 'Identidad sexual', 'Convivencia', 'Opinion apps no amorosas']
        
        col1, col2 = st.columns(2)
        with col1:
            var_x_b = st.selectbox("Elige la variable para el Eje X:", options=opciones_ejes_bubble, index=0, key='bubble_x')
        with col2:
            var_y_b = st.selectbox("Elige la variable para el Eje Y:", options=opciones_ejes_bubble, index=1, key='bubble_y')

        if var_x_b != var_y_b:
            df_lbt_agg = datos['df_clean'].groupby([var_x_b, var_y_b]).agg(conteo=('Identidad sexual', 'size'), facilidad_promedio=('Facilidad LesBi Num', 'mean')).reset_index()
            df_hetero_agg = datos['df_clean'].groupby([var_x_b, var_y_b]).agg(conteo=('Identidad sexual', 'size'), facilidad_promedio=('Facilidad Hetero Num', 'mean')).reset_index()
            
            fig_lbt = create_categorical_bubble_chart(df_lbt_agg, var_x_b, var_y_b, 'conteo', 'facilidad_promedio', 'Facilidad para Conocer Comunidad LBT+', MAPEO_FACILIDAD_NUM)
            fig_hetero = create_categorical_bubble_chart(df_hetero_agg, var_x_b, var_y_b, 'conteo', 'facilidad_promedio', 'Facilidad para Conocer Comunidad Hetero', MAPEO_FACILIDAD_NUM)

            if fig_lbt:
                st.plotly_chart(fig_lbt, use_container_width=True)
            st.divider()
            if fig_hetero:
                st.plotly_chart(fig_hetero, use_container_width=True)
        else:
            st.warning("Por favor, selecciona dos variables diferentes para los ejes X e Y.")

    add_footer()