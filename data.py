import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

class TechStockData:
    def __init__(self):
        self.tech_tickers = self._get_nyse_tech_tickers()

    def _get_nyse_tech_tickers(self):
        """Scrape NYSE tech tickers"""
        url = "https://www.nyse.com/listings_directory/stock"
        sectors = {
            'Technology Services': ['GOOG', 'MSFT', 'META'],
            'Electronic Technology': ['AAPL', 'NVDA', 'AMD'],
            # Add more sectors as needed
        }
        return [ticker for sublist in sectors.values() for ticker in sublist]

    def get_historical_data(self, ticker, years_back=5):
        """Get OHLCV + fundamentals"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*years_back)

        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date, interval='1d')

            # Add fundamental data
            fundamentals = {
                'pe_ratio': stock.info.get('trailingPE'),
                'profit_margins': stock.info.get('profitMargins'),
                'revenue_growth': stock.info.get('revenueGrowth'),
                'rsi_14': self._calculate_rsi(hist['Close']),
                'institutional_ownership': stock.info.get('heldPercentInstitutions'),
                'short_interest': stock.info.get('shortPercentOfFloat')
            }

            return {
                'historical': hist,
                'fundamentals': fundamentals,
                'info': stock.info
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def _calculate_rsi(self, close_prices, window=14):
        """Calculate RSI indicator"""
        delta = close_prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
