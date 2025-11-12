import streamlit as st
import pandas as pd

# --- Configuración de la Página ---
st.set_page_config(layout="wide", page_title="Simulador 1ª Vuelta Presidencial")
st.title("🗳️ Simulador de Escenarios: Primera Vuelta Presidencial")
st.markdown("Basado en el sistema de ponderación normalizada.")

# --- Definición de Candidatos ---
# (Basado en la información que proporcionaste)
CANDIDATOS = [
    "Jeannette Jara",
    "Evelyn Matthei",
    "José Antonio Kast",
    "Johannes Kaiser",
    "Franco Parisi",
    "Marco Enríquez-Ominami",
    "Harold Mayne-Nicholls",
    "Eduardo Artés"
]

# --- Valores por Defecto (Basados en las encuestas que mencionaste) ---
# Usamos estos números como un punto de partida razonable
DEFAULTS = {
    "Jeannette Jara": 30,
    "Evelyn Matthei": 15,
    "José Antonio Kast": 20,
    "Johannes Kaiser": 12,
    "Franco Parisi": 10,
    "Marco Enríquez-Ominami": 4,
    "Harold Mayne-Nicholls": 3,
    "Eduardo Artés": 2
}

# --- Panel Lateral (Sidebar) de Controles ---
st.sidebar.header("Parámetros de Simulación")
st.sidebar.markdown("""
Ajuste la 'intención base' de cada candidato. 
Los porcentajes finales se calcularán automáticamente, normalizados al 100%.
""")

# Slider de Participación
votos_validos_estimados = st.sidebar.slider(
    "Total de Votos Válidos Estimados",
    min_value=8_000_000,
    max_value=13_000_000,
    value=11_200_000,  # Usamos la base municipal 2024
    step=100_000,
    help="Define el universo total de votantes válidos esperados."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Ajuste de Intención de Voto")

# Diccionario para guardar los valores de intención
intencion = {}
for candidato in CANDIDATOS:
    intencion[candidato] = st.sidebar.slider(
        candidato,
        min_value=0,
        max_value=100,
        value=DEFAULTS.get(candidato, 5)
    )

# --- Cálculo de Resultados ---
total_intencion = sum(intencion.values())

resultados = []
if total_intencion > 0:
    for candidato, valor in intencion.items():
        # Lógica de Normalización
        porcentaje = (valor / total_intencion) * 100
        votos = (porcentaje / 100) * votos_validos_estimados

        resultados.append({
            "Candidato": candidato,
            "Intención Base": valor,
            "Porcentaje (%)": porcentaje,
            "Votos Estimados": votos
        })
else:
    # Caso por si todos los sliders están en 0
    for candidato in CANDIDATOS:
        resultados.append({
            "Candidato": candidato,
            "Intención Base": 0,
            "Porcentaje (%)": 0.0,
            "Votos Estimados": 0.0
        })

# --- Visualización de Resultados ---
st.header("📊 Resultados de la Simulación")

if total_intencion > 0:
    # Convertir a DataFrame y ordenar
    df_resultados = pd.DataFrame(resultados).sort_values(by="Porcentaje (%)", ascending=False).reset_index(drop=True)

    # --- Métricas para los 2 primeros (Paso a Balotaje) ---
    st.subheader("Definición de Segunda Vuelta")

    col1, col2 = st.columns(2)
    # Primer Lugar
    c1_nombre = df_resultados.iloc[0]["Candidato"]
    c1_pct = df_resultados.iloc[0]["Porcentaje (%)"]
    c1_votos = df_resultados.iloc[0]["Votos Estimados"]
    col1.metric(
        label="1er Lugar (Pasa a Balotaje)",
        value=c1_nombre,
        delta=f"{c1_pct:.1f}% ({c1_votos:,.0f} votos)"
    )

    # Segundo Lugar
    c2_nombre = df_resultados.iloc[1]["Candidato"]
    c2_pct = df_resultados.iloc[1]["Porcentaje (%)"]
    c2_votos = df_resultados.iloc[1]["Votos Estimados"]
    col2.metric(
        label="2do Lugar (Pasa a Balotaje)",
        value=c2_nombre,
        delta=f"{c2_pct:.1f}% ({c2_votos:,.0f} votos)"
    )

    st.markdown("---")

    # --- Gráfico de Barras ---
    st.subheader("Distribución Porcentual del Voto")
    st.bar_chart(df_resultados.set_index("Candidato")["Porcentaje (%)"])

    # --- Tabla Detallada ---
    with st.expander("Ver tabla detallada de votos"):
        st.dataframe(
            df_resultados.style.format({
                "Porcentaje (%)": "{:.1f}%",
                "Votos Estimados": "{:,.0f}",
                "Intención Base": "{:d}"
            }),
            use_container_width=True
        )

else:
    st.error("Mueva al menos un slider de 'Intención de Voto' por encima de 0 para ver los resultados.")