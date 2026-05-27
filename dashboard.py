import streamlit as st
import plotly.graph_objects as go
from quant_engine import fetch_historical_data, apply_strategy, run_backtest

st.set_page_config(layout="wide", page_title="Aether Quant Dashboard")

# Cache-busting version key — bump on every code change
CACHE_VERSION = "v5_2026_05_27"

@st.cache_data(ttl=3600)
def load_strategy_data(_version):
    df = fetch_historical_data(symbol="BTCUSDT", interval="1d", limit=365)
    df = apply_strategy(df)
    df, metrics = run_backtest(df)
    return df, metrics

try:
    df, metrics = load_strategy_data(CACHE_VERSION)
except Exception:
    st.cache_data.clear()
    df, metrics = load_strategy_data(CACHE_VERSION)

# Auto-retry if stale cache returned 0 trades
if metrics["num_trades"] == 0:
    st.cache_data.clear()
    df, metrics = load_strategy_data(CACHE_VERSION)

profit = metrics["total_profit"]

st.title("🚀 Aether Quant Trading Dashboard")
st.markdown("EMA 9/21 + RSI Pullback Strategy on BTCUSDT")

# --- TOP METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("🔄 Number of Trades", f"{metrics['num_trades']}")
col2.metric("🎯 Win Rate", f"{metrics['win_rate']:.1f}%")
col3.metric("💰 Total Profit", f"${profit:,.2f}", f"{(profit/10000)*100:.2f}% ROI")

st.divider()

# --- PRICE CHART WITH SIGNALS ---
st.subheader("📈 Price Chart with Buy/Sell Signals")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df['timestamp'], open=df['open'], high=df['high'],
    low=df['low'], close=df['close'], name='BTC Price',
    increasing_line_color='#00C853', decreasing_line_color='#FF1744'
))

fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['EMA_9'],
    mode='lines', name='EMA 9', line=dict(color='yellow', width=2)
))

fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['EMA_21'],
    mode='lines', name='EMA 21', line=dict(color='orange', width=2)
))

buy_df = df[df['signal'] == 1]
fig.add_trace(go.Scatter(
    x=buy_df['timestamp'], y=buy_df['close'],
    mode='markers', name='BUY',
    marker=dict(symbol='triangle-up', size=12, color='#00E676',
                line=dict(color='white', width=1))
))

sell_df = df[df['signal'] == -1]
fig.add_trace(go.Scatter(
    x=sell_df['timestamp'], y=sell_df['close'],
    mode='markers', name='SELL',
    marker=dict(symbol='triangle-down', size=12, color='#FF1744',
                line=dict(color='white', width=1))
))

fig.update_layout(
    height=600, template="plotly_dark",
    xaxis_rangeslider_visible=False,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, width='stretch')

# --- EQUITY CURVE ---
st.subheader("💰 Equity Curve (Account Balance over Time)")
equity_fig = go.Figure()
equity_fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['equity'], mode='lines', name='Equity',
    line=dict(color='cyan', width=2), fill='tozeroy', fillcolor='rgba(0,255,255,0.1)'
))
equity_fig.add_hline(y=10000, line_dash="dash", line_color="#888",
                     annotation_text="Starting Capital ($10,000)")
equity_fig.update_layout(height=400, template="plotly_dark",
                         yaxis_title="Account Value ($)", xaxis_title="Date")
st.plotly_chart(equity_fig, width='stretch')

st.caption("For educational & research purposes only • Not financial advice")
