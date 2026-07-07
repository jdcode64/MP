import streamlit as st
import pandas as pd
from repositories.user_repo import get_all_users, update_user_status
from repositories.config_repo import get_scoring_config, update_scoring_config
from services.sync_service import sync_matches_to_db
from services.scoring_service import calculate_prediction_points

if "user" not in st.session_state or st.session_state.user is None or st.session_state.user['role'] != 'admin':
    st.warning("Acceso denegado. Se requieren permisos de administrador.")
    st.stop()

st.title("Panel de Administrador")

tab1, tab2, tab3 = st.tabs(["Usuarios", "Sincronización", "Configuración"])

with tab1:
    st.header("Administrar Usuarios")
    users = get_all_users()

    if not users:
        st.write("No hay usuarios.")
    else:
        for u in users:
            if u['username'] == 'admin':
                continue # Skip admin

            with st.expander(f"{u['first_name']} {u['last_name']} - {u['username']} ({u['status']})"):
                col1, col2, col3 = st.columns(3)
                if col1.button("Aprobar", key=f"approve_{u['id']}"):
                    update_user_status(u['id'], 'aprobado')
                    st.success(f"Usuario {u['username']} aprobado.")
                    st.rerun()
                if col2.button("Desactivar", key=f"deactivate_{u['id']}"):
                    update_user_status(u['id'], 'inactivo')
                    st.warning(f"Usuario {u['username']} desactivado.")
                    st.rerun()

with tab2:
    st.header("Sincronización con API")
    if st.button("Forzar Sincronización"):
        with st.spinner("Sincronizando partidos..."):
            updated, ms, api_used = sync_matches_to_db()
            st.success(f"Sincronización completada desde {api_used}. {updated} partidos actualizados en {ms} ms.")

    if st.button("Recalcular Puntos"):
        with st.spinner("Calculando puntos..."):
            calculate_prediction_points()
            st.success("Puntos recalculados exitosamente.")

with tab3:
    st.header("Configuración de Puntajes")
    configs = get_scoring_config()

    with st.form("config_form"):
        pts_exact = st.number_input("Puntos por marcador exacto", min_value=0, value=int(configs.get('points_exact_score', 5)))
        pts_winner = st.number_input("Puntos por ganador", min_value=0, value=int(configs.get('points_winner', 2)))
        pts_combined = st.number_input("Puntos por cada combinada", min_value=0, value=int(configs.get('points_combined', 1)))

        if st.form_submit_button("Guardar Configuración"):
            update_scoring_config({
                'points_exact_score': pts_exact,
                'points_winner': pts_winner,
                'points_combined': pts_combined
            })
            st.success("Configuración actualizada.")
            st.rerun()
