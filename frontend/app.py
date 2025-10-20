import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importar a página de análise técnica
from tech_analysis_page import show_technical_analysis

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="AI Business Oracle",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== FUNÇÕES DAS OUTRAS PÁGINAS =====

def show_home():
    """Página Inicial"""
    st.title("🏠 AI Business Oracle")
    st.markdown("""
    ## Bem-vindo ao Sistema de Análise Financeira Inteligente!
    
    **✨ Recursos disponíveis:**
    - 📊 **Dashboard Interativo** - Visualização de dados em tempo real
    - 🔍 **Análise Técnica** - Indicadores técnicos profissionais
    - 📈 **Gráficos Personalizados** - Análises avançadas
    - 🔄 **Atualização de Dados** - Informações atualizadas do mercado
    
    **🚀 Comece escolhendo uma página no menu lateral!**
    """)
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Ações Monitoradas", "150+")
    with col2:
        st.metric("🌎 Mercados", "10")
    with col3:
        st.metric("⏰ Atualizado", "Agora")
    with col4:
        st.metric("🎯 Precisão", "95%")

def show_dashboard():
    """Dashboard Interativo"""
    st.title("📊 Dashboard Interativo")
    st.markdown("Visualização completa de dados de mercado")
    
    # Simulação de dados do dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tendência de Mercado")
        # Gráfico simples
        data = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
            'Performance': [100, 112, 105, 120, 118]
        })
        st.line_chart(data.set_index('Mês'))
    
    with col2:
        st.subheader("🎯 Setores")
        setores = pd.DataFrame({
            'Setor': ['Tecnologia', 'Financeiro', 'Energia', 'Saúde'],
            'Crescimento': [15, 8, -2, 12]
        })
        st.bar_chart(setores.set_index('Setor'))

def show_custom_charts():
    """Gráficos Personalizados"""
    st.title("📈 Gráficos Personalizados")
    st.markdown("Crie visualizações customizadas dos dados")
    
    st.info("🔧 **Em desenvolvimento** - Em breve mais funcionalidades!")
    
    # Exemplo simples
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

def show_data_update():
    """Atualização de Dados"""
    st.title("🔄 Atualizar Dados")
    st.markdown("Sincronize e atualize os dados do mercado")
    
    if st.button("🔄 Sincronizar Agora", type="primary"):
        with st.spinner("Sincronizando dados..."):
            # Simulação
            import time
            time.sleep(2)
            st.success("✅ Dados sincronizados com sucesso!")
            
    st.metric("📅 Última Atualização", datetime.now().strftime("%d/%m/%Y %H:%M"))

# ===== MENU DE NAVEGAÇÃO =====

def main():
    """Função principal com menu de navegação"""
    
    # Menu lateral
    st.sidebar.title("🎯 Menu de Navegação")
    
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        [
            "🏠 Página Inicial",
            "📊 Dashboard Interativo", 
            "🔍 Análise Técnica",
            "📈 Gráficos Personalizados",
            "🔄 Atualizar Dados"
        ]
    )
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **AI Business Oracle** v1.0
    *Sistema de análise financeira inteligente*
    """)
    
    # Navegação entre páginas
    if page == "🏠 Página Inicial":
        show_home()
    elif page == "📊 Dashboard Interativo":
        show_dashboard()
    elif page == "🔍 Análise Técnica":
        show_technical_analysis()  # ← CHAMA A PÁGINA IMPORTADA
    elif page == "📈 Gráficos Personalizados":
        show_custom_charts()
    elif page == "🔄 Atualizar Dados":
        show_data_update()

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    main()