import streamlit as st
from app.data_manager import DashboardStock
from app.styles import cargar_estilos, crear_header, crear_sidebar
from app.utils import verificar_admin, keep_session

# page configuration
st.set_page_config(
    page_title="Makers Tech Assistant",
    page_icon="🤖",
    layout="wide"
)

def main():
    # styles and headers
    st.markdown(cargar_estilos(), unsafe_allow_html=True)
    st.markdown(crear_header(), unsafe_allow_html=True)
    
    # keep the active chat (does not imply loggin) 
    keep_session()
    
    # sidebar
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

    # chat area
    chat_container = st.container()
    with chat_container:
        # show past messages
        for mensaje in st.session_state.historial:
            if mensaje['rol'] == 'usuario':
                with st.chat_message("user"):
                    st.markdown(f"**Tú:** {mensaje['contenido']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"{mensaje['contenido']}")

    # chat input (works even you are logged as admin)
    consulta = st.chat_input("Escribe tu consulta aquí...")
    if consulta:
        # show query
        with chat_container:
            with st.chat_message("user"):
                st.markdown(f"**Tú:** {consulta}")
        
        # keep query
        st.session_state.historial.append({
            'rol': 'usuario',
            'contenido': consulta
        })

        # generate and show answer
        with st.spinner("Analizando..."):
            respuesta = st.session_state.asistente.generar_respuesta(
                consulta, 
                st.session_state.historial[-3:]
            )

        # show answer
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        
        # keep answer
        st.session_state.historial.append({
            'rol': 'asistente',
            'contenido': respuesta
        })

if __name__ == "__main__":
    main()