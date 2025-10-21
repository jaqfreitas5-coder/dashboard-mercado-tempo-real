from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import logging

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
    def analyze(self, symbol: str):
        try:
            logger.info(f"Analisando símbolo: {symbol}")
            
            # Tentar diferentes formatos de símbolo
            symbols_to_try = [symbol, f"{symbol}.SA", f"{symbol}.AX"]
            
            for sym in symbols_to_try:
                try:
                    stock = yf.Ticker(sym)
                    data = stock.history(period="1mo")
                    
                    if not data.empty and len(data) > 20:
                        current_price = data['Close'].iloc[-1]
                        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
                        rsi = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
                        
                        return {
                            'symbol': sym,
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
                            'success': True
                        }
                except Exception as e:
                    logger.warning(f"Falha com {sym}: {e}")
                    continue
            
            return {"error": f"Nenhum dado encontrado para {symbol}. Tente: PETR4.SA, VALE3.SA, ITSA4.SA", "success": False}
            
        except Exception as e:
            logger.error(f"Erro geral: {e}")
            return {'error': f"Erro interno: {str(e)}", 'success': False}

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
