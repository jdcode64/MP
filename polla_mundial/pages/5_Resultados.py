import streamlit as st
import pandas as pd
from repositories.match_repo import get_all_matches
from repositories.prediction_repo import get_user_predictions

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Debes iniciar sesión para ver esta página.")
    st.stop()

st.title("Resultados")

matches = {m['id']: m for m in get_all_matches() if m['status'] == 'FINISHED'}
predictions = {p['match_id']: p for p in get_user_predictions(st.session_state.user['id'])}

if not matches:
    st.info("Aún no hay partidos finalizados.")
else:
    for match_id, match in matches.items():
        pred = predictions.get(match_id)

        with st.expander(f"{match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}"):
            if not pred:
                st.write("No registraste pronóstico para este partido.")
            else:
                col1, col2, col3 = st.columns(3)

                col1.metric("Tu Pronóstico", f"{pred['home_score']} - {pred['away_score']}")
                col2.metric("Puntos Exactos", pred['points_exact_score'])
                col3.metric("Puntos Ganador", pred['points_winner'])

                st.write(f"**Total puntos en este partido:** {pred['total_points']}")
                st.write(f"**Puntos por combinadas:** {pred['points_combined']}")

                st.write("### Detalle Combinadas")

                # Mock comparison for demonstration
                # Real logic would depend on the match having full data for combinadas

                df_detail = pd.DataFrame({
                    "Combinada": [
                        "Ganador",
                        "Ambos anotan",
                        "Más de 2.5 goles",
                        "Primer equipo en anotar",
                        "Habrá penal",
                        "Habrá expulsión",
                        "Más tiros de esquina",
                        "Equipo clasificado",
                        "Cómo termina el partido",
                        "Total de goles"
                    ],
                    "Tu Pronóstico": [
                        pred['winner'],
                        "Sí" if pred['both_score'] else "No",
                        "Sí" if pred['over_2_5_goals'] else "No",
                        pred['first_to_score'],
                        "Sí" if pred['has_penalty'] else "No",
                        "Sí" if pred['has_red_card'] else "No",
                        pred['more_corners'],
                        pred['team_qualified'],
                        pred['match_ending'],
                        pred['total_goals_range']
                    ]
                })
                st.table(df_detail)
