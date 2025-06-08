import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def grafico_torta(df, columna):
    fig, ax = plt.subplots(figsize=(4, 4))
    counts = df[columna].value_counts()
    wedges, texts = ax.pie(
        counts,
        labels=None,          # sin etiquetas dentro
        startangle=90,
        wedgeprops={'edgecolor': 'black'}
    )
    ax.set_ylabel("")
    # Leyenda al costado con etiquetas y colores
    ax.legend(
        wedges,
        counts.index,
        title="Categorías",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig)



def grafico_barras(df, col, orientacion):
    if col in df.columns:
            conteo = df[col].value_counts(normalize=True).sort_values(ascending=False if orientacion == 'horizontal' else False) * 100
            fig, ax = plt.subplots(figsize=(8, 4.5))
            if orientacion == 'horizontal':
                sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="crest")
                ax.set_xlabel("% de respuestas")
                ax.set_ylabel("")
            else:
                sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette="crest")
                ax.set_ylabel("% de respuestas")
                ax.set_xlabel("")
                ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
            
def grafico_barras_conteo2(df, col_categoria, col_valor):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    barplot = sns.barplot(
        x=col_valor, 
        y=col_categoria, 
        data=df, 
        ax=ax, 
        palette="crest"
    )

    # Agrega los valores al final de cada barra
    for index, value in enumerate(df[col_valor]):
        ax.text(value + 1, index, str(int(value)), va='center')  # +1 para separar del borde

    ax.set_ylabel("Cantidad de respuestas")
    ax.set_xlabel("")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)




def graficos_cruzados(df, combinaciones_validas, colormap="Set2"):
    st.header("📊 Gráfico cruzado dinámico")
    columna_segmento = st.selectbox("Variable explicativa", list(combinaciones_validas.keys()))
    opciones_objetivo = combinaciones_validas.get(columna_segmento, [])
    columna_objetivo = st.selectbox("Variable a explicar", opciones_objetivo)

    if st.button("Generar gráfico"):
        # Limpiar datos nulos en ambas columnas
        df_clean = df[[columna_segmento, columna_objetivo]].dropna()

        # Tabla cruzada con normalización por columna para % dentro de cada segmento
        tabla = pd.crosstab(df_clean[columna_objetivo], df_clean[columna_segmento], normalize='columns') * 100
        tabla = tabla.round(1)

        if tabla.index.dtype == 'O':
            tabla = tabla.sort_index()

        # Preparar datos para seaborn
        df_plot = tabla.reset_index().melt(id_vars=columna_objetivo, var_name=columna_segmento, value_name='Porcentaje')

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=df_plot, x='Porcentaje', y=columna_objetivo, hue=columna_segmento, palette=colormap, ax=ax)

        ax.set_xlabel("Porcentaje (%)")
        ax.set_ylabel("")
        ax.set_title(f"Cruce: {columna_objetivo} vs {columna_segmento}")
        ax.legend(title=columna_segmento, bbox_to_anchor=(1.05, 0.5), loc='center left')
        st.pyplot(fig)


def grafico_barras_conteo(df, col_categoria, col_valor):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=col_valor, y=col_categoria, data=df, ax=ax, palette="crest")
    ax.set_xlabel("Frecuencia de menciones")
    ax.set_ylabel("")
    st.pyplot(fig)

def addFooter():
    st.markdown("""
    <style>
     .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0A0F1C;
        color: #EAEAEA;
        text-align: center;
        padding: 1em 0;
        font-size: 0.9em;
        font-family: Helvetica, sans-serif;
        z-index: 100;
    }
    .footer a {
        color: #00C2A8;
        text-decoration: none;
        margin: 0 0.5em;
    }
    @media (max-width: 600px) {
        .footer {
            font-size: 0.8em;
            padding: 0.8em 0;
        }
    }
    </style>
    <div class="footer">
        © 2025 KnowLytics IA |         
        <a href="mailto:knowlytics.ia@gmail.com">knowlytics.ia@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

