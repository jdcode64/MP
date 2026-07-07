import streamlit as st
from datetime import timedelta
from datetime import timezone
from repositories.match_repo import get_all_matches
from repositories.prediction_repo import save_prediction, get_user_predictions
from utils.time_utils import get_current_bogota_time, to_bogota_time

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Debes iniciar sesión para ver esta página.")
    st.stop()

st.title("Mis Pronósticos")

matches = get_all_matches()
user_predictions = {p['match_id']: p for p in get_user_predictions(st.session_state.user['id'])}
current_time = get_current_bogota_time()

for match in matches:
    match_time_utc = match['match_date']
    if match_time_utc.tzinfo is None:
        match_time_utc = match_time_utc.replace(tzinfo=timezone.utc)

    match_time_bog = to_bogota_time(match_time_utc)
    lock_time = match_time_bog - timedelta(hours=1)

    is_locked = current_time >= lock_time

    with st.expander(f"{match['home_team']} vs {match['away_team']} - {match_time_bog.strftime('%Y-%m-%d %H:%M')}"):
        if is_locked:
            st.error("Pronóstico cerrado.")
            pred = user_predictions.get(match['id'])
            if pred:
                st.write(f"Tu pronóstico: {pred['home_score']} - {pred['away_score']}")
            else:
                st.write("No registraste pronóstico para este partido.")
        else:
            pred = user_predictions.get(match['id'], {})

            with st.form(f"pred_form_{match['id']}"):
                col1, col2 = st.columns(2)
                home_score = col1.number_input(f"Goles {match['home_team']}", min_value=0, value=pred.get('home_score', 0))
                away_score = col2.number_input(f"Goles {match['away_team']}", min_value=0, value=pred.get('away_score', 0))

                st.write("Combinadas obligatorias:")

                # Mapping dicts
                winner_options = {"HOME_TEAM": "Local", "DRAW": "Empate", "AWAY_TEAM": "Visitante"}
                winner_keys = list(winner_options.keys())
                winner_labels = list(winner_options.values())

                first_options = {"HOME_TEAM": "Local", "AWAY_TEAM": "Visitante", "NONE": "Ninguno"}
                first_keys = list(first_options.keys())
                first_labels = list(first_options.values())

                corners_options = {"HOME_TEAM": "Local", "DRAW": "Empate", "AWAY_TEAM": "Visitante"}
                corners_keys = list(corners_options.keys())
                corners_labels = list(corners_options.values())

                # Assuming Equipo A = Local, Equipo B = Visitante
                qualified_options = {"HOME_TEAM": "Equipo A", "AWAY_TEAM": "Equipo B"}
                qualified_keys = list(qualified_options.keys())
                qualified_labels = list(qualified_options.values())

                ending_options = {"REGULAR": "90 minutos", "EXTRA_TIME": "Tiempo extra", "PENALTIES": "Penales"}
                ending_keys = list(ending_options.keys())
                ending_labels = list(ending_options.values())

                goals_options = {"0-1": "0-1", "2-3": "2-3", "4_PLUS": "4 o más"}
                goals_keys = list(goals_options.keys())
                goals_labels = list(goals_options.values())

                winner_val = st.selectbox("1. Ganador", winner_labels, index=winner_keys.index(pred.get('winner', 'HOME_TEAM')))
                both_score = st.selectbox("2. Ambos anotan", ["Sí", "No"], index=0 if pred.get('both_score', True) else 1)
                over_2_5 = st.selectbox("3. Más de 2.5 goles", ["Sí", "No"], index=0 if pred.get('over_2_5_goals', False) else 1)
                first_to_score_val = st.selectbox("4. Primer equipo en anotar", first_labels, index=first_keys.index(pred.get('first_to_score', 'NONE')))
                has_penalty = st.selectbox("5. Habrá penal", ["Sí", "No"], index=0 if pred.get('has_penalty', False) else 1)
                has_red = st.selectbox("6. Habrá expulsión", ["Sí", "No"], index=0 if pred.get('has_red_card', False) else 1)
                more_corners_val = st.selectbox("7. Más tiros de esquina", corners_labels, index=corners_keys.index(pred.get('more_corners', 'DRAW')))
                team_qualified_val = st.selectbox("8. Equipo clasificado", qualified_labels, index=qualified_keys.index(pred.get('team_qualified', 'HOME_TEAM')))
                match_ending_val = st.selectbox("9. Cómo termina el partido", ending_labels, index=ending_keys.index(pred.get('match_ending', 'REGULAR')))
                total_goals_val = st.selectbox("10. Total de goles", goals_labels, index=goals_keys.index(pred.get('total_goals_range', '0-1')))

                submit = st.form_submit_button("Guardar Pronóstico")
                if submit:
                    try:
                        save_prediction({
                            'user_id': st.session_state.user['id'],
                            'match_id': match['id'],
                            'home_score': home_score,
                            'away_score': away_score,
                            'winner': winner_keys[winner_labels.index(winner_val)],
                            'both_score': both_score == "Sí",
                            'over_2_5_goals': over_2_5 == "Sí",
                            'first_to_score': first_keys[first_labels.index(first_to_score_val)],
                            'has_penalty': has_penalty == "Sí",
                            'has_red_card': has_red == "Sí",
                            'more_corners': corners_keys[corners_labels.index(more_corners_val)],
                            'team_qualified': qualified_keys[qualified_labels.index(team_qualified_val)],
                            'match_ending': ending_keys[ending_labels.index(match_ending_val)],
                            'total_goals_range': goals_keys[goals_labels.index(total_goals_val)]
                        })
                        st.success("Pronóstico guardado exitosamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
