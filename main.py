import streamlit as st
from app.data_manager import DashboardStock
from app.styles import cargar_estilos, crear_header, crear_sidebar
from app.utils import verificar_admin, inicializar_session

# Configuración de la página
st.set_page_config(
    page_title="Makers Tech Assistant",
    page_icon="🤖",
    layout="wide"
)

def main():
    # Cargar estilos y header
    st.markdown(cargar_estilos(), unsafe_allow_html=True)
    st.markdown(crear_header(), unsafe_allow_html=True)
    
    # Inicializar sesión
    inicializar_session()
    
    # Sidebar
    crear_sidebar()
    with st.sidebar:
        admin_pass = st.text_input("🔑 Clave de Administrador", type="password")
        verificar_admin(admin_pass)

    # Panel de control admin (no afecta el chat)
    if st.session_state.get('es_admin'):
        with st.expander("📊 PANEL DE CONTROL - STOCK", expanded=True):
            dash = DashboardStock(st.session_state.asistente.gestor.datos['productos'])
            dash.mostrar_metricas_principales()
            dash.mostrar_distribucion_stock()
            dash.mostrar_alertas_stock()

    # Área de chat (se mantiene intacta)
    chat_container = st.container()
    with chat_container:
        # Mostrar historial de chat
        for mensaje in st.session_state.historial:
            if mensaje['rol'] == 'usuario':
                with st.chat_message("user"):
                    st.markdown(f"**Tú:** {mensaje['contenido']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"{mensaje['contenido']}")

    # Input de chat (funciona independientemente del panel de admin)
    consulta = st.chat_input("Escribe tu consulta aquí...")
    if consulta:
        # Mostrar mensaje del usuario
        with chat_container:
            with st.chat_message("user"):
                st.markdown(f"**Tú:** {consulta}")
        
        # Guardar en el historial
        st.session_state.historial.append({
            'rol': 'usuario',
            'contenido': consulta
        })

        # Generar y mostrar respuesta
        with st.spinner("Analizando..."):
            respuesta = st.session_state.asistente.generar_respuesta(
                consulta, 
                st.session_state.historial[-3:]
            )

        # Mostrar respuesta del asistente
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        
        # Guardar respuesta en el historial
        st.session_state.historial.append({
            'rol': 'asistente',
            'contenido': respuesta
        })

if __name__ == "__main__":
    main()