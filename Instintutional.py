def detect_institutional_flow(df):
    """Identifies institutional buying through price/volume patterns"""
    close = df['Close']
    volume = df['Volume']
    
    # 1. Up days on higher volume than down days
    up_days = close.diff() > 0
    volume_ratio = volume[up_days].mean() / volume[~up_days].mean()
    
    # 2. Closing in upper half of daily range
    daily_range = df['High'] - df['Low']
    close_position = (close - df['Low']) / daily_range
    upper_close_days = (close_position > 0.6).mean()
    
    return {
        'volume_ratio': volume_ratio,
        'upper_close_percent': upper_close_days,
        'composite_score': volume_ratio * upper_close_days * 100
    }
