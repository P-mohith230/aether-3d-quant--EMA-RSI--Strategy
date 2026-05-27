import streamlit as st
import plotly.graph_objects as go
from quant_engine import fetch_historical_data, apply_strategy, run_backtest

st.set_page_config(layout="wide", page_title="3D Quant Dashboard")

st.title("🚀 3D Quant Trading Dashboard")
st.markdown("Beginner-friendly visualization of EMA + RSI Strategy on BTCUSDT.")

# Fetch and Process Data
@st.cache_data
def load_data():
    df = fetch_historical_data(symbol="BTCUSDT", interval="1d", limit=365)
    df = apply_strategy(df)
    df, metrics = run_backtest(df)
    return df, metrics

df, metrics = load_data()
profit = metrics["total_profit"]

# --- TOP METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Backtest Profit", f"${profit:.2f}")
col2.metric("Final Equity", f"${df['equity'].iloc[-1]:.2f}", f"{(profit/10000)*100:.2f}%")
col3.metric("Current BTC Price", f"${df['close'].iloc[-1]:.2f}")

st.divider()

# --- 3D VISUALIZATION (Plotly) ---
st.subheader("Interactive 3D Strategy View")
st.markdown("X-axis: Time | Y-axis: Price | Z-axis: RSI (Colors indicate overbought/oversold)")

fig = go.Figure()

# Add 3D line for Price vs Time vs RSI
fig.add_trace(go.Scatter3d(
    x=df['timestamp'],
    y=df['close'],
    z=df['RSI'],
    mode='lines+markers',
    marker=dict(
        size=3,
        color=df['RSI'],
        colorscale='RdYlGn_r', # Red for Overbought(>70), Green for Oversold(<30)
        showscale=True,
        colorbar=dict(title="RSI")
    ),
    line=dict(color='white', width=2),
    name='BTC Price Path'
))

# Highlight Buy Signals in 3D
buy_signals = df[df['signal'] == 1]
fig.add_trace(go.Scatter3d(
    x=buy_signals['timestamp'],
    y=buy_signals['close'],
    z=buy_signals['RSI'],
    mode='markers',
    marker=dict(size=8, color='green', symbol='circle'),
    name='Buy Signal'
))

# Highlight Sell Signals in 3D
sell_signals = df[df['signal'] == -1]
fig.add_trace(go.Scatter3d(
    x=sell_signals['timestamp'],
    y=sell_signals['close'],
    z=sell_signals['RSI'],
    mode='markers',
    marker=dict(size=8, color='red', symbol='x'),
    name='Sell Signal'
))

fig.update_layout(
    scene=dict(
        xaxis_title='Time',
        yaxis_title='Price (USDT)',
        zaxis_title='RSI',
        bgcolor='black'
    ),
    height=700,
    margin=dict(r=20, l=10, b=10, t=10)
)

st.plotly_chart(fig, use_container_width=True)

# --- 2D EQUITY CURVE ---
st.subheader("2D Equity Curve (Account Balance over Time)")
equity_fig = go.Figure()
equity_fig.add_trace(go.Scatter(x=df['timestamp'], y=df['equity'], mode='lines', name='Equity', line=dict(color='cyan')))
st.plotly_chart(equity_fig, use_container_width=True)
