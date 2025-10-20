import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def show_technical_analysis():
    """Página completa de Análise Técnica"""
    
    st.header("📊 Análise Técnica Profissional")
    st.markdown("Análise técnica em tempo real com indicadores profissionais")
    
    # Input do usuário
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        symbol = st.text_input(
            "**🔍 Digite o símbolo da ação:**", 
            "AAPL",
            placeholder="Ex: AAPL, TSLA, MSFT, PETR4.SA"
        ).upper()
    
    with col2:
        analyze_btn = st.button("🚀 Analisar", use_container_width=True)
    
    with col3:
        if st.button("🔄 Limpar", use_container_width=True):
            st.rerun()
    
    if analyze_btn and symbol:
        analyze_stock(symbol)
    elif symbol and len(symbol) > 1:
        # Analisa automaticamente após digitar
        analyze_stock(symbol)

def analyze_stock(symbol):
    """Faz a análise da ação"""
    with st.spinner(f"📈 Analisando {symbol}..."):
        try:
            response = requests.get(f"http://localhost:8000/api/tech-analysis/{symbol}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    display_analysis_results(data)
                else:
                    st.error(f"❌ Erro: {data.get('error', 'Erro desconhecido')}")
            else:
                st.error("🔌 Erro ao conectar com o servidor")
                
        except requests.exceptions.ConnectionError:
            st.error("🚫 Servidor offline - Verifique se o backend está rodando")
        except Exception as e:
            st.error(f"💥 Erro inesperado: {e}")

def display_analysis_results(data):
    """Exibe os resultados da análise"""
    symbol = data['symbol']
    indicators = data['indicators']
    signals = data['signals']
    
    # ===== CABEÇALHO COM MÉTRICAS =====
    st.subheader(f"📈 {symbol} - Análise Técnica")
    
    # Linha 1: Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        price = indicators['current_price']
        st.metric(
            label="💵 Preço Atual", 
            value=f"${price}",
            delta=None
        )
    
    with col2:
        signal = signals['overall_signal']
        if signal == "COMPRA":
            st.metric("🎯 Sinal", "COMPRA", delta_color="off")
            st.success("**🟢 OPORTUNIDADE**")
        elif signal == "VENDA":
            st.metric("🎯 Sinal", "VENDA", delta_color="off") 
            st.error("**🔴 CUIDADO**")
        else:
            st.metric("🎯 Sinal", "NEUTRO", delta_color="off")
            st.info("**⚪ AGUARDAR**")
    
    with col3:
        rsi = indicators['rsi']
        if rsi < 30:
            st.metric("📊 RSI", f"{rsi}", "Sobrevendido", delta_color="inverse")
        elif rsi > 70:
            st.metric("📊 RSI", f"{rsi}", "Sobrecomprado", delta_color="inverse")
        else:
            st.metric("📊 RSI", f"{rsi}", "Neutro")
    
    with col4:
        macd = indicators['macd']
        st.metric("🔄 MACD", f"{macd:.4f}")
    
    # ===== GRÁFICOS SIMULADOS =====
    st.subheader("📊 Visualização dos Indicadores")
    
    # Abas para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["📈 Preço & Tendência", "🎯 Momentum", "📋 Resumo"])
    
    with tab1:
        display_price_chart(symbol, indicators)
    
    with tab2:
        display_momentum_indicators(indicators)
    
    with tab3:
        display_summary(symbol, indicators, signals)
    
    # ===== SINAIS DETALHADOS =====
    st.subheader("🔍 Sinais Detalhados por Indicador")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📡 Sinais de Trading:**")
        for signal_name, signal_value in signals.items():
            if signal_name != 'overall_signal':
                display_signal(signal_name, signal_value)
    
    with col2:
        st.write("**📈 Valores dos Indicadores:**")
        display_indicator_values(indicators)
    
    # ===== INTERPRETAÇÃO =====
    st.subheader("💡 Interpretação e Recomendação")
    display_interpretation(signals, indicators)

def display_price_chart(symbol, indicators):
    """Gráfico de preço simulado"""
    # Gerar dados simulados
    dates = pd.date_range(end=datetime.now(), periods=50, freq='D')
    base_price = indicators['current_price']
    
    # Simular variação de preço
    np.random.seed(42)  # Para resultados consistentes
    returns = np.random.normal(0, 0.02, 50)
    prices = base_price * (1 + returns).cumprod()
    
    fig = go.Figure()
    
    # Linha de preço
    fig.add_trace(go.Scatter(
        x=dates, y=prices,
        mode='lines',
        name='Preço',
        line=dict(color='#2E86AB', width=3)
    ))
    
    # Médias móveis simuladas
    sma = pd.Series(prices).rolling(20).mean()
    ema = pd.Series(prices).ewm(span=20).mean()
    
    fig.add_trace(go.Scatter(
        x=dates, y=sma, 
        mode='lines', 
        name='SMA 20',
        line=dict(color='#F18F01', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=ema,
        mode='lines',
        name='EMA 20', 
        line=dict(color='#A23B72', width=2, dash='dot')
    ))
    
    fig.update_layout(
        title=f"{symbol} - Preço e Médias Móveis (Simulado)",
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_momentum_indicators(indicators):
    """Gráficos de momentum"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico RSI
        rsi_value = indicators['rsi']
        fig_rsi = go.Figure()
        
        fig_rsi.add_trace(go.Indicator(
            mode="gauge+number",
            value=rsi_value,
            title={'text': "RSI (14)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': rsi_value
                }
            }
        ))
        
        fig_rsi.update_layout(height=300)
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col2:
        # Gráfico MACD
        macd = indicators['macd']
        macd_signal = indicators['macd_signal']
        
        st.write("**🔄 MACD:**")
        st.metric("MACD Line", f"{macd:.4f}")
        st.metric("Signal Line", f"{macd_signal:.4f}")
        
        if macd > macd_signal:
            st.success("📈 MACD acima da linha de sinal - **Momentum positivo**")
        else:
            st.warning("📉 MACD abaixo da linha de sinal - **Momentum negativo**")

def display_summary(symbol, indicators, signals):
    """Resumo da análise"""
    st.write(f"**📋 Resumo da Análise - {symbol}**")
    
    summary_data = {
        'Indicador': ['Preço', 'SMA 20', 'EMA 20', 'RSI', 'MACD', 'Bollinger Upper', 'Bollinger Lower'],
        'Valor': [
            f"${indicators['current_price']}",
            f"${indicators['sma_20']}",
            f"${indicators['ema_20']}", 
            f"{indicators['rsi']}",
            f"{indicators['macd']:.4f}",
            f"${indicators['bb_upper']}",
            f"${indicators['bb_lower']}"
        ],
        'Status': [
            get_price_status(indicators),
            get_sma_status(indicators),
            get_ema_status(indicators),
            get_rsi_status(indicators['rsi']),
            get_macd_status(indicators['macd']),
            "Resistência",
            "Suporte"
        ]
    }
    
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_signal(signal_name, signal_value):
    """Exibe um sinal individual"""
    signal_display = {
        'rsi_signal': '📊 RSI',
        'macd_signal': '🔄 MACD', 
        'trend_signal': '📈 Tendência'
    }
    
    icon = "✅" if signal_value == "COMPRA" else "❌" if signal_value == "VENDA" else "➖"
    name = signal_display.get(signal_name, signal_name.replace('_', ' ').title())
    
    st.write(f"{icon} **{name}:** {signal_value}")

def display_indicator_values(indicators):
    """Exibe valores dos indicadores"""
    st.write(f"• **💵 Preço:** ${indicators['current_price']}")
    st.write(f"• **📊 SMA 20:** ${indicators['sma_20']}")
    st.write(f"• **📈 EMA 20:** ${indicators['ema_20']}")
    st.write(f"• **🎯 RSI:** {indicators['rsi']}")
    st.write(f"• **🔄 MACD:** {indicators['macd']:.4f}")
    st.write(f"• **📏 Bollinger Upper:** ${indicators['bb_upper']}")
    st.write(f"• **📐 Bollinger Lower:** ${indicators['bb_lower']}")

def display_interpretation(signals, indicators):
    """Exibe interpretação final"""
    overall_signal = signals['overall_signal']
    rsi = indicators['rsi']
    
    if overall_signal == "COMPRA":
        st.success("""
        **🎯 RECOMENDAÇÃO: COMPRA**
        
        📈 **Fundamentação:**
        - Múltiplos indicadores sugerem oportunidade de compra
        - Momentum positivo identificado
        - Condições técnicas favoráveis
        
        💡 **Sugestão:** Considerar entrada com gestão de risco adequada
        """)
    elif overall_signal == "VENDA":
        st.error("""
        **🎯 RECOMENDAÇÃO: VENDA/CAUTELA**
        
        📉 **Fundamentação:**
        - Indicadores sugerem pressão vendedora
        - Momentum negativo predominante
        - Condições técnicas desfavoráveis
        
        💡 **Sugestão:** Considerar proteção ou redução de posição
        """)
    else:
        st.info("""
        **🎯 RECOMENDAÇÃO: NEUTRO**
        
        ⚖️ **Fundamentação:**
        - Indicadores em equilíbrio
        - Mercado sem direção definida
        - Condições técnicas neutras
        
        💡 **Sugestão:** Aguardar confirmação de tendência
        """)

# Funções auxiliares para status
def get_price_status(indicators):
    price = indicators['current_price']
    sma = indicators['sma_20']
    return "Acima da SMA" if price > sma else "Abaixo da SMA"

def get_sma_status(indicators):
    price = indicators['current_price']
    sma = indicators['sma_20']
    return "Suporte" if price > sma else "Resistência"

def get_ema_status(indicators):
    price = indicators['current_price']
    ema = indicators['ema_20']
    return "Tendência Alta" if price > ema else "Tendência Baixa"

def get_rsi_status(rsi):
    if rsi < 30:
        return "Sobrevendido"
    elif rsi > 70:
        return "Sobrecomprado"
    else:
        return "Neutro"

def get_macd_status(macd):
    return "Positivo" if macd > 0 else "Negativo"

# Para testar a página diretamente
if __name__ == "__main__":
    show_technical_analysis()