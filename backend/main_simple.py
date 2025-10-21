from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import logging
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dashboard Mercado")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TechnicalAnalysis:
    def generate_simulated_data(self, symbol: str):
        """Gera dados simulados para demonstração"""
        base_prices = {
            'PETR4.SA': 35.50, 'VALE3.SA': 68.20, 'ITSA4.SA': 10.15,
            'AAPL': 185.00, 'TSLA': 245.50, 'MSFT': 410.75
        }
        
        base_price = base_prices.get(symbol, 50.00)
        
        # Simular variação de preço
        current_price = base_price * (1 + random.uniform(-0.1, 0.1))
        sma_20 = current_price * (1 + random.uniform(-0.05, 0.05))
        rsi = random.uniform(20, 80)
        
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
            'success': True,
            'simulated': True
        }

    def analyze(self, symbol: str):
        try:
            logger.info(f"Analisando símbolo: {symbol}")
            
            # Tentar buscar dados reais
            try:
                stock = yf.Ticker(symbol)
                data = stock.history(period="1mo")
                
                if not data.empty and len(data) > 20:
                    current_price = data['Close'].iloc[-1]
                    sma_20 = data['Close'].rolling(20).mean().iloc[-1]
                    rsi = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
                    
                    return {
                        'symbol': symbol,
                        'indicators': {
                            'current_price': round(current_price, 2),
                            'sma_20': round(sma_20, 2),
                            'rsi': round(rsi, 2) if not pd.isna(rsi) else 50
                        },
                        'signals': {
                            'rsi_signal': 'COMPRA' if rsi < 30 else 'VENDA' if rsi > 70 else 'NEUTRO',
                            'trend_signal': 'COMPRA' if current_price > sma_20 else 'VENDA',
                            'overall_signal': 'COMPRA' if (rsi < 30 and current_price > sma_20) else 'VENDA' if (rsi > 70 and current_price < sma_20) else 'NEUTRO'
                        },
                        'success': True,
                        'simulated': False
                    }
            except Exception as e:
                logger.warning(f"Erro com yFinance: {e}")
            
            # Fallback para dados simulados
            logger.info(f"Usando dados simulados para {symbol}")
            return self.generate_simulated_data(symbol)
            
        except Exception as e:
            logger.error(f"Erro geral: {e}")
            return self.generate_simulated_data(symbol)

analyzer = TechnicalAnalysis()

@app.get("/")
async def root():
    return {"message": "Dashboard Mercado API - Online", "status": "operational"}

@app.get("/api/tech-analysis/{symbol}")
async def tech_analysis(symbol: str):
    return analyzer.analyze(symbol)

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
