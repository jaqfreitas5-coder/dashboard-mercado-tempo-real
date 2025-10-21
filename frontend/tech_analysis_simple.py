import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def show_technical_analysis():
    """Página simplificada de Análise Técnica compatível com backend atual"""
    
    st.header("📊 Análise Técnica")
    st.markdown("Sistema de análise técnica com dados em tempo real")
    
    # Input do usuário
    col1, col2 = st.columns([3, 1])
    
    with col1:
        symbol = st.text_input(
            "**🔍 Digite o símbolo da ação:**", 
            "PETR4.SA",
            placeholder="Ex: PETR4.SA, VALE3.SA, AAPL, TSLA"
        ).upper()
    
    with col2:
        analyze_btn = st.button("🚀 Analisar", use_container_width=True)
    
    if analyze_btn and symbol:
        analyze_stock(symbol)
    elif symbol and len(symbol) > 1:
        analyze_stock(symbol)

def analyze_stock(symbol):
    """Faz a análise da ação"""
    with st.spinner(f"📈 Analisando {symbol}..."):
        try:
            response = requests.get(f"https://dashboard-mercado-tempo-real-production.up.railway.app/api/tech-analysis/{symbol}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    display_analysis_results(data)
                else:
                    st.error(f"❌ {data.get('error', 'Erro desconhecido')}")
            else:
                st.error("🔌 Erro ao conectar com o servidor")
                
        except requests.exceptions.ConnectionError:
            st.error("🚫 Servidor offline")
        except Exception as e:
            st.error(f"💥 Erro: {e}")

def display_analysis_results(data):
    """Exibe os resultados da análise"""
    symbol = data['symbol']
    indicators = data['indicators']
    signals = data['signals']
    is_simulated = data.get('simulated', False)
    
    # Aviso se são dados simulados
    if is_simulated:
        st.info("📊 **Dados de demonstração** - Sistema funcionando com dados simulados")
    
    st.subheader(f"📈 {symbol} - Análise Técnica")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        price = indicators['current_price']
        st.metric("💵 Preço Atual", f"R$ {price}")
    
    with col2:
        signal = signals['overall_signal']
        color = "green" if signal == "COMPRA" else "red" if signal == "VENDA" else "gray"
        st.metric("🎯 Sinal", signal, delta_color="off")
    
    with col3:
        rsi = indicators['rsi']
        st.metric("📊 RSI", f"{rsi}")
    
    # Gráfico de preço simulado
    display_price_chart(symbol, indicators)
    
    # Sinais detalhados
    st.subheader("🔍 Sinais de Trading")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Indicadores:**")
        st.write(f"• **Preço:** R$ {indicators['current_price']}")
        st.write(f"• **SMA 20:** R$ {indicators['sma_20']}")
        st.write(f"• **RSI:** {indicators['rsi']}")
    
    with col2:
        st.write("**Sinais:**")
        for signal_name, signal_value in signals.items():
            icon = "✅" if signal_value == "COMPRA" else "❌" if signal_value == "VENDA" else "➖"
            st.write(f"{icon} {signal_name.replace('_', ' ').title()}: {signal_value}")

def display_price_chart(symbol, indicators):
    """Gráfico de preço simulado"""
    # Gerar dados simulados para o gráfico
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    base_price = indicators['current_price']
    
    # Simular variação de preço
    np.random.seed(42)
    returns = np.random.normal(0, 0.015, 30)
    prices = base_price * (1 + returns).cumprod()
    
    fig = go.Figure()
    
    # Linha de preço
    fig.add_trace(go.Scatter(
        x=dates, y=prices,
        mode='lines',
        name='Preço',
        line=dict(color='#2E86AB', width=3)
    ))
    
    # Média móvel
    sma = pd.Series(prices).rolling(10).mean()
    
    fig.add_trace(go.Scatter(
        x=dates, y=sma, 
        mode='lines', 
        name='SMA 10',
        line=dict(color='#F18F01', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f"{symbol} - Preço e Tendência",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Para testar diretamente
if __name__ == "__main__":
    show_technical_analysis()
