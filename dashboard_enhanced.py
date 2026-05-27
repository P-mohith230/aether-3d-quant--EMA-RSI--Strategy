"""
=============================================================================
🚀 ENHANCED 3D QUANT TRADING DASHBOARD
=============================================================================
This dashboard provides MULTIPLE 3D visualization options to help beginners
understand trading data from different perspectives.

Each visualization explained:
1. 3D Price-Time-RSI Path    → See how price moves with momentum
2. 3D Surface (Price Terrain) → See price as a landscape/mountain
3. 3D Candlestick Tower      → Traditional candles in 3D space
4. 3D Volume Bars            → See trading activity in 3D
5. 3D Signal Sphere          → All signals in one spherical view

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
    page_title="3D Quant Dashboard - Enhanced",
    page_icon="📈"
)

st.title("📈 Enhanced 3D Quant Trading Dashboard")
st.markdown("""
**Beginner-Friendly Guide:** This dashboard shows BTC trading data in multiple 3D views.
Each visualization helps you understand different aspects of trading!
""")

# =============================================================================
# LOAD DATA
# =============================================================================
@st.cache_data
def load_data():
    """Fetch BTC data and apply our EMA + RSI strategy"""
    df = fetch_historical_data(symbol="BTCUSDT", interval="1d", limit=365)
    df = apply_strategy(df)
    df, metrics = run_backtest(df)
    # Add a numeric index for 3D plotting
    df['day_index'] = range(len(df))
    return df, metrics

df, metrics = load_data()
profit = metrics["total_profit"]

# =============================================================================
# TOP METRICS - Key Numbers at a Glance
# =============================================================================
st.markdown("---")
st.subheader("📊 Key Performance Metrics")

# First Row of Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Profit/Loss",
        value=f"${profit:,.2f}",
        delta=f"{(profit/10000)*100:.1f}%"
    )
    st.caption("How much money we made/lost")

with col2:
    st.metric(
        label="📈 Final Account Balance",
        value=f"${df['equity'].iloc[-1]:,.2f}"
    )
    st.caption("Total portfolio capital at closure")

with col3:
    st.metric(
        label="🎯 Strategy Win Rate",
        value=f"{metrics['win_rate']:.1f}%"
    )
    st.caption("Percentage of profitable trades")

with col4:
    st.metric(
        label="⚖️ Profit Factor",
        value=f"{metrics['profit_factor']:.2f}"
    )
    st.caption("Gross Profits divided by Gross Losses")

# Second Row of Metrics
st.write("") # Add spacing
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        label="📉 Maximum Drawdown (Max DD)",
        value=f"{metrics['max_drawdown']:.2f}%"
    )
    st.caption("Peak-to-trough drop from equity curve")

with col6:
    st.metric(
        label="📊 Sharpe Ratio",
        value=f"{metrics['sharpe_ratio']:.2f}"
    )
    st.caption("Risk-adjusted volatility return")

with col7:
    st.metric(
        label="🔄 Reward-to-Risk Ratio",
        value=f"{metrics['avg_win_loss_ratio']:.2f}:1"
    )
    st.caption("Average Win-to-Loss ratio per trade")

with col8:
    st.metric(
        label="🔔 Executed Trades",
        value=f"{metrics['num_trades']}"
    )
    st.caption("Total completed trading lifecycle runs")

st.markdown("---")

# =============================================================================
# VISUALIZATION SELECTOR
# =============================================================================
st.subheader("🎨 Choose Your 3D Visualization")

viz_option = st.selectbox(
    "Select a visualization style:",
    [
        "1️⃣ 3D Price Journey (Time × Price × RSI)",
        "2️⃣ 3D Mountain Terrain (Price Surface)",
        "3️⃣ 3D Candlestick Towers",
        "4️⃣ 3D Volume Activity Bars",
        "5️⃣ 3D Signal Overview (All-in-One)"
    ],
    index=0
)

# =============================================================================
# VISUALIZATION 1: 3D PRICE JOURNEY PATH
# =============================================================================
if viz_option.startswith("1"):
    st.markdown("""
    ### 🎯 Understanding This Chart:

    ```
    What you're seeing:
    ┌─────────────────────────────────────────────────────────────┐
    │  • WHITE LINE = Bitcoin's price moving through time         │
    │  • GREEN DOTS = BUY signals (good time to buy!)            │
    │  • RED X's    = SELL signals (good time to sell!)          │
    │  • COLORS     = RSI value (Green=oversold, Red=overbought) │
    └─────────────────────────────────────────────────────────────┘

    How to read it:
    - Follow the white line from left to right = Price over time
    - When line goes UP = Price increasing
    - When line moves FORWARD (toward you) = RSI is high (overbought)
    - When line moves BACK = RSI is low (oversold, good buying time)

    🖱️ TIP: Click and drag to rotate! Scroll to zoom!
    ```
    """)

    fig = go.Figure()

    # Main price path
    fig.add_trace(go.Scatter3d(
        x=df['day_index'],
        y=df['close'],
        z=df['RSI'],
        mode='lines+markers',
        marker=dict(
            size=4,
            color=df['RSI'],
            colorscale='RdYlGn_r',  # Red=high RSI, Green=low RSI
            showscale=True,
            colorbar=dict(title="RSI<br>Value", x=1.02)
        ),
        line=dict(color='white', width=3),
        name='BTC Price Journey',
        hovertemplate=(
            '<b>Day:</b> %{x}<br>'
            '<b>Price:</b> $%{y:,.2f}<br>'
            '<b>RSI:</b> %{z:.1f}<br>'
            '<extra></extra>'
        )
    ))

    # Buy signals - Green spheres
    buy_df = df[df['signal'] == 1]
    fig.add_trace(go.Scatter3d(
        x=buy_df['day_index'],
        y=buy_df['close'],
        z=buy_df['RSI'],
        mode='markers',
        marker=dict(size=12, color='lime', symbol='circle',
                   line=dict(color='white', width=2)),
        name='🟢 BUY Signal',
        hovertemplate='<b>BUY!</b><br>Price: $%{y:,.2f}<br>RSI: %{z:.1f}<extra></extra>'
    ))

    # Sell signals - Red X
    sell_df = df[df['signal'] == -1]
    fig.add_trace(go.Scatter3d(
        x=sell_df['day_index'],
        y=sell_df['close'],
        z=sell_df['RSI'],
        mode='markers',
        marker=dict(size=12, color='red', symbol='x',
                   line=dict(color='white', width=2)),
        name='🔴 SELL Signal',
        hovertemplate='<b>SELL!</b><br>Price: $%{y:,.2f}<br>RSI: %{z:.1f}<extra></extra>'
    ))

    # Add RSI threshold planes for reference
    # Oversold zone (RSI = 30)
    fig.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['close'].min(), df['close'].min()], [df['close'].max(), df['close'].max()]],
        z=[[30, 30], [30, 30]],
        colorscale=[[0, 'rgba(0,255,0,0.2)'], [1, 'rgba(0,255,0,0.2)']],
        showscale=False,
        name='Oversold Zone (RSI=30)',
        hoverinfo='skip'
    ))

    # Overbought zone (RSI = 70)
    fig.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['close'].min(), df['close'].min()], [df['close'].max(), df['close'].max()]],
        z=[[70, 70], [70, 70]],
        colorscale=[[0, 'rgba(255,0,0,0.2)'], [1, 'rgba(255,0,0,0.2)']],
        showscale=False,
        name='Overbought Zone (RSI=70)',
        hoverinfo='skip'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='📅 Day Number', backgroundcolor='rgb(20,20,20)'),
            yaxis=dict(title='💵 Price (USD)', backgroundcolor='rgb(20,20,20)'),
            zaxis=dict(title='📊 RSI (0-100)', backgroundcolor='rgb(20,20,20)', range=[0, 100]),
            bgcolor='rgb(10,10,10)'
        ),
        height=700,
        margin=dict(r=20, l=10, b=10, t=40),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0.5)')
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# VISUALIZATION 2: 3D MOUNTAIN TERRAIN (PRICE SURFACE)
# =============================================================================
elif viz_option.startswith("2"):
    st.markdown("""
    ### 🏔️ Understanding This Chart:

    ```
    What you're seeing:
    ┌─────────────────────────────────────────────────────────────┐
    │  A 3D "terrain" or "landscape" made from price data!       │
    │                                                             │
    │  • PEAKS (mountains) = High prices                          │
    │  • VALLEYS (low areas) = Low prices                         │
    │  • COLOR = Price level (Purple=low, Yellow=high)           │
    └─────────────────────────────────────────────────────────────┘

    Imagine flying over a mountain range:
    - Mountains going UP = Price was HIGH
    - Going into valleys = Price was LOW
    - The terrain shows price movement over time!

    🖱️ TIP: Rotate to see it from different angles!
    ```
    """)

    # Create a surface from price data
    # We'll create a "ribbon" effect by extending the price line

    x = np.array(df['day_index'])
    y_base = np.linspace(0, 1, 20)  # Width of the ribbon

    # Create meshgrid
    X, Y = np.meshgrid(x, y_base)

    # Price as height (Z), repeated across Y
    Z = np.tile(df['close'].values, (20, 1))

    # Add some variation to make it more terrain-like
    noise = np.random.normal(0, df['close'].std() * 0.02, Z.shape)
    Z = Z + noise * Y  # More variation at edges

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale='Viridis',
        colorbar=dict(title='Price ($)', x=1.02),
        hovertemplate='Day: %{x}<br>Price: $%{z:,.2f}<extra></extra>'
    ))

    # Add buy signals as markers on top
    buy_df = df[df['signal'] == 1]
    fig.add_trace(go.Scatter3d(
        x=buy_df['day_index'],
        y=[0.5] * len(buy_df),
        z=buy_df['close'] + 1000,  # Slightly above surface
        mode='markers+text',
        marker=dict(size=10, color='lime', symbol='diamond'),
        text=['BUY'] * len(buy_df),
        textposition='top center',
        name='🟢 BUY'
    ))

    # Add sell signals
    sell_df = df[df['signal'] == -1]
    fig.add_trace(go.Scatter3d(
        x=sell_df['day_index'],
        y=[0.5] * len(sell_df),
        z=sell_df['close'] + 1000,
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='diamond'),
        text=['SELL'] * len(sell_df),
        textposition='top center',
        name='🔴 SELL'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number',
            yaxis_title='Width',
            zaxis_title='💵 Price (USD)',
            bgcolor='rgb(10,10,10)'
        ),
        height=700,
        margin=dict(r=20, l=10, b=10, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# VISUALIZATION 3: 3D CANDLESTICK TOWERS
# =============================================================================
elif viz_option.startswith("3"):
    st.markdown("""
    ### 🕯️ Understanding This Chart:

    ```
    What you're seeing:
    ┌─────────────────────────────────────────────────────────────┐
    │  Traditional candlesticks shown as 3D BARS/TOWERS!         │
    │                                                             │
    │  Each bar represents ONE DAY of trading:                   │
    │                                                             │
    │      🟩 GREEN TOWER = Price went UP that day (bullish)     │
    │      🟥 RED TOWER   = Price went DOWN that day (bearish)   │
    │      HEIGHT = How much price changed (volatility)          │
    └─────────────────────────────────────────────────────────────┘

    Reading candlesticks:
       ┬  ← High price
       │
       █  ← Body (open to close)
       │
       ┴  ← Low price

    🖱️ Rotate to see patterns over time!
    ```
    """)

    fig = go.Figure()

    # Sample every few days for cleaner visualization
    sample_df = df.iloc[::3].reset_index(drop=True)  # Every 3rd day

    for i, row in sample_df.iterrows():
        # Determine color based on price movement
        if row['close'] >= row['open']:
            color = 'lime'  # Bullish (price went up)
        else:
            color = 'red'   # Bearish (price went down)

        # Create a 3D bar for each candle
        # X: day, Y: 0 (single row), Z: price range

        # Body of candle (open to close)
        fig.add_trace(go.Mesh3d(
            x=[i-0.3, i+0.3, i+0.3, i-0.3, i-0.3, i+0.3, i+0.3, i-0.3],
            y=[-0.3, -0.3, 0.3, 0.3, -0.3, -0.3, 0.3, 0.3],
            z=[row['open'], row['open'], row['open'], row['open'],
               row['close'], row['close'], row['close'], row['close']],
            i=[0, 0, 0, 0, 4, 4, 0, 1, 1, 2, 2, 3],
            j=[1, 2, 3, 4, 5, 6, 1, 5, 2, 6, 3, 7],
            k=[2, 3, 0, 5, 6, 7, 4, 4, 5, 5, 6, 6],
            color=color,
            opacity=0.8,
            showlegend=False,
            hovertemplate=f'Day {i}<br>Open: ${row["open"]:,.2f}<br>Close: ${row["close"]:,.2f}<extra></extra>'
        ))

    # Add EMA lines
    fig.add_trace(go.Scatter3d(
        x=sample_df.index,
        y=[0] * len(sample_df),
        z=sample_df['EMA_9'],
        mode='lines',
        line=dict(color='yellow', width=4),
        name='EMA 9 (Fast)'
    ))

    fig.add_trace(go.Scatter3d(
        x=sample_df.index,
        y=[0] * len(sample_df),
        z=sample_df['EMA_21'],
        mode='lines',
        line=dict(color='orange', width=4),
        name='EMA 21 (Slow)'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number',
            yaxis_title='',
            zaxis_title='💵 Price (USD)',
            bgcolor='rgb(10,10,10)',
            yaxis=dict(showticklabels=False)
        ),
        height=700,
        margin=dict(r=20, l=10, b=10, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# VISUALIZATION 4: 3D VOLUME ACTIVITY BARS
# =============================================================================
elif viz_option.startswith("4"):
    st.markdown("""
    ### 📊 Understanding This Chart:

    ```
    What you're seeing:
    ┌─────────────────────────────────────────────────────────────┐
    │  VOLUME = How much Bitcoin was traded each day             │
    │                                                             │
    │  • TALL bars = LOTS of trading activity (high interest!)   │
    │  • SHORT bars = Little trading (quiet market)              │
    │  • COLOR = Based on price that day                         │
    └─────────────────────────────────────────────────────────────┘

    Why volume matters:
    - High volume + price UP = Strong bullish move! 💪
    - High volume + price DOWN = Strong selling pressure! 😰
    - Low volume = Nobody cares about this move 🤷

    🖱️ Rotate to see volume spikes over time!
    ```
    """)

    # Sample data for cleaner visualization
    sample_df = df.iloc[::5].reset_index(drop=True)  # Every 5th day

    fig = go.Figure()

    # Create 3D bar chart for volume
    fig.add_trace(go.Bar3d(
        x=sample_df['day_index'].tolist(),
        y=[0] * len(sample_df),
        z=[0] * len(sample_df),
        dx=[1] * len(sample_df),
        dy=[0.8] * len(sample_df),
        dz=sample_df['volume'].tolist(),
        color=sample_df['close'].tolist(),
        colorscale='Blues',
        opacity=0.8,
        showlegend=False
    ) if hasattr(go, 'Bar3d') else go.Scatter3d(
        # Fallback: Use scatter3d with varying sizes
        x=sample_df['day_index'],
        y=[0] * len(sample_df),
        z=sample_df['volume'] / 2,  # Center the "bars"
        mode='markers',
        marker=dict(
            size=sample_df['volume'] / sample_df['volume'].max() * 30,
            color=sample_df['close'],
            colorscale='Blues',
            colorbar=dict(title='Price ($)')
        ),
        name='Volume'
    ))

    # Since Bar3d might not exist, let's use a creative alternative
    # Using vertical lines for each volume bar
    for i, row in sample_df.iterrows():
        # Normalize volume for visualization
        vol_height = row['volume'] / sample_df['volume'].max() * 50000

        # Color based on price change
        color = 'lime' if row['close'] > row['open'] else 'red'

        fig.add_trace(go.Scatter3d(
            x=[row['day_index'], row['day_index']],
            y=[0, 0],
            z=[0, vol_height],
            mode='lines',
            line=dict(color=color, width=10),
            showlegend=False,
            hovertemplate=f'Day {row["day_index"]}<br>Volume: {row["volume"]:,.0f}<extra></extra>'
        ))

    # Add price line on top
    fig.add_trace(go.Scatter3d(
        x=sample_df['day_index'],
        y=[0.5] * len(sample_df),
        z=sample_df['close'] / sample_df['close'].max() * 50000,  # Scaled
        mode='lines+markers',
        line=dict(color='yellow', width=3),
        marker=dict(size=4, color='yellow'),
        name='Price (scaled)'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number',
            yaxis_title='',
            zaxis_title='📊 Trading Volume',
            bgcolor='rgb(10,10,10)',
            yaxis=dict(showticklabels=False)
        ),
        height=700,
        margin=dict(r=20, l=10, b=10, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# VISUALIZATION 5: 3D SIGNAL OVERVIEW (ALL-IN-ONE)
# =============================================================================
elif viz_option.startswith("5"):
    st.markdown("""
    ### 🎯 Understanding This Chart:

    ```
    What you're seeing:
    ┌─────────────────────────────────────────────────────────────┐
    │  A complete 3D overview of all trading signals!            │
    │                                                             │
    │  X-axis = Day (time)                                       │
    │  Y-axis = EMA Difference (momentum indicator)              │
    │  Z-axis = RSI (overbought/oversold)                        │
    │                                                             │
    │  • 🟢 GREEN = BUY zones (oversold + upward momentum)       │
    │  • 🔴 RED = SELL zones (overbought + downward momentum)    │
    │  • GRAY = Neutral (no clear signal)                        │
    └─────────────────────────────────────────────────────────────┘

    The IDEAL trades:
    - BUY when: Point is GREEN (low RSI) and Y is positive (EMA crossover up)
    - SELL when: Point is RED (high RSI) and Y is negative (EMA crossover down)
    ```
    """)

    # Calculate EMA difference (momentum)
    df['ema_diff'] = df['EMA_9'] - df['EMA_21']

    # Create color based on signal conditions
    colors = []
    for _, row in df.iterrows():
        if row['RSI'] < 30 and row['ema_diff'] > 0:
            colors.append('lime')  # Strong BUY
        elif row['RSI'] > 70 and row['ema_diff'] < 0:
            colors.append('red')   # Strong SELL
        elif row['RSI'] < 40:
            colors.append('lightgreen')  # Weak BUY
        elif row['RSI'] > 60:
            colors.append('salmon')  # Weak SELL
        else:
            colors.append('gray')  # Neutral

    fig = go.Figure()

    # Main scatter plot
    fig.add_trace(go.Scatter3d(
        x=df['day_index'],
        y=df['ema_diff'],
        z=df['RSI'],
        mode='markers',
        marker=dict(
            size=6,
            color=colors,
            opacity=0.7,
            line=dict(color='white', width=1)
        ),
        name='All Data Points',
        hovertemplate=(
            'Day: %{x}<br>'
            'EMA Diff: %{y:.2f}<br>'
            'RSI: %{z:.1f}<br>'
            '<extra></extra>'
        )
    ))

    # Highlight actual BUY signals
    buy_df = df[df['signal'] == 1]
    fig.add_trace(go.Scatter3d(
        x=buy_df['day_index'],
        y=buy_df['ema_diff'],
        z=buy_df['RSI'],
        mode='markers',
        marker=dict(size=15, color='lime', symbol='diamond',
                   line=dict(color='white', width=2)),
        name='🟢 Executed BUY'
    ))

    # Highlight actual SELL signals
    sell_df = df[df['signal'] == -1]
    fig.add_trace(go.Scatter3d(
        x=sell_df['day_index'],
        y=sell_df['ema_diff'],
        z=sell_df['RSI'],
        mode='markers',
        marker=dict(size=15, color='red', symbol='x',
                   line=dict(color='white', width=2)),
        name='🔴 Executed SELL'
    ))

    # Add reference planes
    # RSI = 30 plane (oversold threshold)
    fig.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['ema_diff'].min(), df['ema_diff'].min()],
           [df['ema_diff'].max(), df['ema_diff'].max()]],
        z=[[30, 30], [30, 30]],
        colorscale=[[0, 'rgba(0,255,0,0.15)'], [1, 'rgba(0,255,0,0.15)']],
        showscale=False,
        name='RSI=30 (Oversold)',
        hoverinfo='skip'
    ))

    # RSI = 70 plane (overbought threshold)
    fig.add_trace(go.Surface(
        x=[[0, len(df)], [0, len(df)]],
        y=[[df['ema_diff'].min(), df['ema_diff'].min()],
           [df['ema_diff'].max(), df['ema_diff'].max()]],
        z=[[70, 70], [70, 70]],
        colorscale=[[0, 'rgba(255,0,0,0.15)'], [1, 'rgba(255,0,0,0.15)']],
        showscale=False,
        name='RSI=70 (Overbought)',
        hoverinfo='skip'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='📅 Day Number',
            yaxis_title='📈 EMA Difference (Momentum)',
            zaxis_title='📊 RSI (0-100)',
            bgcolor='rgb(10,10,10)',
            zaxis=dict(range=[0, 100])
        ),
        height=700,
        margin=dict(r=20, l=10, b=10, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# ADDITIONAL 2D CHARTS FOR CONTEXT
# =============================================================================
st.markdown("---")
st.subheader("📈 Supporting 2D Charts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Equity Curve (Your Account Balance)")
    st.markdown("""
    ```
    This line shows how your account value changed over time.
    ↗️ Going UP = Making money!
    ↘️ Going DOWN = Losing money
    ```
    """)

    equity_fig = go.Figure()
    equity_fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['equity'],
        mode='lines',
        name='Equity',
        line=dict(color='cyan', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,255,255,0.1)'
    ))
    equity_fig.add_hline(y=10000, line_dash="dash", line_color="white",
                         annotation_text="Starting Balance ($10,000)")
    equity_fig.update_layout(
        height=300,
        yaxis_title="Account Value ($)",
        xaxis_title="Date"
    )
    st.plotly_chart(equity_fig, use_container_width=True)

with col2:
    st.markdown("#### RSI Indicator Over Time")
    st.markdown("""
    ```
    RSI measures if BTC is OVERBOUGHT or OVERSOLD
    🟢 Below 30 = Oversold (potential BUY!)
    🔴 Above 70 = Overbought (potential SELL!)
    ```
    """)

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=2)
    ))
    rsi_fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.2,
                      annotation_text="Oversold Zone")
    rsi_fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.2,
                      annotation_text="Overbought Zone")
    rsi_fig.update_layout(
        height=300,
        yaxis_title="RSI Value",
        xaxis_title="Date",
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(rsi_fig, use_container_width=True)

# =============================================================================
# LEARNING SECTION
# =============================================================================
st.markdown("---")
st.subheader("📚 Quick Learning Guide")

with st.expander("🔰 What is EMA Crossover?"):
    st.markdown("""
    **EMA = Exponential Moving Average**

    Think of it as a "smoothed average" of recent prices.

    ```
    EMA 9  (Fast) = Average of last 9 days  → Reacts quickly
    EMA 21 (Slow) = Average of last 21 days → Reacts slowly

    📈 When Fast EMA crosses ABOVE Slow EMA:
       → Price is going UP → Consider BUYING

    📉 When Fast EMA crosses BELOW Slow EMA:
       → Price is going DOWN → Consider SELLING
    ```

    **Visual Example:**
    ```
    Price: ──────╱╲──────╱╲────
    EMA 9:  ─────╱──╲───╱───╲───  (follows price closely)
    EMA 21: ──────╱────╲───╱──── (smoother, slower)
                 ↑        ↑
            BUY signal  SELL signal
    ```
    """)

with st.expander("🔰 What is RSI?"):
    st.markdown("""
    **RSI = Relative Strength Index** (ranges from 0 to 100)

    It measures if something is "too expensive" or "too cheap".

    ```
    RSI > 70 = OVERBOUGHT 🔴
    → Too many people bought → Price might drop → SELL signal

    RSI < 30 = OVERSOLD 🟢
    → Too many people sold → Price might rise → BUY signal

    RSI 30-70 = NEUTRAL ⚪
    → No clear signal
    ```

    **Think of it like:**
    - RSI > 70 = "Everyone already bought. Party's over!"
    - RSI < 30 = "Everyone sold in panic. Time to buy cheap!"
    """)

with st.expander("🔰 How Our Strategy Combines Both"):
    st.markdown("""
    **Our Strategy: EMA Crossover + RSI Confirmation**

    We only trade when BOTH indicators agree:

    ```
    ✅ BUY when:
       • EMA 9 > EMA 21 (uptrend starting)
       • AND RSI < 30 (oversold = good deal!)

    ✅ SELL when:
       • EMA 9 < EMA 21 (downtrend starting)
       • AND RSI > 70 (overbought = exit time!)
    ```

    **Why combine them?**
    - EMA alone might give false signals
    - RSI alone might be too early
    - Together = STRONGER, more reliable signals!
    """)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Built with Streamlit + Plotly | Educational purposes only | Not financial advice!")
