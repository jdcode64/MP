import streamlit as st
from utils.auth import hash_password, check_password
from repositories.user_repo import get_user_by_username, create_user
from database.connection import init_db

# Initialize database on first run
init_db()

st.set_page_config(page_title="Polla Mundial 2026", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

def login():
    st.title("Polla Mundial 2026 - Iniciar Sesión")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            user = get_user_by_username(username)
            if user and check_password(password, user['password_hash']):
                if user['status'] == 'aprobado':
                    st.session_state.user = user
                    st.rerun()
                elif user['status'] == 'pendiente':
                    st.warning("Tu cuenta está pendiente de aprobación por el administrador.")
                else:
                    st.error("Tu cuenta está inactiva.")
            else:
                st.error("Usuario o contraseña incorrectos.")

def register():
    st.title("Registro de Participantes")
    with st.form("register_form"):
        first_name = st.text_input("Nombre")
        last_name = st.text_input("Apellido")
        username = st.text_input("Usuario")
        email = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")
        password_confirm = st.text_input("Confirmar contraseña", type="password")

        submit = st.form_submit_button("Registrarse")

        if submit:
            if not all([first_name, last_name, username, email, password, password_confirm]):
                st.error("Todos los campos son obligatorios.")
            elif password != password_confirm:
                st.error("Las contraseñas no coinciden.")
            else:
                existing_user = get_user_by_username(username)
                if existing_user:
                    st.error("El usuario ya existe.")
                else:
                    hashed = hash_password(password)
                    try:
                        create_user(first_name, last_name, username, email, hashed)
                        st.success("Registro exitoso. Tu cuenta está pendiente de aprobación.")
                    except Exception as e:
                        st.error(f"Error en el registro: {e}")

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    with tab1:
        login()
    with tab2:
        register()
else:
    st.sidebar.title(f"Bienvenido, {st.session_state.user['first_name']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()

    st.title("Polla Mundial 2026")
    st.write("Selecciona una opción del menú lateral.")

    # Simple navigation structure
    if st.session_state.user['role'] == 'admin':
        st.sidebar.info("Modo Administrador activo")
