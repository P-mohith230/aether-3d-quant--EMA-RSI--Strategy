# <div align="center">AETHER-3D QUANT</div>

<!-- PLATFORM HEADER BANNER -->
<div align="center">
  <svg width="100%" max-width="850px" height="260px" viewBox="0 0 850 260" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: #070709; border-radius: 12px; border: 1px solid #1E2030; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <!-- Background Gradients -->
    <rect width="850" height="260" rx="12" fill="url(#bg_gradient)" />
    <!-- Cyber Grid Pattern -->
    <rect width="850" height="260" rx="12" fill="url(#cyber_grid)" opacity="0.45" />
    
    <!-- Neon Glow Filters -->
    <defs>
      <linearGradient id="bg_gradient" x1="0" y1="0" x2="850" y2="260" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stop-color="#090514"/>
        <stop offset="50%" stop-color="#0E0F1E"/>
        <stop offset="100%" stop-color="#040407"/>
      </linearGradient>
      <linearGradient id="neon_cyan_grad" x1="0" y1="200" x2="600" y2="50" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stop-color="#00FFA3" stop-opacity="0.2"/>
        <stop offset="50%" stop-color="#00D2FF" stop-opacity="1"/>
        <stop offset="100%" stop-color="#BD00FF" stop-opacity="0.9"/>
      </linearGradient>
      <pattern id="cyber_grid" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#252A45" stroke-width="0.5"/>
      </pattern>
      <filter id="neon_glow_cyan" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="6" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="neon_glow_green" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="8" result="blur1" />
        <feGaussianBlur stdDeviation="3" result="blur2" />
        <feMerge>
          <feMergeNode in="blur1" />
          <feMergeNode in="blur2" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="neon_glow_red" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="8" result="blur1" />
        <feGaussianBlur stdDeviation="3" result="blur2" />
        <feMerge>
          <feMergeNode in="blur1" />
          <feMergeNode in="blur2" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>

    <!-- Perspective 3D Landscape Wireframe -->
    <path d="M 50 220 L 250 140 L 450 180 L 600 110 L 800 130" stroke="url(#neon_cyan_grad)" stroke-width="3.5" stroke-linecap="round" filter="url(#neon_glow_cyan)" />
    <path d="M 50 220 L 250 140 L 450 180 L 600 110 L 800 130" stroke="#FFFFFF" stroke-width="1" stroke-linecap="round" opacity="0.8" />
    
    <!-- Floor reflection grid lines -->
    <line x1="250" y1="140" x2="250" y2="260" stroke="#1F243A" stroke-width="0.75" stroke-dasharray="3,3" />
    <line x1="450" y1="180" x2="450" y2="260" stroke="#1F243A" stroke-width="0.75" stroke-dasharray="3,3" />
    <line x1="600" y1="110" x2="600" y2="260" stroke="#1F243A" stroke-width="0.75" stroke-dasharray="3,3" />

    <!-- 3D Volumetric Signal Spheres -->
    <!-- BUY Signal -->
    <circle cx="450" cy="180" r="9" fill="#00FFA3" filter="url(#neon_glow_green)" />
    <circle cx="450" cy="180" r="4" fill="#FFFFFF" />
    <text x="450" y="160" fill="#00FFA3" font-family="system-ui, sans-serif" font-weight="bold" font-size="10" text-anchor="middle" letter-spacing="1">🟢 BUY ENTRY</text>

    <!-- SELL Signal -->
    <circle cx="600" cy="110" r="9" fill="#FF0055" filter="url(#neon_glow_red)" />
    <circle cx="600" cy="110" r="4" fill="#FFFFFF" />
    <text x="600" y="90" fill="#FF0055" font-family="system-ui, sans-serif" font-weight="bold" font-size="10" text-anchor="middle" letter-spacing="1">🔴 SELL EXIT</text>

    <!-- UI Overlay / HUD Details -->
    <rect x="30" y="25" width="120" height="20" rx="4" fill="#141622" stroke="#2D314C" stroke-width="1"/>
    <circle cx="42" cy="35" r="3" fill="#00FFA3" />
    <text x="52" y="38" fill="#8F94B5" font-family="monospace" font-size="9">SYS STATUS: OK</text>

    <rect x="700" y="25" width="120" height="20" rx="4" fill="#141622" stroke="#2D314C" stroke-width="1"/>
    <text x="760" y="38" fill="#00D2FF" font-family="monospace" font-size="9" text-anchor="middle">TELEMETRY: WebGL</text>

    <!-- Glowing Brand Title -->
    <text x="425" y="60" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="900" font-size="28" text-anchor="middle" letter-spacing="12" filter="url(#neon_glow_cyan)">AETHER-3D QUANT</text>
    <text x="425" y="80" fill="#00D2FF" font-family="system-ui, sans-serif" font-weight="600" font-size="11" text-anchor="middle" letter-spacing="3" opacity="0.9">AI-DRIVEN 3D QUANTITATIVE TELEMETRY SYSTEM</text>
  </svg>
</div>

<br>

<div align="center">

  <!-- PLATFORM BADGES -->
  <img src="https://img.shields.io/badge/System-Institutional--Grade-00FFA3?style=for-the-badge&logo=appveyor&logoColor=black&labelColor=141622" alt="Grade" />
  <img src="https://img.shields.io/badge/Engine-WebGL--GPU--Accelerated-00D2FF?style=for-the-badge&logo=webgl&logoColor=white&labelColor=141622" alt="Engine" />
  <img src="https://img.shields.io/badge/Framework-Streamlit--Plotly-BD00FF?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=141622" alt="Framework" />
  <img src="https://img.shields.io/badge/LICENSE-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=141622" alt="License" />
  <img src="https://img.shields.io/badge/Strategy-EMA--RSI--Crossover-FF9F00?style=for-the-badge&logo=tradingview&logoColor=white&labelColor=141622" alt="Strategy" />

</div>

---

### 🧠 Core Strategy & Telemetry Solution

#### 1. The Quantitative Strategy
At the heart of **Aether-3D Quant** is an adaptive **Exponential Moving Average (EMA) Trend Crossover model** integrated with a **Relative Strength Index (RSI) Momentum Filter**.
* **Trend Inception (EMA 9 & 21)**: The system tracks the exponential moving average of recent close values to isolate structural trend directions. A crossover of the fast 9-period EMA above the slow 21-period EMA indicates potential upward price expansion.
* **Momentum Confirmation (RSI 14)**: To eliminate the false breakouts and "whipsaws" common to moving averages, the engine overlays an RSI indicator. Buy triggers are strictly locked to high-probability oversold regions ($\text{RSI} < 30$), and exit signals are executed at overbought zones ($\text{RSI} > 70$).
* **Risk Protocol Layer**: Every trade is instantly armored with a hard **2.0% Stop-Loss** safety buffer to protect capital and a **5.0% Take-Profit** target boundary to lock in gains at momentum peaks.

#### 2. The Telemetry Solution (Solving the 2D Viewport Limit)
* **The Problem**: Standard 2D chart viewports flatten multiple independent variables (Time, Price, Indicators, and Liquidity) into flat lines. This hides critical geometric correlations at crucial trend transition boundaries.
* **The Solution**: **Aether-3D** resolves this by vectorizing time-series data directly into interactive **3D spatial WebGL coordinates**. By moving price structures, EMA velocity spreads, and momentum vectors along three independent physical axes ($X$, $Y$, $Z$), analysts can visually inspect, rotate, and isolate cluster patterns.

#### 3. Real-Time Data Ingestion Channels
The framework operates with dual data ingestion streams for absolute fidelity:
* **Historical & Backtest Feeds**: Fetched directly from the **Binance Spot REST API** (`https://api.binance.com`) using optimized request limits to build structured data tables and generate offline backtesting metrics.
* **Live Streaming Telemetry**: Connected dynamically via low-latency WebSockets directly to the official **Binance Ticker Feed** (`wss://stream.binance.com:9443/ws/btcusdt@ticker`), streaming sub-second market updates directly into the system telemetry grid.

---

### 🌌 Executive Overview

**AETHER-3D Quant** is a state-of-the-art, institutional-grade quantitative backtesting and algorithmic telemetry framework. Built for developers, researchers, and financial engineers, it turns multi-dimensional market structures into high-fidelity, interactive **3D spatial environments**. 

Traditional 2D charts squeeze high-dimensional market variables into flat lines, hiding critical correlation structures. **AETHER-3D** unlocks the spatial dimension, projecting **Time**, **Price Dynamics**, **Market Momentum (RSI)**, and **Order Book Liquidity** into unified WebGL environments. 

Through standard web engines, it delivers cinematic, GPU-accelerated visualizations, converting abstract trading logic into interactive topographic terrains, spatial trajectories, and volumetric vectors.

---

### 🎨 The 3D Spatial Visualization Arsenal

The system provides five distinct GPU-driven spatial environments designed to isolate and reveal complex correlation patterns in market mechanics.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        3D VISUALIZATION ENGINE                         │
├────────────────────────────────────────────────────────────────────────┤
│  [1] 3D Price Journey    ⟶ Spatial price-time-momentum path            │
│  [2] 3D Price Terrain    ⟶ Continuously generated price-valley mesh    │
│  [3] 3D Candlestick Tower ⟶ Extruded volumetric price towers            │
│  [4] 3D Volume Activity  ⟶ 3D volumetric liquidity coordinates         │
│  [5] 3D Signal Overview  ⟶ Multi-indicator decision boundary space     │
└────────────────────────────────────────────────────────────────────────┘
```

#### 1️⃣ 3D Price Journey (Time × Price × RSI)
* **Mathematical Concept**: Projects time series data along a continuous spatial vector.
* **The Dimension Matrix**:
  * **X-Axis (Depth)**: Time series vector (Timeline progression).
  * **Y-Axis (Altitude)**: Asset Price Index.
  * **Z-Axis (Latitude)**: RSI Momentum Vector (0 to 100).
  * **Surface Color-Mapping**: Dynamically maps color to the continuous gradient of the RSI vector (using a high-contrast `RdYlGn_r` scale where deep green signals extreme oversold momentum and glowing red represents extreme overbought zones).
* **Reference Shaders**: Embeds two transparent horizontal bounding surfaces representing the **Oversold Boundary (RSI = 30)** and **Overbought Boundary (RSI = 70)**, highlighting breakout signals instantly.

#### 2️⃣ 3D Mountain Terrain (Price Surface Landscape)
* **Mathematical Concept**: Translates asset price history into a continuous topological field.
* **Topographical Mapping**: Generates a custom 3D mesh by extruding the closing price across a lateral width grid, applying custom Gaussian white noise perturbations to the boundaries to visualize volatility spreads as a jagged valley landscape.
* **Visual Insight**: Allows quant researchers to view price history as a physical physical landscape—peaks represent historical structural resistance and valleys signify support baselines.

#### 3️⃣ 3D Candlestick Towers
* **Mathematical Concept**: Extrudes classical financial data into volumetric 3D geometric shapes (Mesh3d).
* **Volumetric Mesh Construction**: Renders 3D rectangular cuboids representing daily candlesticks:
  * **Vertical Extrusion Range**: Renders the vertical limits from Open to Close prices.
  * **Color Code**: Cybernetic Lime Green for bullish expansions; Neon Red for bearish compressions.
  * **Trend Alignment Overlay**: Projects dynamic 3D paths for fast (EMA-9) and slow (EMA-21) trend lines, sweeping through the cuboid fields.

#### 4️⃣ 3D Volume Activity Bars
* **Mathematical Concept**: Translates asset liquidity flow into dynamic volumetric columns.
* **Volume Extrusion**: Generates high-density vertical bars, where bar height represents total asset trading volume.
* **Momentum Correlation**: Colors the columns based on the day's positive/negative close-open delta. This isolates high-volume institutional buying pressure from quiet consolidations.

#### 5️⃣ 3D Signal Overview (All-in-One Multi-Model space)
* **Mathematical Concept**: Maps a multi-variable decision boundary space.
* **Vector Coordinates**:
  * **X-Axis**: Time Series Index.
  * **Y-Axis**: EMA Spread Vector ($EMA_9 - EMA_{21}$) representing directional velocity.
  * **Z-Axis**: RSI Value.
* **Visual Core**: Displays every historical point as a colored momentum coordinate. The engine plots large, glowing 3D green diamonds for actual **Executed BUY Signals** and red 3D wireframe 'X' symbols for **Executed SELL Signals**, highlighting the exact mathematical sweet spots of the strategy.

---

### ⚙️ Telemetry System & WebGL Shading Pipeline

The platform uses a GPU-accelerated rendering architecture. The diagram below illustrates how raw time-series data is fetched, processed, and transformed into high-performance interactive shaders:

<!-- 3D PIPELINE DIAGRAM -->
<div align="center">
  <svg width="100%" max-width="800px" height="200px" viewBox="0 0 800 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: #0A0B13; border-radius: 8px; border: 1px solid #232742;">
    <!-- Pipeline Background Grid -->
    <rect width="800" height="200" rx="8" fill="#0A0B13" />
    <path d="M 0 50 L 800 50 M 0 100 L 800 100 M 0 150 L 800 150 M 100 0 L 100 200 M 200 0 L 200 200 M 300 0 L 300 200 M 400 0 L 400 200 M 500 0 L 500 200 M 600 0 L 600 200 M 700 0 L 700 200" stroke="#16182C" stroke-width="0.5"/>
    
    <!-- Flow Connector Lines -->
    <path d="M 180 100 L 260 100 M 440 100 L 520 100" stroke="#00FFA3" stroke-width="2.5" stroke-dasharray="4,4" />
    <path d="M 350 100 H 350" stroke="#00D2FF" stroke-width="2" />
    
    <!-- Step 1 Node -->
    <rect x="30" y="60" width="150" height="80" rx="6" fill="#14172B" stroke="#00D2FF" stroke-width="1.5" />
    <text x="105" y="85" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="bold" font-size="12" text-anchor="middle">1. TELEMETRY STREAM</text>
    <text x="105" y="105" fill="#8F94B5" font-family="monospace" font-size="9" text-anchor="middle">Binance API (REST/WS)</text>
    <text x="105" y="120" fill="#00D2FF" font-family="monospace" font-size="9" text-anchor="middle">BTCUSDT Real-time</text>
    
    <!-- Step 2 Node -->
    <rect x="270" y="60" width="170" height="80" rx="6" fill="#14172B" stroke="#00FFA3" stroke-width="1.5" />
    <text x="355" y="85" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="bold" font-size="12" text-anchor="middle">2. VECTORIZATION ENGINE</text>
    <text x="355" y="105" fill="#8F94B5" font-family="monospace" font-size="9" text-anchor="middle">quant_engine.py</text>
    <text x="355" y="120" fill="#00FFA3" font-family="monospace" font-size="9" text-anchor="middle">Calculates EMA, RSI, PnL</text>
    
    <!-- Step 3 Node -->
    <rect x="530" y="60" width="240" height="80" rx="6" fill="#1B1333" stroke="#BD00FF" stroke-width="1.5" />
    <text x="650" y="85" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="bold" font-size="12" text-anchor="middle">3. GPU SHADER PIPELINE</text>
    <text x="650" y="105" fill="#8F94B5" font-family="monospace" font-size="9" text-anchor="middle">WebGL / Plotly / Three.js</text>
    <text x="650" y="120" fill="#BD00FF" font-family="monospace" font-size="9" text-anchor="middle">Mesh3D &amp; Volumetric Shaders</text>

    <!-- Animated Pointer Triangle -->
    <polygon points="260,95 270,100 260,105" fill="#00FFA3" />
    <polygon points="520,95 530,100 520,105" fill="#BD00FF" />
  </svg>
</div>

---

### 📊 The Core Quantitative Strategy Engine

The default algorithmic framework leverages an adaptive **Exponential Moving Average (EMA) Trend Crossover** model combined with **Relative Strength Index (RSI)** volume and momentum filters. This combination creates highly robust signal filters that screen out false breakouts.

#### Mathematical Formulation

$$\text{EMA}_t = \left( V_t \times \left( \frac{2}{N + 1} \right) \right) + \text{EMA}_{t-1} \times \left( 1 - \frac{2}{N + 1} \right)$$

Where $V_t$ is the current close price and $N \in \{9, 21\}$ represents our window parameters. The Relative Strength Index (RSI) acts as an overbought/oversold oscillator:

$$\text{RS} = \frac{\text{EMA}(\text{U}, 14)}{\text{EMA}(\text{D}, 14)} \implies \text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right)$$

#### Logic Signal Schematic

<!-- STRATEGY BLUEPRINT DIAGRAM -->
<div align="center">
  <svg width="100%" max-width="800px" height="150px" viewBox="0 0 800 150" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: #09090C; border-radius: 8px; border: 1px solid #1E2030;">
    <rect width="800" height="150" rx="8" fill="#09090C" />
    <path d="M 0 37.5 L 800 37.5 M 0 75 L 800 75 M 0 112.5 L 800 112.5 M 100 0 L 100 150 M 200 0 L 200 150 M 300 0 L 300 150 M 400 0 L 400 150 M 500 0 L 500 150 M 600 0 L 600 150 M 700 0 L 700 150" stroke="#161823" stroke-width="0.5" />

    <!-- Trend Condition Gate -->
    <rect x="50" y="35" width="160" height="30" rx="4" fill="#14172B" stroke="#00D2FF" stroke-width="1"/>
    <text x="130" y="53" fill="#00D2FF" font-family="monospace" font-size="10" text-anchor="middle">EMA-9 &gt; EMA-21 (Uptrend)</text>

    <!-- Momentum Gate -->
    <rect x="50" y="85" width="160" height="30" rx="4" fill="#14172B" stroke="#00FFA3" stroke-width="1"/>
    <text x="130" y="103" fill="#00FFA3" font-family="monospace" font-size="10" text-anchor="middle">RSI &lt; 30 (Oversold Filter)</text>

    <!-- Signal Decision Engine -->
    <rect x="330" y="50" width="140" height="50" rx="6" fill="#18152B" stroke="#BD00FF" stroke-width="1.5"/>
    <text x="400" y="74" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="bold" font-size="11" text-anchor="middle">SIGNAL GATE</text>
    <text x="400" y="88" fill="#BD00FF" font-family="monospace" font-size="9" text-anchor="middle">AND Crossover Logic</text>

    <!-- Output Node -->
    <rect x="590" y="55" width="160" height="40" rx="4" fill="#102B20" stroke="#00FFA3" stroke-width="1.5"/>
    <text x="670" y="79" fill="#00FFA3" font-family="system-ui, sans-serif" font-weight="bold" font-size="12" text-anchor="middle">🟢 EXECUTE BUY</text>

    <!-- Connectors -->
    <path d="M 210 50 H 270 V 75 H 330" stroke="#00D2FF" stroke-width="1.5" fill="none" />
    <path d="M 210 100 H 270 V 75 H 330" stroke="#00FFA3" stroke-width="1.5" fill="none" />
    <path d="M 470 75 H 590" stroke="#BD00FF" stroke-width="2" />
    <polygon points="585,71 590,75 585,79" fill="#00FFA3" />
  </svg>
</div>

#### Risk Management Protocol
The engine implements strict risk controls for every active trade:
* **Stop-Loss Protection**: Standard **2.0% hard stop** from the entries to limit downside risks in volatile reversals.
* **Take-Profit Targets**: A **5.0% profit target** to lock in gains at short-term momentum extremes.

---

### 📂 Repository Blueprint & Components

```
.
├── quant_engine.py             # 🧮 Core math engine: fetches API data, calculates EMA/RSI, runs backtests
├── dashboard_enhanced.py      # 🚀 Enhanced dashboard: houses the 5 WebGL 3D visualizations and educational UI
├── dashboard.py               # 📈 Standard lightweight dashboard deployment
├── live_stream.py             # 🔌 WebSocket connector for real-time market data
├── test_3d.html               # 🖥️ Compiled standalone 3D WebGL dashboard (4.8MB full library build)
├── run_dashboard.bat          # ⚡ One-click launcher script for Windows developers
├── requirements.txt           # 📦 Dependency manifest
├── LICENSE                    # 📄 MIT Open Source License
└── README.md                  # 🌌 Futuristic technical overview
```

---

### 🚀 Production Deployment & Installation

Follow these steps to set up the system environment and launch the dynamic analytics telemetry.

#### 1. Pre-requisites & Core Environment Setup
Ensure Python 3.8+ is installed on your workstation. Clone the codebase, navigate to the project directory, and initialize dependencies:

```bash
# Clone the repository
git clone https://github.com/your-username/aether-3d-quant.git

# Navigate into the project boundary
cd aether-3d-quant

# Install vectorized dependencies and visualization packages
pip install -r requirements.txt
```

#### 2. Run the Quantitative Backtest Engine (Command-Line)
Run the backtesting module in the terminal to fetch daily history from Binance and execute the mathematical model:

```bash
python quant_engine.py
```
*Expected Terminal Telemetry:*
```
### FETCHING SYSTEM DATA FROM BINANCE API...
### RUNNING HISTORICAL BACKTEST ON BTCUSDT...
Backtest complete. Total Profit: -$428.27
```

#### 3. Launch the WebGL Telemetry Dashboard
Start the local server. The dashboard will automatically launch in your browser at `http://localhost:8501`:

```bash
# Direct Streamlit launch
streamlit run dashboard_enhanced.py
```
*Windows developer shortcut:*
```bash
# Run via bat launcher
run_dashboard.bat
```

#### 4. Stream Live Market Data via WebSockets
To test real-time data streaming from Binance tickers directly to your console, run:

```bash
python live_stream.py
```

#### 5. Offline Standalone 3D Engine
Open `test_3d.html` directly in any modern WebGL-compliant web browser. This 4.8MB compiled file runs entirely offline and provides deep, high-fidelity interaction with pre-rendered strategy path environments.

---

### 🗺️ Future Roadmap

```
  PHASE 1: GPU CORE SHADERS ──────────────────────────► Completed
  • WebGL 3D Spatial Trajectories rendered via Plotly Mesh3d.
  • Caching engine for time-series vectorization.

  PHASE 2: DEEP MODEL PERFORMANCE COMPARISON ──────────► In Progress
  • Dual-purpose dashboard extensions to showcase benchmarking of free AI models.
  • Real-time GPU execution speed and accuracy evaluation profiles in 3D.

  PHASE 3: HIGH-FREQUENCY TELEMETRY ──────────────────► Planning
  • Low-latency WebSocket pipelines feeding dynamic 3D WebGL charts.
  • Support for multi-exchange order-book data visualization.
```

---

### 👥 Contribution & Guidelines

AETHER-3D Quant is an open-source research initiative. We welcome enhancements to our spatial math engines:
1. **Fork the Repository** to your workspace.
2. **Implement enhancements** (such as custom WebGL shaders, alternative indicators, or AI benchmarks).
3. **Ensure strict compatibility**: Maintain the standalone structure of `test_3d.html`.
4. **Submit a Pull Request** with detailed documentation of your math engine enhancements.

---

### 📄 License Compliance

This project is officially released under the **MIT License**. It grants full permissions for modification, distribution, and commercial applications, provided the original copyright is kept.

> [!CAUTION]
> **Financial Disclaimer**: Algorithmic trading involves substantial risk of loss. The strategy and analytics displayed by AETHER-3D Quant are designed for academic, research, and educational purposes only. Past backtesting performance does not guarantee future results.

---

<div align="center">
  <sub>Developed by <b>pagad</b> | Powered by WebGL, Plotly &amp; Streamlit</sub>
</div>
