import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importar a página de análise técnica simplificada
from tech_analysis_simple import show_technical_analysis

# Configuração da página
st.set_page_config(
    page_title="Dashboard Mercado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funções das páginas
def show_home():
    st.title("🏠 Dashboard de Mercado em Tempo Real")
    st.markdown("""
    ## Sistema completo de análise financeira
    
    **✨ Funcionalidades:**
    - 📊 **Análise Técnica** - Indicadores e sinais de trading
    - 📈 **Gráficos Interativos** - Visualização em tempo real
    - 🔍 **Dados de Mercado** - Análise de ações e tendências
    
    **🚀 Comece escolhendo uma página no menu lateral!**
    """)
    
    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Ações Analisadas", "50+")
    with col2:
        st.metric("🌎 Mercados", "Brasil & EUA")
    with col3:
        st.metric("⏰ Atualizado", "Agora")

def show_dashboard():
    st.title("📊 Dashboard Interativo")
    st.markdown("Visualização de dados de mercado")
    
    # Dados simulados do dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance")
        data = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
            'IBOV': [100, 105, 102, 110, 108]
        })
        st.line_chart(data.set_index('Mês'))
    
    with col2:
        st.subheader("🎯 Setores")
        setores = pd.DataFrame({
            'Setor': ['Financeiro', 'Energia', 'Tecnologia', 'Varejo'],
            'Performance': [12, 8, 15, 5]
        })
        st.bar_chart(setores.set_index('Setor'))

# Menu de navegação
def main():
    st.sidebar.title("🎯 Navegação")
    
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        ["🏠 Página Inicial", "📊 Dashboard", "🔍 Análise Técnica"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Dashboard Mercado** v1.0
    *Sistema de análise técnica*
    """)
    
    if page == "🏠 Página Inicial":
        show_home()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "🔍 Análise Técnica":
        show_technical_analysis()

if __name__ == "__main__":
    main()
