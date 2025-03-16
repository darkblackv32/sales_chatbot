import streamlit as st
import hashlib

# password verification
def verificar_admin(password: str) -> bool:
    if password == st.secrets["admin"]["password"]:
        st.session_state.es_admin = True
        return True
    st.session_state.es_admin = False
    return False

# keep the chaat
def keep_session():
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'asistente' not in st.session_state:
        from app.data_manager import AsistenteTech
        st.session_state.asistente = AsistenteTech()