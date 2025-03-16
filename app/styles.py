import streamlit as st

def cargar_estilos():
    return """
    <style>
        .stChatMessage {
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 8px;
        }
        .stChatMessage.user {
            background-color: #e9f5db;
            text-align: right;
        }
        .stChatMessage.assistant {
            background-color: #f1faee;
            text-align: left;
        }
        .sidebar-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2a9d8f;
            margin-bottom: 15px;
        }
    </style>
    """

def crear_header():
    return """
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <img src="https://cdn-icons-png.flaticon.com/512/190/190708.png" width="150">
        <div style="margin-left: 20px;">
            <h1 style="margin: 0;">Makers Tech Assistant</h1>
            <p style="margin: 0; color: #666;">Listo para responder lo que necesites!</p>
        </div>
    </div>
    """

def crear_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🔍 Accesos Rápidos</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # sidebar blocks
        bloques = [
            {
                "color": "#264653",
                "titulo": "📩 Contacto:",
                "contenido": "soporte@makerstech.com"
            },
            {
                "color": "#e76f51",
                "titulo": "🛒 Tienda:",
                "contenido": "<a href='https://preview--chatbot-for-inventory-buddy.lovable.app/' target='_blank' style='color: white; text-decoration: none;'>Explora nuestros productos</a>"
            },
            {
                "color": "#2a9d8f",
                "titulo": "💬 Comunidad:",
                "contenido": "<a href='https://www.linkedin.com/school/makersfellowship/' target='_blank' style='color: white; text-decoration: none;'>Síguenos en LinkedIn</a>"
            },
            {
                "color": "#f4a261",
                "titulo": "📚 Recursos:",
                "contenido": "<a href='https://www.youtube.com/watch?v=g_yYZmRyhmY' target='_blank' style='color: white; text-decoration: none;'>Prueba del procesador M4</a>"
            }
        ]
        
        for bloque in bloques:
            st.markdown(f"""
            <div style="background: {bloque['color']}; padding: 10px; border-radius: 10px; color: white; text-align: center; margin: 10px 0;">
                <strong>{bloque['titulo']}</strong><br>
                <span style="font-size: 14px;">{bloque['contenido']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="footer" style="text-align: center; color: #666; font-size: 0.9em;">
            © 2025 Makers Tech<br>
        </div>
        """, unsafe_allow_html=True)