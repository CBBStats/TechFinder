def calculate_vw_consolidation(df):
    """Identifies tight trading ranges with volume buildup"""
    price_range = df['High'].rolling(20).max() - df['Low'].rolling(20).min()
    price_range_pct = price_range / df['Close'].rolling(20).mean()
    volume_ma = df['Volume'].rolling(20).mean()
    
    # Score between 0-100 (lower = better)
    return 100 * (price_range_pct / (volume_ma / volume_ma.max()))
