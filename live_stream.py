import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    price = float(data['c']) # Current closing price
    print(f"Live BTCUSDT Price: ${price:.2f}")
    
    # Here you would typically append this to your real-time dataframe
    # and check your EMA/RSI conditions.
    
def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket Closed ###")

def on_open(ws):
    print("### WebSocket Opened: Streaming BTCUSDT ###")

if __name__ == "__main__":
    # Binance Mini Ticker stream for BTCUSDT
    socket_url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
    
    ws = websocket.WebSocketApp(socket_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()
