"""
=============================================================================
🚀 AETHER QUANT — EMA/RSI Strategy Dashboard
=============================================================================
Full-featured quantitative trading dashboard with:
  • Key Metrics: Number of Trades, Win Rate, Profit
  • 2D Charts: Candlestick, Equity Curve, RSI, Volume
  • 3D Research Visualizations: Price-RSI Path, Terrain, Candlestick
    Towers, Volume Bars, Signal Overview
  • Strategy Architecture & Learning Guides

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
# 🌐 3D RESEARCH VISUALIZATIONS
# =============================================================================
st.markdown("---")
st.subheader("🌐 3D Research Visualizations")
st.markdown("""
Explore the strategy from multiple 3D perspectives. These interactive views reveal patterns
that are invisible in flat 2D charts. **Click and drag to rotate, scroll to zoom!**
""")

viz_option = st.selectbox(
    "Select a 3D visualization:",
    [
        "1️⃣ 3D Price Journey (Time × Price × RSI)",
        "2️⃣ 3D Mountain Terrain (Price Surface)",
        "3️⃣ 3D Candlestick Towers",
        "4️⃣ 3D Volume Activity Bars",
        "5️⃣ 3D Signal Overview (All-in-One)"
    ],
    index=0
)

# ---------------------------------------------------------------------------
# VIZ 1: 3D PRICE JOURNEY PATH
# ---------------------------------------------------------------------------
if viz_option.startswith("1"):
    st.markdown("""
    **What you see:** The white line traces BTC's price through three dimensions —
    time (X), price (Y), and RSI momentum (Z). Green dots = BUY, Red X = SELL.
    Colors shift from green (oversold) to red (overbought).
    """)

    fig3d = go.Figure()

    # Main price path
    fig3d.add_trace(go.Scatter3d(
        x=df['day_index'], y=df['close'], z=df['RSI'],
        mode='lines+markers',
        marker=dict(
            size=4, color=df['RSI'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="RSI<br>Value", x=1.02)
        ),
        line=dict(color='white', width=3),
        name='BTC Price Journey',
        hovertemplate='<b>Day:</b> %{x}<br><b>Price:</b> $%{y:,.2f}<br><b>RSI:</b> %{z:.1f}<extra></extra>'
    ))

    # Buy signals
    buy_3d = df[df['signal'] == 1]
    fig3d.add_trace(go.Scatter3d(
        x=buy_3d['day_index'], y=buy_3d['close'], z=buy_3d['RSI'],
        mode='markers',
        marker=dict(size=12, color='lime', symbol='circle',
                    line=dict(color='white', width=2)),
        name='🟢 BUY Signal',
        hovertemplate='<b>BUY!</b><br>Price: $%{y:,.2f}<br>RSI: %{z:.1f}<extra></extra>'
    ))

    # Sell signals
    sell_3d = df[df['signal'] == -1]
    fig3d.add_trace(go.Scatter3d(
        x=sell_3d['day_index'], y=sell_3d['close'], z=sell_3d['RSI'],
        mode='markers',
        marker=dict(size=12, color='red', symbol='x',
                    line=dict(color='white', width=2)),
        name='🔴 SELL Signal',
        hovertemplate='<b>SELL!</b><br>Price: $%{y:,.2f}<br>RSI: %{z:.1f}<extra></extra>'
    ))

    # RSI threshold planes
    fig3d.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['close'].min(), df['close'].min()], [df['close'].max(), df['close'].max()]],
        z=[[30, 30], [30, 30]],
        colorscale=[[0, 'rgba(0,255,0,0.2)'], [1, 'rgba(0,255,0,0.2)']],
        showscale=False, name='Oversold Zone (RSI=30)', hoverinfo='skip'
    ))
    fig3d.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['close'].min(), df['close'].min()], [df['close'].max(), df['close'].max()]],
        z=[[70, 70], [70, 70]],
        colorscale=[[0, 'rgba(255,0,0,0.2)'], [1, 'rgba(255,0,0,0.2)']],
        showscale=False, name='Overbought Zone (RSI=70)', hoverinfo='skip'
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis=dict(title='📅 Day Number', backgroundcolor='rgb(20,20,20)'),
            yaxis=dict(title='💵 Price (USD)', backgroundcolor='rgb(20,20,20)'),
            zaxis=dict(title='📊 RSI (0-100)', backgroundcolor='rgb(20,20,20)', range=[0, 100]),
            bgcolor='rgb(10,10,10)'
        ),
        height=700, margin=dict(r=20, l=10, b=10, t=40),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0.5)')
    )
    st.plotly_chart(fig3d, width='stretch')

# ---------------------------------------------------------------------------
# VIZ 2: 3D MOUNTAIN TERRAIN
# ---------------------------------------------------------------------------
elif viz_option.startswith("2"):
    st.markdown("""
    **What you see:** Price data rendered as a 3D terrain/landscape.
    Peaks = high prices, valleys = low prices. Color encodes price level (purple=low, yellow=high).
    """)

    x = np.array(df['day_index'])
    y_base = np.linspace(0, 1, 20)
    X, Y = np.meshgrid(x, y_base)
    Z = np.tile(df['close'].values, (20, 1))
    noise = np.random.normal(0, df['close'].std() * 0.02, Z.shape)
    Z = Z + noise * Y

    fig3d = go.Figure()
    fig3d.add_trace(go.Surface(
        x=X, y=Y, z=Z, colorscale='Viridis',
        colorbar=dict(title='Price ($)', x=1.02),
        hovertemplate='Day: %{x}<br>Price: $%{z:,.2f}<extra></extra>'
    ))

    buy_3d = df[df['signal'] == 1]
    fig3d.add_trace(go.Scatter3d(
        x=buy_3d['day_index'], y=[0.5] * len(buy_3d),
        z=buy_3d['close'] + 1000,
        mode='markers+text',
        marker=dict(size=10, color='lime', symbol='diamond'),
        text=['BUY'] * len(buy_3d), textposition='top center', name='🟢 BUY'
    ))

    sell_3d = df[df['signal'] == -1]
    fig3d.add_trace(go.Scatter3d(
        x=sell_3d['day_index'], y=[0.5] * len(sell_3d),
        z=sell_3d['close'] + 1000,
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='diamond'),
        text=['SELL'] * len(sell_3d), textposition='top center', name='🔴 SELL'
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number', yaxis_title='Width', zaxis_title='💵 Price (USD)',
            bgcolor='rgb(10,10,10)'
        ),
        height=700, margin=dict(r=20, l=10, b=10, t=40)
    )
    st.plotly_chart(fig3d, width='stretch')

# ---------------------------------------------------------------------------
# VIZ 3: 3D CANDLESTICK TOWERS
# ---------------------------------------------------------------------------
elif viz_option.startswith("3"):
    st.markdown("""
    **What you see:** Traditional candlesticks rendered as 3D towers.
    🟩 Green = price went UP (bullish). 🟥 Red = price went DOWN (bearish).
    Yellow line = EMA 9 (Fast), Orange line = EMA 21 (Slow).
    """)

    fig3d = go.Figure()
    sample_df = df.iloc[::3].reset_index(drop=True)

    for i, row in sample_df.iterrows():
        color = 'lime' if row['close'] >= row['open'] else 'red'
        fig3d.add_trace(go.Mesh3d(
            x=[i-0.3, i+0.3, i+0.3, i-0.3, i-0.3, i+0.3, i+0.3, i-0.3],
            y=[-0.3, -0.3, 0.3, 0.3, -0.3, -0.3, 0.3, 0.3],
            z=[row['open'], row['open'], row['open'], row['open'],
               row['close'], row['close'], row['close'], row['close']],
            i=[0, 0, 0, 0, 4, 4, 0, 1, 1, 2, 2, 3],
            j=[1, 2, 3, 4, 5, 6, 1, 5, 2, 6, 3, 7],
            k=[2, 3, 0, 5, 6, 7, 4, 4, 5, 5, 6, 6],
            color=color, opacity=0.8, showlegend=False,
            hovertemplate=f'Day {i}<br>Open: ${row["open"]:,.2f}<br>Close: ${row["close"]:,.2f}<extra></extra>'
        ))

    fig3d.add_trace(go.Scatter3d(
        x=sample_df.index, y=[0] * len(sample_df), z=sample_df['EMA_9'],
        mode='lines', line=dict(color='yellow', width=4), name='EMA 9 (Fast)'
    ))
    fig3d.add_trace(go.Scatter3d(
        x=sample_df.index, y=[0] * len(sample_df), z=sample_df['EMA_21'],
        mode='lines', line=dict(color='orange', width=4), name='EMA 21 (Slow)'
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number', yaxis_title='',
            zaxis_title='💵 Price (USD)', bgcolor='rgb(10,10,10)',
            yaxis=dict(showticklabels=False)
        ),
        height=700, margin=dict(r=20, l=10, b=10, t=40)
    )
    st.plotly_chart(fig3d, width='stretch')

# ---------------------------------------------------------------------------
# VIZ 4: 3D VOLUME ACTIVITY BARS
# ---------------------------------------------------------------------------
elif viz_option.startswith("4"):
    st.markdown("""
    **What you see:** Trading volume as 3D bars. Tall bars = lots of activity,
    short bars = quiet market. Green = bullish day, Red = bearish day.
    Yellow line = scaled price overlay.
    """)

    sample_df = df.iloc[::5].reset_index(drop=True)
    fig3d = go.Figure()

    for i, row in sample_df.iterrows():
        vol_height = row['volume'] / sample_df['volume'].max() * 50000
        color = 'lime' if row['close'] > row['open'] else 'red'
        fig3d.add_trace(go.Scatter3d(
            x=[row['day_index'], row['day_index']], y=[0, 0], z=[0, vol_height],
            mode='lines', line=dict(color=color, width=10),
            showlegend=False,
            hovertemplate=f'Day {row["day_index"]}<br>Volume: {row["volume"]:,.0f}<extra></extra>'
        ))

    fig3d.add_trace(go.Scatter3d(
        x=sample_df['day_index'], y=[0.5] * len(sample_df),
        z=sample_df['close'] / sample_df['close'].max() * 50000,
        mode='lines+markers', line=dict(color='yellow', width=3),
        marker=dict(size=4, color='yellow'), name='Price (scaled)'
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number', yaxis_title='',
            zaxis_title='📊 Trading Volume', bgcolor='rgb(10,10,10)',
            yaxis=dict(showticklabels=False)
        ),
        height=700, margin=dict(r=20, l=10, b=10, t=40)
    )
    st.plotly_chart(fig3d, width='stretch')

# ---------------------------------------------------------------------------
# VIZ 5: 3D SIGNAL OVERVIEW (ALL-IN-ONE)
# ---------------------------------------------------------------------------
elif viz_option.startswith("5"):
    st.markdown("""
    **What you see:** Complete 3D signal map. X = time, Y = EMA momentum difference,
    Z = RSI. Green = buy zones, Red = sell zones, Gray = neutral.
    Transparent planes mark RSI 30 (oversold) and RSI 70 (overbought) thresholds.
    """)

    df['ema_diff'] = df['EMA_9'] - df['EMA_21']

    colors = []
    for _, row in df.iterrows():
        if row['RSI'] < 30 and row['ema_diff'] > 0:
            colors.append('lime')
        elif row['RSI'] > 70 and row['ema_diff'] < 0:
            colors.append('red')
        elif row['RSI'] < 40:
            colors.append('lightgreen')
        elif row['RSI'] > 60:
            colors.append('salmon')
        else:
            colors.append('gray')

    fig3d = go.Figure()
    fig3d.add_trace(go.Scatter3d(
        x=df['day_index'], y=df['ema_diff'], z=df['RSI'],
        mode='markers',
        marker=dict(size=6, color=colors, opacity=0.7, line=dict(color='white', width=1)),
        name='All Data Points',
        hovertemplate='Day: %{x}<br>EMA Diff: %{y:.2f}<br>RSI: %{z:.1f}<extra></extra>'
    ))

    buy_3d = df[df['signal'] == 1]
    fig3d.add_trace(go.Scatter3d(
        x=buy_3d['day_index'], y=buy_3d['ema_diff'], z=buy_3d['RSI'],
        mode='markers',
        marker=dict(size=15, color='lime', symbol='diamond', line=dict(color='white', width=2)),
        name='🟢 Executed BUY'
    ))

    sell_3d = df[df['signal'] == -1]
    fig3d.add_trace(go.Scatter3d(
        x=sell_3d['day_index'], y=sell_3d['ema_diff'], z=sell_3d['RSI'],
        mode='markers',
        marker=dict(size=15, color='red', symbol='x', line=dict(color='white', width=2)),
        name='🔴 Executed SELL'
    ))

    # RSI threshold planes
    fig3d.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['ema_diff'].min(), df['ema_diff'].min()],
           [df['ema_diff'].max(), df['ema_diff'].max()]],
        z=[[30, 30], [30, 30]],
        colorscale=[[0, 'rgba(0,255,0,0.15)'], [1, 'rgba(0,255,0,0.15)']],
        showscale=False, name='RSI=30 (Oversold)', hoverinfo='skip'
    ))
    fig3d.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['ema_diff'].min(), df['ema_diff'].min()],
           [df['ema_diff'].max(), df['ema_diff'].max()]],
        z=[[70, 70], [70, 70]],
        colorscale=[[0, 'rgba(255,0,0,0.15)'], [1, 'rgba(255,0,0,0.15)']],
        showscale=False, name='RSI=70 (Overbought)', hoverinfo='skip'
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number',
            yaxis_title='📈 EMA Difference (Momentum)',
            zaxis_title='📊 RSI (0-100)',
            bgcolor='rgb(10,10,10)', zaxis=dict(range=[0, 100])
        ),
        height=700, margin=dict(r=20, l=10, b=10, t=40)
    )
    st.plotly_chart(fig3d, width='stretch')

# =============================================================================
# 🏛️ RESEARCH ARCHITECTURE
# =============================================================================
st.markdown("---")
st.subheader("🏛️ Strategy Architecture & Research Design")

with st.expander("📐 System Architecture", expanded=False):
    st.markdown("""
    ```
    ┌──────────────────────────────────────────────────────────────────┐
    │                    AETHER QUANT ARCHITECTURE                     │
    ├──────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
    │  │ DATA LAYER  │────▶│ STRATEGY     │────▶│ BACKTEST ENGINE │  │
    │  │             │     │ ENGINE       │     │                 │  │
    │  │ • Binance   │     │ • EMA 9/21   │     │ • Trade Sim     │  │
    │  │   API       │     │   Crossover  │     │ • Stop Loss 2%  │  │
    │  │ • Multi-    │     │ • RSI < 55   │     │ • Take Profit   │  │
    │  │   endpoint  │     │   Pullback   │     │   5%            │  │
    │  │ • Synthetic │     │ • RSI > 70   │     │ • Equity Curve  │  │
    │  │   Fallback  │     │   Exit       │     │ • Metrics Calc  │  │
    │  └─────────────┘     └──────────────┘     └────────┬────────┘  │
    │                                                     │           │
    │                                           ┌─────────▼────────┐  │
    │                                           │ DASHBOARD LAYER  │  │
    │                                           │                  │  │
    │                                           │ • Key Metrics    │  │
    │                                           │ • 2D Charts      │  │
    │                                           │ • 3D Research    │  │
    │                                           │   Visualizations │  │
    │                                           │ • Streamlit UI   │  │
    │                                           └──────────────────┘  │
    └──────────────────────────────────────────────────────────────────┘
    ```
    """)

with st.expander("🔬 Strategy Signal Pipeline", expanded=False):
    st.markdown("""
    ```
    MARKET DATA (1D candles, 365 days)
        │
        ▼
    ┌─────────────────────────────────┐
    │  INDICATOR CALCULATION          │
    │  ├─ EMA 9  (Fast Moving Avg)    │
    │  ├─ EMA 21 (Slow Moving Avg)    │
    │  └─ RSI 14 (Momentum Osc.)     │
    └───────────────┬─────────────────┘
                    │
        ┌───────────▼───────────┐
        │  SIGNAL GENERATION    │
        │                       │
        │  BUY when:            │
        │  • EMA9 > EMA21  AND  │
        │  • RSI < 55           │
        │                       │
        │  SELL when:           │
        │  • EMA9 < EMA21  OR   │
        │  • RSI > 70           │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │  RISK MANAGEMENT      │
        │                       │
        │  • Stop Loss:  -2%    │
        │  • Take Profit: +5%   │
        │  • Position Sizing:   │
        │    100% of capital    │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │  METRICS OUTPUT       │
        │                       │
        │  • Win Rate           │
        │  • Profit Factor      │
        │  • Max Drawdown       │
        │  • Sharpe Ratio       │
        │  • Avg Win/Loss Ratio │
        └───────────────────────┘
    ```
    """)

with st.expander("📂 Data Pipeline & Resilience", expanded=False):
    st.markdown("""
    ```
    ┌───────────────────────────────────────────────────────────┐
    │                   DATA FETCH PIPELINE                     │
    ├───────────────────────────────────────────────────────────┤
    │                                                           │
    │  Endpoint Rotation (Geo-Blocking Bypass):                 │
    │  ┌────────────────────────────────────────────┐           │
    │  │ 1. api.binance.com     (Primary)           │           │
    │  │ 2. api1.binance.com    (Backup Cluster 1)  │           │
    │  │ 3. api2.binance.com    (Backup Cluster 2)  │           │
    │  │ 4. api3.binance.com    (Backup Cluster 3)  │           │
    │  │ 5. api.binance.us      (US Endpoint)       │           │
    │  └──────────────────┬─────────────────────────┘           │
    │                     │                                     │
    │          ┌──────────▼──────────┐                          │
    │          │ All endpoints fail? │                          │
    │          └──────────┬──────────┘                          │
    │                     │ YES                                 │
    │          ┌──────────▼──────────────┐                      │
    │          │ SYNTHETIC MARKET        │                      │
    │          │ GENERATOR               │                      │
    │          │ • Seed: 42              │                      │
    │          │ • Start: $62,500        │                      │
    │          │ • Drift: +0.03%/day     │                      │
    │          │ • Volatility: 1.8%/day  │                      │
    │          └─────────────────────────┘                      │
    │                                                           │
    │  Browser-Mimicking Headers:                               │
    │  User-Agent: Chrome 120 (Windows NT 10.0)                 │
    │                                                           │
    │  Cache Strategy:                                          │
    │  • Streamlit @cache_data with TTL=3600s                   │
    │  • Versioned cache key for forced invalidation            │
    │  • Auto-retry on zero-trade detection                     │
    └───────────────────────────────────────────────────────────┘
    ```
    """)

# =============================================================================
# 📚 LEARNING SECTION
# =============================================================================
st.markdown("---")
st.subheader("📚 Strategy Learning Guide")

with st.expander("🔰 What is EMA Crossover?"):
    st.markdown("""
    **EMA = Exponential Moving Average** — a "smoothed average" of recent prices.

    ```
    EMA 9  (Fast) = Average of last 9 days  → Reacts quickly to price changes
    EMA 21 (Slow) = Average of last 21 days → Reacts slowly, filters noise

    📈 When Fast EMA crosses ABOVE Slow EMA → Uptrend starting → BUY
    📉 When Fast EMA crosses BELOW Slow EMA → Downtrend starting → SELL
    ```

    **Visual Example:**
    ```
    Price: ──────╱╲──────╱╲────
    EMA 9:  ─────╱──╲───╱───╲──  (follows price closely)
    EMA 21: ──────╱────╲───╱──── (smoother, slower)
                 ↑        ↑
            BUY signal  SELL signal
    ```
    """)

with st.expander("🔰 What is RSI?"):
    st.markdown("""
    **RSI = Relative Strength Index** (ranges from 0 to 100)

    It measures if an asset is "too expensive" or "too cheap" right now.

    ```
    RSI > 70 = OVERBOUGHT 🔴 → Too many buyers → Price may drop → SELL
    RSI < 30 = OVERSOLD   🟢 → Too many sellers → Price may rise → BUY
    RSI 30-70 = NEUTRAL   ⚪ → No extreme signal
    ```

    **Think of it like a rubber band:**
    - Stretched too far up (RSI > 70) = will snap back down
    - Stretched too far down (RSI < 30) = will snap back up
    """)

with st.expander("🔰 How Our Strategy Combines Both"):
    st.markdown("""
    **Aether Strategy: EMA Crossover + RSI Pullback Confirmation**

    We only trade when BOTH indicators agree:

    ```
    ✅ BUY when:
       • EMA 9 > EMA 21 (uptrend confirmed)
       • AND RSI < 55 (not overbought — catching the pullback)

    ✅ SELL when:
       • EMA 9 < EMA 21 (downtrend starts)
       • OR RSI > 70 (overbought — time to take profits)
    ```

    **Why combine them?**
    - EMA alone gives false signals during sideways markets
    - RSI alone can signal too early before trends develop
    - Together = **stronger, more reliable** trade signals!
    """)

with st.expander("📊 Key Metrics Explained"):
    st.markdown("""
    | Metric | What It Means | Good Value |
    |--------|--------------|------------|
    | **Win Rate** | % of trades that were profitable | > 40% |
    | **Profit Factor** | Gross profit ÷ Gross loss | > 1.3 |
    | **Max Drawdown** | Largest peak-to-trough equity drop | > -20% |
    | **Sharpe Ratio** | Risk-adjusted return per unit of volatility | > 1.0 |
    | **Avg Win/Loss** | Average winning trade ÷ Average losing trade | > 1.5:1 |
    """)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Built with Streamlit + Plotly • Aether 3D Quant Research • For educational & research purposes only • Not financial advice")
