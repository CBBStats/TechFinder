import numpy as np
from scipy import stats

class GrowthAnalyzer:
    def __init__(self, threshold=5.0):
        self.threshold = threshold  # Minimum growth multiplier to consider

    def find_explosive_periods(self, df):
        """Identify periods where stock grew >threshold in 12 months"""
        explosive_periods = []
        close_prices = df['Close'].values

        for i in range(len(close_prices) - 252):  # 252 trading days
            start_price = close_prices[i]
            max_future = max(close_prices[i:i+252])

            if max_future / start_price >= self.threshold:
                explosive_periods.append({
                    'start_index': i,
                    'growth_multiple': max_future / start_price,
                    'duration_days': np.argmax(close_prices[i:i+252] >= self.threshold * start_price) + 1
                })

        return explosive_periods

    def analyze_pre_conditions(self, df, explosive_period):
        """Analyze 6 months before explosive growth"""
        pre_window = df.iloc[max(0, explosive_period['start_index']-126):explosive_period['start_index']]

        analysis = {
            'volume_trend': self._calculate_trend(pre_window['Volume']),
            'price_consolidation': self._calculate_consolidation(pre_window['Close']),
            'rsi_profile': self._analyze_rsi(pre_window),
            'institutional_flow': self._estimate_institutional_activity(pre_window),
            'earnings_surprises': self._check_earnings_surprises(pre_window)
        }

        return analysis

    def _calculate_trend(self, series):
        """Calculate linear regression slope"""
        x = np.arange(len(series))
        slope, _, _, _, _ = stats.linregress(x, series)
        return slope

    def _calculate_consolidation(self, prices):
        """Measure price consolidation before breakout"""
        high = prices.max()
        low = prices.min()
        mean = prices.mean()
        return (high - low) / mean  # Lower values = tighter consolidation

    def _analyze_rsi(self, window):
        """Analyze RSI behavior"""
        rsi = TechStockData()._calculate_rsi(window['Close'])
        return {
            'oversold_days': sum(rsi < 30),
            'overbought_days': sum(rsi > 70),
            'mean_rsi': np.mean(rsi)
        }
