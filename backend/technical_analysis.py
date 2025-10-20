import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple
import ta  # Biblioteca de análise técnica

class TechnicalAnalyzer:
    def __init__(self):
        self.indicators = {}
    
    def get_stock_data(self, symbol: str, period: str = "6mo") -> pd.DataFrame:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Erro ao buscar dados de {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_sma(self, data: pd.DataFrame, window: int = 20) -> pd.Series:
        return data['Close'].rolling(window=window).mean()
    
    def calculate_ema(self, data: pd.DataFrame, window: int = 20) -> pd.Series:
        return data['Close'].ewm(span=window, adjust=False).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
       
        return ta.momentum.RSIIndicator(data['Close'], window=window).rsi()
    
    def calculate_macd(self, data: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
                macd = ta.trend.MACD(data['Close'])
        return macd.macd(), macd.macd_signal(), macd.macd_diff()
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, window: int = 20) -> Tuple[pd.Series, pd.Series, pd.Series]:
                bb = ta.volatility.BollingerBands(data['Close'], window=window)
        return bb.bollinger_hband(), bb.bollinger_lband(), bb.bollinger_mavg()
    
    def calculate_stochastic(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
               return ta.momentum.StochasticOscillator(
            data['High'], data['Low'], data['Close'], window=window
        ).stoch()
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        signals = {
            "rsi_signal": "NEUTRO",
            "macd_signal": "NEUTRO", 
            "trend_signal": "NEUTRO",
            "overall_signal": "NEUTRO"
        }
        
        # RSI Signal
        if len(data) > 0:
            current_rsi = data['RSI_14'].iloc[-1] if 'RSI_14' in data.columns else 50
            if current_rsi < 30:
                signals["rsi_signal