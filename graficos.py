import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px

# Paleta de colores definida como una constante para reutilizarla
PALETA_PASTEL_LGBTIQ = [
    "#0077BB",  # Azul
    "#EE7733",  # Naranja
    "#009988",  # Turquesa
    "#CC3311",  # Rojo Ladrillo
    "#BBBBBB",  # Gris
    "#EE3377",  # Magenta
    "#33BBEE",  # Cian
]

def plot_pie_chart(df, columna):
    """
    Genera y muestra un gráfico de torta para una columna del DataFrame.
    Si la columna tiene un orden de categoría, lo respeta en la leyenda.
    """
    fig, ax = plt.subplots(figsize=(5, 5)) 

    if pd.api.types.is_categorical_dtype(df[columna]) and df[columna].cat.ordered:
        counts = df[columna].value_counts(sort=False)
    else:
        counts = df[columna].value_counts()
    total = counts.sum()
    legend_labels = [f'{label} ({count/total:.1%})' for label, count in counts.items()]
    wedges, _ = ax.pie(
        counts,
        labels=None,
        startangle=90,
        colors=PALETA_PASTEL_LGBTIQ[:len(counts)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    ax.set_ylabel("")
    ax.legend(
        wedges,
        legend_labels, 
        title="Categorías",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig)

def plot_bar_chart_normalized(df, col, orientacion='horizontal'):
    """
    Genera un gráfico de barras con porcentajes y AÑADE ETIQUETAS
    con el valor exacto en cada barra.
    """
    if col in df.columns:
        if pd.api.types.is_categorical_dtype(df[col]) and df[col].cat.ordered:
            conteo = df[col].value_counts(normalize=True, sort=False) * 100
            order_param = conteo.index 
        else:
            conteo = df[col].value_counts(normalize=True).sort_values(ascending=False) * 100
            order_param = conteo.index
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if orientacion == 'horizontal':
            barplot = sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette=PALETA_PASTEL_LGBTIQ, order=order_param)
            for container in barplot.containers:
                ax.bar_label(
                    container,
                    fmt='%.1f%%',
                    padding=3,
                    fontsize=10
                )
            ax.set_xlim(right=conteo.values.max() * 1.15)
            ax.set_xlabel("% de respuestas")
            ax.set_ylabel("")
        else: # Orientación vertical
            barplot = sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette=PALETA_PASTEL_LGBTIQ, order=order_param)

            for container in barplot.containers:
                ax.bar_label(
                    container,
                    fmt='%.1f%%',
                    padding=3,
                    fontsize=10
                )
            ax.set_ylim(top=conteo.values.max() * 1.15)
            ax.set_ylabel("% de respuestas")
            ax.set_xlabel("")
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        plt.tight_layout()
        st.pyplot(fig)

def plot_bar_chart_from_count(df_conteo, col_categoria, col_valor):
    """
    Genera un gráfico de barras a partir de un DataFrame que ya tiene los conteos.
    Añade etiquetas con los valores a cada barra.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    df_sorted = df_conteo.sort_values(col_valor, ascending=True)
    
    barplot = sns.barplot(
        x=col_valor, 
        y=col_categoria, 
        data=df_sorted, 
        ax=ax, 
        palette=PALETA_PASTEL_LGBTIQ
    )

    # Agrega los valores al final de cada barra
    for index, value in enumerate(df_sorted[col_valor]):
        ax.text(value, index, f' {int(value)}', va='center')

    ax.set_xlabel("Cantidad de Menciones")
    ax.set_ylabel("")
    # Ajustar límites para que el texto no se corte
    ax.set_xlim(right=df_sorted[col_valor].max() * 1.15)
    plt.tight_layout()
    st.pyplot(fig)

def plot_crosstab_chart(df, combinaciones_validas, colormap="Set2"):
    """
    Genera un selector y un gráfico de barras cruzado entre dos variables.
    Las barras del eje Y se ordenan de mayor a menor según el porcentaje total.
    """
    st.header("📊 Gráfico cruzado dinámico")
    columna_segmento = st.selectbox("Selecciona la variable principal:", list(combinaciones_validas.keys()))
    opciones_objetivo = combinaciones_validas.get(columna_segmento, [])
    columna_objetivo = st.selectbox("Selecciona la variable a comparar:", opciones_objetivo)

    if st.button("Generar gráfico cruzado"):
        df_clean = df[[columna_segmento, columna_objetivo]].dropna()
        tabla = pd.crosstab(df_clean[columna_objetivo], df_clean[columna_segmento], normalize='columns') * 100
        df_plot = tabla.round(1).reset_index().melt(id_vars=columna_objetivo, var_name=columna_segmento, value_name='Porcentaje')
        order_of_categories = df_plot.groupby(columna_objetivo)['Porcentaje'].sum().sort_values(ascending=False).index

        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.barplot(
            data=df_plot, 
            x='Porcentaje', 
            y=columna_objetivo, 
            hue=columna_segmento, 
            palette=colormap, 
            ax=ax,
            order=order_of_categories 
        )

        ax.set_xlabel("Porcentaje (%)")
        ax.set_ylabel("")
        ax.set_title(f"Análisis de '{columna_objetivo}' según '{columna_segmento}'")
        ax.legend(title=columna_segmento, bbox_to_anchor=(1.05, 0.5), loc='center left')
        plt.tight_layout()
        st.pyplot(fig)

def add_footer():
    """Añade un footer personalizado a la página de Streamlit."""
    st.markdown("""
    <style>
     .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #0A0F1C; color: #EAEAEA;
        text-align: center; padding: 1em 0; font-size: 0.9em;
        z-index: 100;
    }
    .footer a { color: #00C2A8; text-decoration: none; margin: 0 0.5em; }
    </style>
    <div class="footer">
        © 2025 KnowLytics IA | <a href="mailto:knowlytics.ia@gmail.com">knowlytics.ia@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

def create_categorical_bubble_chart(df_agg, x_col, y_col, size_col, color_col, title,mapa_valores_color):
    """
    Crea un gráfico de burbujas categórico donde el tamaño y el color
    representan métricas agregadas.
    """
    if df_agg is None or df_agg.empty:
        return None
    mapa_inverso = {v: k for k, v in mapa_valores_color.items()}

    # Obtenemos los valores mínimo y máximo de la escala de color para etiquetarlos
    min_val = df_agg[color_col].min()
    max_val = df_agg[color_col].max()
    fig = px.scatter(
        df_agg,
        x=x_col,
        y=y_col,
        size=size_col,          # El tamaño de la burbuja es el conteo de personas
        color=color_col,        # El color es el promedio de facilidad
        hover_name=x_col,
        size_max=50,            # Tamaño máximo de la burbuja más grande
        title=title,
        color_continuous_scale=px.colors.sequential.Viridis, # Paleta de color (cálido = alto)
        labels={
            color_col: "Facilidad Promedio",
            size_col: "Nº de Respuestas"
        }
    )
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        # Personalizamos la barra de color
        coloraxis_colorbar=dict(
            title="Facilidad Promedio",
            # Mostramos etiquetas en los puntos clave de la barra
            tickvals=[min_val, max_val],
            ticktext=[f"Más Difícil ({mapa_inverso.get(min_val, '')})", f"Más Fácil ({mapa_inverso.get(max_val, '')})"]
        )
    )
    
    return fig