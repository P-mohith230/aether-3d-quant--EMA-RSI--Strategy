import pandas as pd
import numpy as np
import requests

def fetch_historical_data(symbol="BTCUSDT", interval="1h", limit=1000):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    numeric_columns = ["open", "high", "low", "close", "volume"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    
    return df

def apply_strategy(df):
    # Calculate EMA
    df["EMA_9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["EMA_21"] = df["close"].ewm(span=21, adjust=False).mean()
    
    # Calculate RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # Generate Signals
    df["signal"] = 0
    df["position"] = 0
    
    # Buy: EMA 9 > EMA 21 and RSI < 30 (Oversold but trending up)
    buy_condition = (df["EMA_9"] > df["EMA_21"]) & (df["RSI"] < 30)
    # Sell: EMA 9 < EMA 21 and RSI > 70 (Overbought and trending down)
    sell_condition = (df["EMA_9"] < df["EMA_21"]) & (df["RSI"] > 70)
    
    df.loc[buy_condition, "signal"] = 1
    df.loc[sell_condition, "signal"] = -1
    
    return df

def run_backtest(df):
    initial_balance = 10000
    balance = initial_balance
    position = 0
    equity_curve = []
    
    stop_loss_pct = 0.02
    take_profit_pct = 0.05
    entry_price = 0
    
    for index, row in df.iterrows():
        price = row["close"]
        
        # Check Stop-Loss / Take-Profit
        if position > 0:
            if price <= entry_price * (1 - stop_loss_pct): # Stop Loss
                balance = position * price
                position = 0
                entry_price = 0
            elif price >= entry_price * (1 + take_profit_pct): # Take Profit
                balance = position * price
                position = 0
                entry_price = 0
                
        # Execute Signals
        if row["signal"] == 1 and position == 0:
            position = balance / price
            balance = 0
            entry_price = price
        elif row["signal"] == -1 and position > 0:
            balance = position * price
            position = 0
            entry_price = 0
            
        current_equity = balance + (position * price)
        equity_curve.append(current_equity)
        
    df["equity"] = equity_curve
    profit = df["equity"].iloc[-1] - initial_balance
    
    return df, profit

if __name__ == "__main__":
    df = fetch_historical_data()
    df = apply_strategy(df)
    df, profit = run_backtest(df)
    print(f"Backtest complete. Total Profit: ${profit:.2f}")
