import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px

PALETA_PRINCIPAL = [
    "#D62828",  # Rojo Fuerte
    "#F77F00",  # Naranja Intenso
    "#FCA311",  # Amarillo Oro
    "#4CAF50",  # Verde Intenso
    "#2196F3",  # Azul Vívido
    "#673AB7",  # Púrpura Profundo
    "#E91E63",  # Magenta
]

def plot_pie_chart(df, columna):
    """Genera y muestra un gráfico de torta para una columna del DataFrame."""
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
        colors=PALETA_PRINCIPAL, 
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    ax.set_ylabel("")
    ax.legend(
        wedges, legend_labels, title="Categorías",
        loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
    )
    st.pyplot(fig)

def plot_bar_chart_normalized(df, col, orientacion='horizontal'):
    """Genera un gráfico de barras con porcentajes y etiquetas en cada barra."""
    if col in df.columns:
        if pd.api.types.is_categorical_dtype(df[col]) and df[col].cat.ordered:
            conteo = df[col].value_counts(normalize=True, sort=False) * 100
        else:
            conteo = df[col].value_counts(normalize=True).sort_values(ascending=False) * 100
        
        order_param = conteo.index

        fig, ax = plt.subplots(figsize=(8, 5))
        
        if orientacion == 'horizontal':
            barplot = sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette=PALETA_PRINCIPAL, order=order_param)
            ax.set_xlim(right=conteo.values.max() * 1.15)
        else: # Orientación vertical
            barplot = sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette=PALETA_PRINCIPAL, order=order_param)
            ax.set_ylim(top=conteo.values.max() * 1.15)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        for container in barplot.containers:
            ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=10)
        
        ax.set_xlabel("% de respuestas" if orientacion == 'horizontal' else "")
        ax.set_ylabel("" if orientacion == 'horizontal' else "% de respuestas")
        
        plt.tight_layout()
        st.pyplot(fig)

def plot_bar_chart_from_count(df_conteo, col_categoria, col_valor):
    """Genera un gráfico de barras a partir de un DataFrame que ya tiene los conteos."""
    fig, ax = plt.subplots(figsize=(8, 5))
    df_sorted = df_conteo.sort_values(col_valor, ascending=True)
    
    barplot = sns.barplot(x=col_valor, y=col_categoria, data=df_sorted, ax=ax, palette=PALETA_PRINCIPAL)

    for index, value in enumerate(df_sorted[col_valor]):
        ax.text(value, index, f' {int(value)}', va='center')

    ax.set_xlabel("Cantidad de Menciones")
    ax.set_ylabel("")
    ax.set_xlim(right=df_sorted[col_valor].max() * 1.15)
    plt.tight_layout()
    st.pyplot(fig)

def plot_crosstab_chart(df, columna_y, columna_hue, colormap="Set2"):
    """Genera un gráfico de barras cruzado que desanida las respuestas múltiples."""
    df_filtrado = df[[columna_hue, columna_y]].dropna(subset=[columna_y])
    total_por_segmento = df_filtrado[columna_hue].value_counts()

    if pd.api.types.is_string_dtype(df_filtrado[columna_y]):
        df_explotado = df_filtrado.assign(**{columna_y: df_filtrado[columna_y].str.split(r'\s*,\s*')}).explode(columna_y)
    else:
        df_explotado = df_filtrado
        
    tabla_conteo = pd.crosstab(df_explotado[columna_y], df_explotado[columna_hue])
    tabla_porcentaje = tabla_conteo.copy()
    for col in tabla_porcentaje.columns:
        if total_por_segmento.get(col, 0) > 0:
            tabla_porcentaje[col] = (tabla_porcentaje[col] / total_por_segmento[col]) * 100
    
    df_plot = tabla_porcentaje.round(1).reset_index().melt(id_vars=columna_y, var_name=columna_hue, value_name='Porcentaje')
    order_of_categories = df_plot.groupby(columna_y)['Porcentaje'].sum().sort_values(ascending=False).index

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=df_plot, x='Porcentaje', y=columna_y, hue=columna_hue, palette=PALETA_PRINCIPAL, ax=ax, order=order_of_categories)
    ax.set_xlabel("Porcentaje de Menciones (%)")
    ax.set_ylabel(columna_y)
    ax.set_title(f"Análisis de '{columna_y}' según '{columna_hue}'")
    ax.legend(title=columna_hue, bbox_to_anchor=(1.02, 0.5), loc='center left')
    plt.tight_layout()
    st.pyplot(fig)

def create_heatmap(df, var_x, var_y):
    """Crea y muestra un mapa de calor para dos variables categóricas."""
    if var_x not in df.columns or var_y not in df.columns:
        st.error(f"Una o ambas columnas ('{var_x}', '{var_y}') no se encontraron en los datos.")
        return
    crosstab_data = pd.crosstab(df[var_x], df[var_y])
    height = len(crosstab_data) * 0.5 + 2 
    width = len(crosstab_data.columns) * 1 + 2
    fig, ax = plt.subplots(figsize=(max(width, 8), max(height, 6)))
    sns.heatmap(crosstab_data, annot=True, fmt='d', cmap="viridis", linewidths=.5, ax=ax)
    ax.set_title(f'Mapa de Calor: Cruce entre {var_x} y {var_y}', fontsize=14)
    ax.set_xlabel(var_y, fontsize=12)
    ax.set_ylabel(var_x, fontsize=12)
    st.pyplot(fig)

def create_categorical_bubble_chart(df_agg, x_col, y_col, size_col, color_col, title, mapa_valores_color):
    """Crea un gráfico de burbujas categórico."""
    if df_agg is None or df_agg.empty:
        return None
    mapa_inverso = {v: k for k, v in mapa_valores_color.items()}
    min_val, max_val = df_agg[color_col].min(), df_agg[color_col].max()
    fig = px.scatter(
        df_agg, x=x_col, y=y_col, size=size_col, color=color_col,
        hover_name=x_col, size_max=50, title=title,
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={color_col: "Facilidad Promedio", size_col: "Nº de Respuestas"}
    )
    fig.update_layout(
        xaxis_title=x_col, yaxis_title=y_col,
        coloraxis_colorbar=dict(
            title="Facilidad Promedio",
            tickvals=[min_val, max_val],
            ticktext=[f"Más Difícil ({mapa_inverso.get(min_val, '')})", f"Más Fácil ({mapa_inverso.get(max_val, '')})"]
        )
    )
    return fig

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
