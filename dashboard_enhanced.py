"""
=============================================================================
🚀 AETHER QUANT — EMA/RSI Strategy Dashboard
=============================================================================
Minimalist, mobile-friendly dashboard focused on key metrics:
  • Number of Trades
  • Win Rate
  • Profit

With 2D interactive charts for analysis.

Run: streamlit run dashboard_enhanced.py
=============================================================================
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from quant_engine import fetch_historical_data, apply_strategy, run_backtest

# =============================================================================
# PAGE SETUP
# =============================================================================
st.set_page_config(
    layout="wide",
    page_title="Aether Quant — EMA/RSI Strategy",
    page_icon="📈"
)

# =============================================================================
# LOAD DATA — ttl=3600 ensures cache auto-busts every hour.
# The _version parameter forces re-computation when code changes.
# =============================================================================
CACHE_VERSION = "v5_2026_05_27"  # Bump this to force cache invalidation

@st.cache_data(ttl=3600)
def load_strategy_data(_version):
    """Fetch BTC data, apply strategy, and run backtest.
    _version: cache-busting key (underscore prefix tells Streamlit to ignore it in display)
    """
    df = fetch_historical_data(symbol="BTCUSDT", interval="1d", limit=365)
    df = apply_strategy(df)
    df, metrics = run_backtest(df)
    df['day_index'] = range(len(df))
    return df, metrics

# Force clear any old cache on first load after code update
try:
    df, metrics = load_strategy_data(CACHE_VERSION)
except Exception as e:
    st.cache_data.clear()
    df, metrics = load_strategy_data(CACHE_VERSION)

# =============================================================================
# DEBUG GUARD — If metrics are still zero due to some edge case, show raw debug
# =============================================================================
if metrics["num_trades"] == 0:
    st.warning("⚠️ Backtest produced 0 trades. Clearing cache and retrying...")
    st.cache_data.clear()
    df, metrics = load_strategy_data(CACHE_VERSION)

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div style="text-align:center; padding: 1rem 0;">
    <h1 style="margin-bottom:0;">📈 Aether Quant Dashboard</h1>
    <p style="color: #888; font-size: 1.1rem;">EMA 9/21 + RSI Pullback Strategy — BTCUSDT</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 🔑 TOP 3 KEY METRICS — The user specifically asked for these
# =============================================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🔄 Number of Trades",
        value=f"{metrics['num_trades']}"
    )

with col2:
    wr = metrics['win_rate']
    st.metric(
        label="🎯 Win Rate",
        value=f"{wr:.1f}%",
        delta="Good" if wr >= 50 else "Needs Tuning",
        delta_color="normal" if wr >= 50 else "inverse"
    )

with col3:
    profit = metrics['total_profit']
    st.metric(
        label="💰 Total Profit",
        value=f"${profit:,.2f}",
        delta=f"{(profit / 10000) * 100:.2f}% ROI",
        delta_color="normal" if profit >= 0 else "inverse"
    )

# =============================================================================
# EXTENDED METRICS (collapsed by default, for power users)
# =============================================================================
with st.expander("📊 All Backtesting Metrics", expanded=False):
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("📈 Final Equity", f"${df['equity'].iloc[-1]:,.2f}")
    with mcol2:
        st.metric("⚖️ Profit Factor", f"{metrics['profit_factor']:.2f}")
    with mcol3:
        st.metric("📉 Max Drawdown", f"{metrics['max_drawdown']:.2f}%")
    with mcol4:
        st.metric("📊 Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")

    mcol5, mcol6, mcol7, mcol8 = st.columns(4)
    with mcol5:
        st.metric("🏆 Avg Win/Loss Ratio", f"{metrics['avg_win_loss_ratio']:.2f}:1")
    with mcol6:
        st.metric("💵 Starting Capital", "$10,000.00")
    with mcol7:
        current_price = df['close'].iloc[-1]
        st.metric("₿ Latest BTC Price", f"${current_price:,.2f}")
    with mcol8:
        buy_signals = (df['signal'] == 1).sum()
        sell_signals = (df['signal'] == -1).sum()
        st.metric("📡 Buy / Sell Signals", f"{buy_signals} / {sell_signals}")

st.markdown("---")

# =============================================================================
# CHART 1: PRICE + EMA CROSSOVER + BUY/SELL SIGNALS
# =============================================================================
st.subheader("📈 Price Chart with EMA Crossover & Signals")

price_fig = go.Figure()

# Candlestick chart
price_fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='BTC Price',
    increasing_line_color='#00C853',
    decreasing_line_color='#FF1744'
))

# EMA lines
price_fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['EMA_9'],
    mode='lines', name='EMA 9 (Fast)',
    line=dict(color='#FFD600', width=2)
))

price_fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['EMA_21'],
    mode='lines', name='EMA 21 (Slow)',
    line=dict(color='#FF6D00', width=2)
))

# Buy signals
buy_df = df[df['signal'] == 1]
price_fig.add_trace(go.Scatter(
    x=buy_df['timestamp'], y=buy_df['close'],
    mode='markers', name='BUY',
    marker=dict(symbol='triangle-up', size=12, color='#00E676',
                line=dict(color='white', width=1))
))

# Sell signals
sell_df = df[df['signal'] == -1]
price_fig.add_trace(go.Scatter(
    x=sell_df['timestamp'], y=sell_df['close'],
    mode='markers', name='SELL',
    marker=dict(symbol='triangle-down', size=12, color='#FF1744',
                line=dict(color='white', width=1))
))

price_fig.update_layout(
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USDT)",
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(price_fig, width='stretch')

# =============================================================================
# CHART 2 & 3: EQUITY CURVE + RSI (Side by side)
# =============================================================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💰 Equity Curve")

    equity_fig = go.Figure()
    equity_fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['equity'],
        mode='lines', name='Portfolio Value',
        line=dict(color='#00BCD4', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,188,212,0.1)'
    ))
    equity_fig.add_hline(
        y=10000, line_dash="dash", line_color="#888",
        annotation_text="Starting Capital ($10,000)"
    )
    equity_fig.update_layout(
        height=350,
        yaxis_title="Account Value ($)",
        xaxis_title="Date",
        template="plotly_dark"
    )
    st.plotly_chart(equity_fig, width='stretch')

with col_right:
    st.subheader("📊 RSI Indicator")

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['RSI'],
        mode='lines', name='RSI',
        line=dict(color='#AB47BC', width=2)
    ))
    rsi_fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.15,
                      annotation_text="Oversold Zone", annotation_position="bottom left")
    rsi_fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.15,
                      annotation_text="Overbought Zone", annotation_position="top left")
    rsi_fig.update_layout(
        height=350,
        yaxis_title="RSI Value",
        xaxis_title="Date",
        yaxis=dict(range=[0, 100]),
        template="plotly_dark"
    )
    st.plotly_chart(rsi_fig, width='stretch')

# =============================================================================
# CHART 4: VOLUME
# =============================================================================
st.subheader("📊 Trading Volume")

vol_fig = go.Figure()

# Color bars green/red based on price movement
colors = ['#00C853' if c >= o else '#FF1744' for c, o in zip(df['close'], df['open'])]

vol_fig.add_trace(go.Bar(
    x=df['timestamp'], y=df['volume'],
    marker_color=colors,
    name='Volume',
    opacity=0.7
))

vol_fig.update_layout(
    height=300,
    yaxis_title="Volume",
    xaxis_title="Date",
    template="plotly_dark"
)

st.plotly_chart(vol_fig, width='stretch')

# =============================================================================
# STRATEGY EXPLANATION (collapsible)
# =============================================================================
st.markdown("---")
with st.expander("📚 How This Strategy Works", expanded=False):
    st.markdown("""
    ### EMA 9/21 Crossover + RSI Pullback Strategy

    **Entry (Buy) Conditions:**
    - EMA 9 > EMA 21 (uptrend confirmed)
    - RSI < 55 (not overbought — pullback entry)

    **Exit (Sell) Conditions:**
    - EMA 9 < EMA 21 (trend reversal) **OR**
    - RSI > 70 (overbought — take profit)

    **Risk Management:**
    - Stop Loss: 2% below entry price
    - Take Profit: 5% above entry price

    **Key Metrics Explained:**
    | Metric | What It Means |
    |--------|--------------|
    | Win Rate | % of trades that were profitable |
    | Profit Factor | Gross profit ÷ Gross loss (>1.0 = profitable) |
    | Max Drawdown | Largest peak-to-trough drop in equity |
    | Sharpe Ratio | Risk-adjusted return (>1.0 = good) |
    """)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Built with Streamlit + Plotly • For educational & research purposes only • Not financial advice")
