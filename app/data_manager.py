import json
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List
import google.generativeai as genai
import streamlit as st

"""
Main module. include adata manager, 
stock dashboard y AI assistant.
"""

# gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
modelo = genai.GenerativeModel('gemini-1.5-pro-latest')

class GestorDatos:
    """Class to manage loading and storage of JSON data"""

    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir # directory containing data files
        # Main data structure
        self.datos = {'productos': [], 'servicios': {}, 'politicas': {}}
        self.cargar_datos() # data load

    def cargar_archivo_json(self, ruta: str) -> Dict:
        """Load a JSON file with error handling"""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {ruta}: {str(e)}")
            return {}

    def cargar_datos(self):
        """Load all JSON files from data directory"""
        if os.path.exists(self.data_dir):
            for archivo in os.listdir(self.data_dir):
                if archivo.endswith('.json'):
                    ruta = os.path.join(self.data_dir, archivo)
                    datos = self.cargar_archivo_json(ruta)
                    # process product files
                    if 'productos' in datos:
                        categoria = datos.get('categoria', 'Sin categoría')
                        # add category to each product
                        productos_con_categoria = [{
                            **producto, 
                            'categoria': categoria
                        } for producto in datos['productos']]
                        self.datos['productos'].extend(productos_con_categoria)
                        # process service/policy files
                    elif archivo in ['servicios.json', 'politicas.json']:
                        self.datos[archivo.split('.')[0]] = datos

class DashboardStock:
    """Class to generate stock visualizations"""

    def __init__(self, productos: list):
        self.productos = productos
        self.df = self._crear_dataframe() # main analysis dataframe

    def _crear_dataframe(self) -> pd.DataFrame:
        """Create structured DataFrame from product data"""
        datos = []
        for p in self.productos:
            try:
                # Process stock and price data
                stock = p['stock']
                precio = p['precio']
                
                stock_tienda = int(stock.get('tienda', 0)) if isinstance(stock.get('tienda', 0), (int, float)) else 0
                stock_almacen = int(stock.get('almacen', 0)) if isinstance(stock.get('almacen', 0), (int, float)) else 0
                
                if isinstance(precio, dict):
                    precio = float(precio.get('valor', 0.0))
                else:
                    precio = float(str(precio).replace('$', '').replace(',', ''))

                # build record
                datos.append({
                    'ID': p.get('id', 'N/A'),
                    'Categoria': p.get('categoria', 'Sin categoria'),
                    'Marca': p.get('marca', 'Sin marca'),
                    'Modelo': p.get('modelo', 'Sin modelo'),
                    'Stock Tienda': stock_tienda,
                    'Stock Almacén': stock_almacen,
                    'Stock Total': stock_tienda + stock_almacen,
                    'Precio': precio
                })
            except Exception as e:
                print(f"Error procesando producto: {str(e)}")
                continue
        
        # create and clean DataFrame

        df = pd.DataFrame(datos)
        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce').fillna(0)
        df['Stock Total'] = pd.to_numeric(df['Stock Total'], errors='coerce').fillna(0)
        return df

    def mostrar_metricas_principales(self):
        """Display key stock metrics"""
        df_valido = self.df[(self.df['Precio'] > 0) & (self.df['Stock Total'] >= 0)]
        valor_total = (df_valido['Stock Total'] * df_valido['Precio']).sum()
        
        # three-column layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Productos con Stock", f"{len(df_valido)}", ">5 unidades")
        with col2:
            bajo_stock = df_valido[df_valido['Stock Tienda'] < 5].shape[0]
            st.metric("Productos Bajo Stock", bajo_stock, "(<5 unidades)")
        with col3:
            st.metric("Valor Total Stock", f"${valor_total:,.2f}")

    def mostrar_distribucion_stock(self):
        tab1, tab2, tab3 = st.tabs(["Por Categoría", "Por Marca", "Detallado"])
        
        with tab1:
            # category pie chart
            fig = px.pie(self.df, names='Categoria', values='Stock Total', 
                        title='Distribución de Stock por Categoría')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # brand bar chart
            fig = px.bar(self.df.groupby('Marca', as_index=False)['Stock Total'].sum(),
                        x='Marca', y='Stock Total', color='Marca',
                        title='Stock Total por Marca')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # detailed table
            st.dataframe(self.df.sort_values('Stock Total', ascending=False),
                        column_config={"Precio": st.column_config.NumberColumn(format="$%.2f")})

    def mostrar_alertas_stock(self):
        """Display critical stock alerts"""
        st.subheader("🚨 Alertas de Stock Crítico")
        bajo_stock = self.df[(self.df['Stock Tienda'] < 3) | (self.df['Stock Almacén'] < 5)]
        
        if not bajo_stock.empty:
            for _, row in bajo_stock.iterrows():
                st.warning(f"**{row['Marca']} {row['Modelo']}**\n- Stock Tienda: {row['Stock Tienda']}\n- Stock Almacén: {row['Stock Almacén']}")
        else:
            st.success("✅ Todo el stock está en niveles adecuados")

class AsistenteTech:
    """AI-powered virtual assistant class"""
    def __init__(self):
        self.gestor = GestorDatos() # load data
        self._cargar_contexto() # prepare AI context

    def _cargar_contexto(self):
        """Build initial context for AI model"""
        categorias = set()
        marcas = set()
        
        # extract unique categories and brands 
        for producto in self.gestor.datos['productos']:
            if 'categoria' in producto:
                categorias.add(producto['categoria'])
            if 'marca' in producto:
                marcas.add(producto['marca'])
        
         # context template for AI model
        self.contexto = f"""
        Eres el asistente virtual de Makers Tech. Datos actualizados al {
            datetime.now().strftime('%d/%m/%Y %H:%M')}:

        **Productos Disponibles:**
        - Total: {len(self.gestor.datos['productos'])} productos
        - Categorías: {', '.join(categorias)}
        - Marcas: {', '.join(marcas)}

        **Políticas:**
        - Devoluciones: {self.gestor.datos['politicas'].get('devoluciones', '30 días')}
        - Envíos: {self.gestor.datos['politicas'].get('envios', '3-5 días hábiles')}

        **Instrucciones:**
        1. Respuestas claras y formateadas con emojis
        2. Destacar características técnicas
        3. Verificar stock disponible
        4. Usar Markdown para mejor presentación
        """

    def generar_respuesta(self, consulta: str, historial: list) -> str:
        """Generate response using Gemini model"""
        prompt = f"Historial: {historial}\nConsulta: {consulta}"
        try:
            respuesta = modelo.generate_content([self.contexto, json.dumps(self.gestor.datos, indent=2), prompt])
            return respuesta.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"