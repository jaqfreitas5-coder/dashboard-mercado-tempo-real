
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import json

st.set_page_config(
    page_title="Market Intelligence Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #2E86AB, #A23B72, #F18F01, #C73E1D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .metric-card {
        background: rgba(46, 134, 171, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(46, 134, 171, 0.3);
        backdrop-filter: blur(10px);
    }
    .stAlert {
        border-radius: 10px;
    }
    .positive-trend {
        color: #2E86AB;
        font-weight: bold;
    }
    .negative-trend {
        color: #C73E1D;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E86AB 0%, #1A535C 100%);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📊 Market Intelligence Pro</h1>', unsafe_allow_html=True)
st.markdown("### Plataforma Avançada de Análise de Mercado e Previsões")

st.sidebar.title("🧭 Navegação")
page = st.sidebar.selectbox(
    "Menu Principal:",
    ["📈 Dashboard", "🔮 Análise Preditiva", "⚡ Mercado Ao Vivo", "💼 Meu Portfolio", "🏢 Análise de Empresas"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Desenvolvido por")
st.sidebar.markdown("**Seu Nome Aqui**")
st.sidebar.markdown("Analista de Dados & Desenvolvedor")
st.sidebar.markdown("📧 seu.email@provedor.com")
st.sidebar.markdown("🔗 [Seu LinkedIn](https://linkedin.com/in/seu-perfil)")

