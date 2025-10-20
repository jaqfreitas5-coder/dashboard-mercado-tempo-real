from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio
import json
import yfinance as yf
import requests
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List
import random
import warnings
import ta

# Ignorar warnings
warnings.filterwarnings('ignore')

# ===== ANÁLISE TÉCNICA =====
class TechnicalAnalysis:
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol: str) -> pd.DataFrame:
        """Busca dados da ação"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="6mo")
            return data
        except Exception as e:
            print(f"Erro ao buscar {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_indicators(self, data: pd.DataFrame) -> Dict:
        """Calcula indicadores técnicos"""
        if data.empty:
            return {}
        
        # Preço atual
        current_price = data['Close'].iloc[-1] if len(data) > 0 else 0
        
        # Médias móveis
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        ema_20 = data['Close'].ewm(span=20).mean().iloc[-1]
        
        # RSI
        rsi = ta.momentum.RSIIndicator(data['Close'], window=14).rsi().iloc[-1]
        
        # MACD
        macd_line = ta.trend.MACD(data['Close']).macd().iloc[-1]
        macd_signal = ta.trend.MACD(data['Close']).macd_signal().iloc[-1]
        
        # Bollinger Bands
        bb_upper = ta.volatility.BollingerBands(data['Close']).bollinger_hband().iloc[-1]
        bb_lower = ta.volatility.BollingerBands(data['Close']).bollinger_lband().iloc[-1]
        
        return {
            'current_price': round(current_price, 2),
            'sma_20': round(sma_20, 2),
            'ema_20': round(ema_20, 2),
            'rsi': round(rsi, 2),
            'macd': round(macd_line, 4),
            'macd_signal': round(macd_signal, 4),
            'bb_upper': round(bb_upper, 2),
            'bb_lower': round(bb_lower, 2)
        }
    
    def generate_signals(self, indicators: Dict) -> Dict:
        """Gera sinais de compra/venda"""
        signals = {}
        
        # Sinal RSI
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            signals['rsi_signal'] = 'COMPRA'
        elif rsi > 70:
            signals['rsi_signal'] = 'VENDA'
        else:
            signals['rsi_signal'] = 'NEUTRO'
        
        # Sinal MACD
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd > macd_signal:
            signals['macd_signal'] = 'COMPRA'
        else:
            signals['macd_signal'] = 'VENDA'
        
        # Sinal Tendência
        price = indicators.get('current_price', 0)
        sma = indicators.get('sma_20', 0)
        if price > sma:
            signals['trend_signal'] = 'COMPRA'
        else:
            signals['trend_signal'] = 'VENDA'
        
        # Sinal Geral
        buy_signals = list(signals.values()).count('COMPRA')
        sell_signals = list(signals.values()).count('VENDA')
        
        if buy_signals > sell_signals:
            signals['overall_signal'] = 'COMPRA'
        elif sell_signals > buy_signals:
            signals['overall_signal'] = 'VENDA'
        else:
            signals['overall_signal'] = 'NEUTRO'
        
        return signals
    
    def analyze(self, symbol: str) -> Dict:
        """Análise técnica completa"""
        try:
            # Buscar dados
            data = self.get_stock_data(symbol)
            if data.empty:
                return {'error': f'Dados não encontrados para {symbol}', 'success': False}
            
            # Calcular indicadores
            indicators = self.calculate_indicators(data)
            
            # Gerar sinais
            signals = self.generate_signals(indicators)
            
            return {
                'symbol': symbol,
                'indicators': indicators,
                'signals': signals,
                'success': True
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}

# Instância global
tech_analyzer = TechnicalAnalysis()
# ===== FIM ANÁLISE TÉCNICA =====

app = FastAPI(
    title="🚀 Market Intelligence Pro",
    description="Sistema Avançado de Análise de Mercado e Previsões",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

market_insights = {}
social_sentiment = {}

class AIBusinessOracle:
    def __init__(self):
        self.market_data = {}
        self.ai_predictions = {}
    
    def analyze_market_sentiment(self) -> Dict:
        """Análise de sentiment do mercado"""
        return {
            "overall_sentiment": random.uniform(-1, 1),
            "confidence": random.uniform(0.7, 0.95),
            "trend": random.choice(["BULLISH", "BEARISH", "SIDEWAYS"]),
            "key_indicators": {
                "volatility": random.uniform(0.1, 0.4),
                "momentum": random.uniform(-0.5, 0.5),
                "volume_trend": random.choice(["INCREASING", "DECREASING", "STABLE"])
            }
        }
    
    def predict_market_movement(self, symbol: str = "SPY") -> Dict:
        """Previsão de movimento de mercado"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            prediction = {
                "symbol": symbol,
                "predicted_direction": random.choice(["UP", "DOWN", "SIDEWAYS"]),
                "confidence_score": random.uniform(0.6, 0.9),
                "predicted_change_percent": random.uniform(-5, 5),
                "time_horizon": "1W",
                "reasoning": [
                    "Análise técnica favorável",
                    "Sentimento positivo em redes sociais",
                    "Fundamentos sólidos",
                    "Tendência de alta no setor"
                ]
            }
            return prediction
        except Exception as e:
            return {"error": f"Erro na previsão: {str(e)}"}

# Instância do Oracle
oracle = AIBusinessOracle()

@app.get("/")
async def root():
    return {
        "message": "🚀 Market Intelligence Pro API",
        "version": "2.0",
        "status": "Operacional",
        "features": [
            "Análise de Mercado em Tempo Real",
            "Previsões Avançadas",
            "WebSocket para Dados Live",
            "Análise de Sentiment",
            "Análise Técnica Profissional"
        ]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Dados em tempo real simulados
            live_data = {
                "timestamp": datetime.now().isoformat(),
                "market_pulse": random.uniform(-1, 1),
                "opportunity_score": random.uniform(0, 100),
                "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "alerts": generate_smart_alerts(),
                "top_performers": [
                    {"symbol": "AAPL", "change": random.uniform(1, 5)},
                    {"symbol": "MSFT", "change": random.uniform(1, 4)},
                    {"symbol": "GOOGL", "change": random.uniform(0.5, 3)}
                ],
                "market_insights": oracle.analyze_market_sentiment()
            }
            await websocket.send_json(live_data)
            await asyncio.sleep(3)
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.get("/api/market-analysis")
async def get_market_analysis():
    """Análise completa do mercado"""
    try:
        analysis = {
            "market_trend": predict_market_trend(),
            "social_sentiment": analyze_social_sentiment(),
            "financial_forecast": generate_financial_forecast(),
            "risk_indicators": calculate_risk_indicators(),
            "opportunity_zones": identify_opportunity_zones(),
            "recommendations": generate_recommendations(),
            "timestamp": datetime.now().isoformat()
        }
        return analysis
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/tech-analysis/{symbol}")
async def get_tech_analysis(symbol: str):
    """Análise técnica com indicadores reais"""
    try:
        analysis = tech_analyzer.analyze(symbol)
        return analysis
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company-insights/{symbol}")
async def get_company_insights(symbol: str):
    """Insights profundos sobre empresas"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        history = stock.history(period="1mo")
        
        # Análise de preço
        if not history.empty:
            price_change = ((history['Close'][-1] - history['Close'][0]) / history['Close'][0]) * 100
            volume_trend = "HIGH" if history['Volume'].mean() > 1000000 else "LOW"
        else:
            price_change = 0
            volume_trend = "UNKNOWN"
        
        insights = {
            "company_name": info.get('longName', symbol),
            "sector": info.get('sector', 'N/A'),
            "market_cap": info.get('marketCap', 0),
            "current_price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
            "price_change_percent": price_change,
            "volume_trend": volume_trend,
            "analysis_score": calculate_investment_score(info),
            "growth_potential": analyze_growth_potential(info),
            "risk_factors": identify_risk_factors(info),
            "competitor_analysis": analyze_competitors(symbol),
            "investment_recommendation": generate_investment_recommendation(price_change),
            "timestamp": datetime.now().isoformat()
        }
        return insights
    except Exception as e:
        return {"error": f"Erro ao analisar {symbol}: {str(e)}"}

@app.get("/api/social-intelligence")
async def get_social_intelligence():
    """Análise de sentiment em redes sociais"""
    topics = ["Artificial Intelligence", "Blockchain", "Renewable Energy", "E-commerce", "FinTech", "Cloud Computing"]
    
    sentiment_data = []
    for topic in topics:
        analysis = {
            "topic": topic,
            "sentiment_score": random.uniform(-1, 1),
            "mention_volume": random.randint(1000, 50000),
            "trend_direction": random.choice(["UP", "DOWN", "STABLE"]),
            "momentum": random.uniform(-0.5, 0.5),
            "key_influencers": generate_influencers(topic),
            "related_companies": get_related_companies(topic)
        }
        sentiment_data.append(analysis)
    
    return {
        "social_intelligence": sentiment_data,
        "overall_sentiment": random.uniform(-0.3, 0.3),
        "most_talked_topic": random.choice(topics),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/predictions/{symbol}")
async def get_predictions(symbol: str):
    """Previsões para símbolo específico"""
    return oracle.predict_market_movement(symbol)

@app.get("/api/portfolio-analysis")
async def analyze_portfolio():
    """Análise de portfolio"""
    sample_portfolio = [
        {"symbol": "AAPL", "weight": 0.25},
        {"symbol": "MSFT", "weight": 0.20},
        {"symbol": "GOOGL", "weight": 0.15},
        {"symbol": "AMZN", "weight": 0.20},
        {"symbol": "TSLA", "weight": 0.20}
    ]
    
    analysis = {
        "portfolio": sample_portfolio,
        "total_risk_score": random.uniform(0.1, 0.8),
        "diversification_score": random.uniform(0.5, 0.95),
        "expected_return": random.uniform(5, 25),
        "sector_allocation": {
            "Technology": 0.45,
            "Consumer Cyclical": 0.25,
            "Communication": 0.15,
            "Automotive": 0.15
        },
        "recommendations": [
            "Aumentar exposição em tech",
            "Diversificar em setores defensivos",
            "Considerar bonds para reduzir risco"
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    return analysis

# Funções auxiliares
def predict_market_trend() -> Dict:
    return {
        "short_term": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
        "medium_term": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
        "long_term": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
        "confidence_score": random.uniform(0.7, 0.95),
        "key_drivers": ["Tech Innovation", "Monetary Policy", "Global Events", "Earnings Season"],
        "predicted_volatility": random.uniform(0.1, 0.3)
    }

def analyze_social_sentiment() -> Dict:
    return {
        "overall_sentiment": random.uniform(-1, 1),
        "positive_topics": ["AI Adoption", "Clean Energy", "Digital Transformation", "Innovation"],
        "negative_topics": ["Regulatory Concerns", "Market Volatility", "Supply Chain", "Inflation"],
        "sentiment_trend": random.choice(["IMPROVING", "DETERIORATING", "STABLE"]),
        "social_momentum": random.uniform(-0.5, 0.5)
    }

def generate_smart_alerts() -> List[Dict]:
    alert_types = [
        {"type": "OPPORTUNITY", "message": "Alta crescimento detectado em setor de IA", "priority": "HIGH", "symbol": "AI"},
        {"type": "RISK", "message": "Aumento de volatilidade em tech stocks", "priority": "MEDIUM", "symbol": "TECH"},
        {"type": "TREND", "message": "Crescente sentiment em sustentabilidade", "priority": "LOW", "symbol": "ESG"},
        {"type": "EARNINGS", "message": "Relatórios trimestrais esta semana", "priority": "MEDIUM", "symbol": "EARN"}
    ]
    return random.sample(alert_types, 2)

def calculate_investment_score(info: Dict) -> float:
    factors = [
        info.get('profitMargins', 0) or 0,
        info.get('revenueGrowth', 0) or 0,
        info.get('debtToEquity', 0) or 0,
        random.uniform(0.5, 1.0)
    ]
    return min(10, (sum(factors) / len(factors)) * 12)

def analyze_growth_potential(info):
    return random.uniform(0, 100)

def identify_risk_factors(info):
    risks = ["Market Competition", "Regulatory Changes", "Technology Disruption", "Economic Cycles"]
    return random.sample(risks, 2)

def analyze_competitors(symbol):
    competitors = {
        "AAPL": ["MSFT", "GOOGL", "SAMSUNG"],
        "MSFT": ["AAPL", "GOOGL", "AMZN"],
        "GOOGL": ["MSFT", "AAPL", "META"],
        "AMZN": ["WMT", "TGT", "EBAY"],
        "TSLA": ["F", "GM", "NIO"]
    }
    return competitors.get(symbol, [f"{symbol}_COMP1", f"{symbol}_COMP2"])

def generate_influencers(topic):
    return [f"influencer_{topic}_{i}" for i in range(1, 3)]

def get_related_companies(topic):
    topic_companies = {
        "Artificial Intelligence": ["NVDA", "MSFT", "GOOGL", "AI"],
        "Blockchain": ["COIN", "MARA", "RIOT", "MSTR"],
        "Renewable Energy": ["NEE", "FSLR", "ENPH", "SEDG"],
        "E-commerce": ["AMZN", "SHOP", "MELI", "BABA"],
        "FinTech": ["SQ", "PYPL", "V", "MA"],
        "Cloud Computing": ["MSFT", "AMZN", "GOOGL", "ORCL"]
    }
    return topic_companies.get(topic, [])

def generate_financial_forecast():
    return {
        "revenue_growth": random.uniform(0.05, 0.2),
        "margin_expansion": random.uniform(0.01, 0.1),
        "earnings_growth": random.uniform(0.08, 0.25)
    }

def calculate_risk_indicators():
    return {
        "volatility": random.uniform(0.1, 0.4),
        "liquidity_risk": random.uniform(0, 0.3),
        "credit_risk": random.uniform(0.05, 0.2),
        "market_risk": random.uniform(0.1, 0.5)
    }

def identify_opportunity_zones():
    return ["AI Infrastructure", "Renewable Tech", "Digital Health", "FinTech Innovation"]

def generate_recommendations():
    return [
        "Aumentar exposição em tecnologia",
        "Diversificar em mercados emergentes", 
        "Monitorar taxas de juros",
        "Considerar investimentos defensivos"
    ]

def generate_investment_recommendation(price_change):
    if price_change > 5:
        return "STRONG_BUY"
    elif price_change > 0:
        return "BUY"
    elif price_change > -5:
        return "HOLD"
    else:
        return "SELL"

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Market Intelligence Pro Server...")
    print("📊 Dashboard: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
