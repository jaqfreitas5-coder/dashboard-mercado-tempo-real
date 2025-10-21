cat > README.md << 'EOF'
# Dashboard de Mercado em Tempo Real

Sistema completo de análise financeira com dashboard interativo em tempo real. 
Desenvolvido em Python com arquitetura full-stack.

## Funcionalidades

- Analise Tecnica Avancada - RSI, MACD, Bollinger Bands e mais indicadores
- Dashboard Interativo - Visualizacoes em tempo real com graficos dinamicos
- API REST Completa - Backend robusto com FastAPI e documentacao automatica
- Previsoes com Machine Learning - Modelos preditivos para tendencias de mercado
- Interface Moderna - Frontend responsivo com Streamlit
- Dados em Tempo Real - Integracao com Yahoo Finance API

## Tecnologias

**Backend:** Python, FastAPI, Pandas, NumPy, TA-Lib, yFinance
**Frontend:** Streamlit, Plotly, HTML/CSS
**Analise de Dados:** Scikit-learn, Statistics, Technical Analysis
**Ferramentas:** Git, GitHub, Virtual Environment

## Estrutura do Projeto

dashboard-mercado-tempo-real/
├── backend/
│ ├── main.py # API FastAPI principal
│ ├── technical_analysis.py # Analise tecnica avancada
│ └── main_custom.py # Configuracoes customizadas
├── frontend/
│ ├── app.py # Aplicacao Streamlit principal
│ ├── tech_analysis_page.py # Pagina de analise tecnica
│ └── app_custom.py # Configuracoes de UI
├── requirements.txt # Dependencias do projeto
└── README.md # Documentacao

Execucao
Backend (API)
cd backend
python main.py
Acesse: http://localhost:8000/docs

Frontend (Dashboard)

cd frontend
streamlit run app.py
Acesse: http://localhost:8501

API Endpoints
GET /api/tech-analysis/{symbol} - Analise tecnica completa

GET /api/market-analysis - Analise geral do mercado

GET /api/company-insights/{symbol} - Insights da empresa

GET /api/social-intelligence - Analise de sentiment

WS /ws - WebSocket para dados em tempo real

# Exemplo de chamada para analise tecnica
import requests
response = requests.get("http://localhost:8000/api/tech-analysis/AAPL")
data = response.json()
Desenvolvimento
Para contribuir com o projeto:

Fork o repositorio

Crie uma branch para sua feature

Commit suas mudancas

Push para a branch

Abra um Pull Request

Licenca
Este projeto e open source e esta sob a licenca MIT.

Contato
Desenvolvido por Jaqueline Freitas - 17-982055602


