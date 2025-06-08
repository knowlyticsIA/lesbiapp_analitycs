import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

# Paleta de colores definida como una constante para reutilizarla
PALETA_PASTEL_LGBTIQ = [
    "#FFA8A8", "#FFD8A8", "#FFF2A8", "#A8E6A3",
    "#A8D0FF", "#D2A8FF", "#FFB3DE"
]

def plot_pie_chart(df, columna):
    """Genera y muestra un gráfico de torta para una columna del DataFrame."""
    fig, ax = plt.subplots(figsize=(4, 4))
    counts = df[columna].value_counts()
    palette = PALETA_PASTEL_LGBTIQ[:len(counts)]
    
    wedges, _ = ax.pie(
        counts,
        labels=None,
        startangle=90,
        colors=palette,
        wedgeprops={'edgecolor': 'black'}
    )
    ax.set_ylabel("")
    ax.legend(
        wedges,
        counts.index,
        title="Categorías",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig)

def plot_bar_chart_normalized(df, col, orientacion='horizontal'):
    """Genera y muestra un gráfico de barras con porcentajes para una columna, ordenado de mayor a menor."""
    if col in df.columns:
        # Los datos ya se ordenan aquí
        conteo = df[col].value_counts(normalize=True).sort_values(ascending=False) * 100
        fig, ax = plt.subplots(figsize=(8, 4.5))
        
        if orientacion == 'horizontal':
            # Pasamos el índice ordenado al parámetro 'order' para garantizar la visualización
            sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="crest", order=conteo.index)
            ax.set_xlabel("% de respuestas")
            ax.set_ylabel("")
        else:
            # Hacemos lo mismo para el gráfico vertical
            sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette="crest", order=conteo.index)
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

        # --- INICIO DE LA MODIFICACIÓN ---
        # 1. Calcular el orden: Agrupamos por categoría del eje Y, sumamos sus porcentajes y ordenamos.
        order_of_categories = df_plot.groupby(columna_objetivo)['Porcentaje'].sum().sort_values(ascending=False).index
        # --- FIN DE LA MODIFICACIÓN ---

        fig, ax = plt.subplots(figsize=(8, 6))
        
        # 2. Pasamos el orden calculado al parámetro 'order' del gráfico.
        sns.barplot(
            data=df_plot, 
            x='Porcentaje', 
            y=columna_objetivo, 
            hue=columna_segmento, 
            palette=colormap, 
            ax=ax,
            order=order_of_categories # <-- Aquí aplicamos el orden
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