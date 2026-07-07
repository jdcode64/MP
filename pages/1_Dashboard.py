import streamlit as st
from repositories.user_repo import get_all_users
from repositories.match_repo import get_all_matches, get_last_sync
from services.scoring_service import get_leaderboard_data

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Debes iniciar sesión para ver esta página.")
    st.stop()

st.title("Dashboard")

users = get_all_users()
matches = get_all_matches()
last_sync = get_last_sync()
leaderboard = get_leaderboard_data()

# Calculate stats
registered_users = len([u for u in users if u['status'] == 'aprobado'])
pending_matches = len([m for m in matches if m['status'] == 'PENDING'])
finished_matches = len([m for m in matches if m['status'] == 'FINISHED'])
sync_time = last_sync['sync_date'] if last_sync else "Nunca"

# Current user stats
current_user_name = f"{st.session_state.user['first_name']} {st.session_state.user['last_name']}"
user_pos = "-"
user_points = 0
for idx, entry in enumerate(leaderboard):
    if entry['name'] == current_user_name:
        user_pos = idx + 1
        user_points = entry['total_points']
        break

# If user not in leaderboard yet
leader_name = leaderboard[0]['name'] if leaderboard else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Usuarios Registrados", registered_users)
col2.metric("Partidos Pendientes", pending_matches)
col3.metric("Partidos Finalizados", finished_matches)

st.write("---")

col4, col5, col6 = st.columns(3)
col4.metric("Líder de la polla", leader_name)
col5.metric("Mi posición", user_pos)
col6.metric("Puntos acumulados", user_points)

st.write("---")
st.info(f"Última sincronización: {sync_time}")
