# Importaciones comunes para facilitar el acceso desde otros módulos
from .data_manager import GestorDatos, DashboardStock, AsistenteTech
from .styles import cargar_estilos, crear_header, crear_sidebar
from .utils import verificar_admin, inicializar_session

# Opcional: Configuraciones iniciales
def inicializar_app():
    """
    Función para inicializar configuraciones comunes de la aplicación.
    """
    import streamlit as st
    st.set_page_config(
        page_title="Makers Tech Assistant",
        page_icon="🤖",
        layout="wide"
    )