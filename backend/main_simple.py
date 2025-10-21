from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

app = FastAPI(title="Dashboard Mercado - API Simplificada")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TechnicalAnalysisSimple:
    def analyze(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="3mo")
            
            if data.empty:
                return {"error": f"Dados não encontrados para {symbol}", "success": False}
            
            # Indicadores básicos
            current_price = data['Close'].iloc[-1]
            sma_20 = data['Close'].rolling(20).mean().iloc[-1]
            rsi = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
            
            return {
                'symbol': symbol,
                'indicators': {
                    'current_price': round(current_price, 2),
                    'sma_20': round(sma_20, 2),
                    'rsi': round(rsi, 2)
                },
                'signals': {
                    'rsi_signal': 'COMPRA' if rsi < 30 else 'VENDA' if rsi > 70 else 'NEUTRO',
                    'trend_signal': 'COMPRA' if current_price > sma_20 else 'VENDA',
                    'overall_signal': 'COMPRA' if (rsi < 30 and current_price > sma_20) else 'VENDA' if (rsi > 70 and current_price < sma_20) else 'NEUTRO'
                },
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}

tech_analyzer = TechnicalAnalysisSimple()

@app.get("/")
async def root():
    return {"message": "API Dashboard Mercado - Online", "status": "operational"}

@app.get("/api/tech-analysis/{symbol}")
async def get_tech_analysis(symbol: str):
    return tech_analyzer.analyze(symbol)

@app.get("/api/market-analysis")
async def get_market_analysis():
    return {
        "market_trend": "NEUTRAL",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
