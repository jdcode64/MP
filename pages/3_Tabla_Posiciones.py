import streamlit as st
import pandas as pd
from services.scoring_service import get_leaderboard_data

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Debes iniciar sesión para ver esta página.")
    st.stop()

st.title("Tabla de Posiciones")

leaderboard = get_leaderboard_data()

if not leaderboard:
    st.info("Aún no hay puntos registrados.")
else:
    # Build dataframe for better display
    df_data = []
    for idx, row in enumerate(leaderboard):
        df_data.append({
            "Posición": idx + 1,
            "Nombre": row['name'],
            "Total Puntos": row['total_points'],
            "Marcadores Exactos": row['exact_scores'],
            "Ganadores Acertados": row['winners'],
            "Puntos Combinadas": row['combined']
        })

    df = pd.DataFrame(df_data)
    # Hide index for cleaner UI
    st.dataframe(df, use_container_width=True, hide_index=True)
