import time
import pandas as pd
import talib as ta
from binance.client import Client
from binance.enums import *

# API Key and Secret (gunakan metode yang aman untuk menyimpannya)
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

client = Client(api_key, api_secret)

def get_historical_data(symbol, interval='1h', limit=100):
    bars = client.get_historical_klines(symbol, interval, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df

def apply_indicators(df):
    df['MA'] = ta.SMA(df['close'], timeperiod=14)
    df['RSI'] = ta.RSI(df['close'], timeperiod=14)
    return df

def place_order(symbol, action, quantity):
    if action == 'BUY':
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
    elif action == 'SELL':
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
    return order

def trade(symbol, quantity):
    df = get_historical_data(symbol)
    df = apply_indicators(df)
    
    last_rsi = df['RSI'].iloc[-1]
    last_price = df['close'].iloc[-1]
    ma = df['MA'].iloc[-1]
    
    if last_rsi < 30 and last_price < ma:
        print(f"RSI: {last_rsi}, Price: {last_price} - BUY SIGNAL")
        place_order(symbol, 'BUY', quantity)
    elif last_rsi > 70 and last_price > ma:
        print(f"RSI: {last_rsi}, Price: {last_price} - SELL SIGNAL")
        place_order(symbol, 'SELL', quantity)
    else:
        print("No clear signal.")

if __name__ == '__main__':
    symbol = 'BTCUSDT'
    quantity = 0.001
    while True:
        trade(symbol, quantity)
        time.sleep(60 * 5)  # Tunggu 5 menit
