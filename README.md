# Mazo Hedge Fund

An AI-powered hedge fund that combines multi-agent trading signal generation with autonomous financial research and **live trading on Alpaca**.

## Overview

This system combines three powerful components:

1. **AI Hedge Fund** - Multi-agent trading signal generator with 18 specialized agents
2. **Mazo** - Autonomous financial research agent for deep analysis
3. **Alpaca Trading** - Live and paper trading execution on Alpaca Markets

The system analyzes stocks using AI agents inspired by legendary investors, generates trading signals, and can execute trades automatically on Alpaca.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        UNIFIED TRADING SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐         ┌─────────────────────────────────────────────┐   │
│  │   USER      │         │            ORCHESTRATOR                     │   │
│  │  Request    │────────▶│  (unified_workflow.py)                      │   │
│  └─────────────┘         │  • Routes requests to appropriate system    │   │
│                          │  • Manages data flow between systems        │   │
│                          │  • Aggregates results                       │   │
│                          │  • Executes trades on Alpaca                │   │
│                          └─────────────────────────────────────────────┘   │
│                                            │                               │
│                    ┌───────────────────────┴───────────────────────┐       │
│                    │                                               │       │
│                    ▼                                               ▼       │
│  ┌─────────────────────────────┐             ┌─────────────────────────────┐
│  │         MAZO               │             │      AI HEDGE FUND          │
│  │    (Research Engine)        │◀───────────▶│    (Decision Engine)        │
│  │                             │   Context   │                             │
│  │  • Deep research            │             │  • 18 analyst agents        │
│  │  • Thesis investigation     │             │  • Signal generation        │
│  │  • Explanation generation   │             │  • Risk management          │
│  └──────────────┬──────────────┘             └──────────────┬──────────────┘
│                 │                                           │               │
│                 └─────────────────┬─────────────────────────┘               │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │      ALPACA TRADING         │                          │
│                    │  • Paper trading mode       │                          │
│                    │  • Live trading mode        │                          │
│                    │  • Order execution          │                          │
│                    │  • Position management      │                          │
│                    └─────────────────────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Trading Agents

| # | Agent | Strategy |
|---|-------|----------|
| 1 | Warren Buffett | Wonderful companies at fair prices, competitive moats |
| 2 | Benjamin Graham | Deep value, margin of safety, Graham Number |
| 3 | Michael Burry | Contrarian deep value, hidden assets |
| 4 | Charlie Munger | Quality businesses at fair prices |
| 5 | Peter Lynch | Ten-baggers in everyday businesses |
| 6 | Cathie Wood | Disruptive innovation, exponential growth |
| 7 | Bill Ackman | Activist investing, value unlocking |
| 8 | Phil Fisher | Scuttlebutt research, growth investing |
| 9 | Aswath Damodaran | Rigorous DCF valuation |
| 10 | Stanley Druckenmiller | Macro trends, asymmetric opportunities |
| 11 | Mohnish Pabrai | Dhandho investing, low-risk doubles |
| 12 | Rakesh Jhunjhunwala | Growth + value in emerging markets |
| 13 | Valuation Agent | DCF, Owner Earnings, EV/EBITDA analysis |
| 14 | Sentiment Agent | News sentiment, insider trading signals |
| 15 | Fundamentals Agent | Financial statement analysis |
| 16 | Technicals Agent | Technical indicators and patterns |
| 17 | Risk Manager | Position sizing, volatility adjustment |
| 18 | Portfolio Manager | Final trading decisions |

### Mazo Research Agent

Mazo is an autonomous financial research agent that:
- Takes complex financial questions and turns them into step-by-step research plans
- Executes research tasks using live market data
- Validates its own work and refines results
- Provides data-backed answers with confidence scores

See [docs/MAZO_INTEGRATION.md](docs/MAZO_INTEGRATION.md) for detailed documentation.

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results
- Paper trading is recommended for testing

By using this software, you agree to use it solely for learning purposes.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Trading with Alpaca](#trading-with-alpaca)
- [Workflow Examples](#workflow-examples)
- [License](#license)

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/vitalemazo/mazo-hedge-fund.git
cd mazo-hedge-fund
poetry install
cd mazo && bun install && cd ..

# 2. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 3. Run analysis (no trading)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal

# 4. Run analysis + paper trading
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --execute
```

## Installation

### Prerequisites

- Python 3.11+
- Bun runtime (for Mazo)
- API keys (see Configuration)

### Step 1: Clone Repository

```bash
git clone https://github.com/vitalemazo/mazo-hedge-fund.git
cd mazo-hedge-fund
```

### Step 2: Install Python Dependencies

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### Step 3: Install Mazo Dependencies

```bash
# Install Bun (if not already installed)
curl -fsSL https://bun.sh/install | bash

# Install Mazo dependencies
cd mazo
bun install
cd ..
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys (see Configuration section).

## Configuration

Create a `.env` file with the following configuration:

```bash
# ===========================================
# FINANCIAL DATA API (Required)
# ===========================================
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# ===========================================
# LLM CONFIGURATION (Required)
# ===========================================
# Option 1: OpenAI-compatible proxy (recommended)
OPENAI_API_KEY=your-proxy-api-key
OPENAI_API_BASE=https://your-proxy.com/v1

# Option 2: Direct Anthropic API
# ANTHROPIC_API_KEY=your-anthropic-api-key

# ===========================================
# ALPACA TRADING API (Required for trading)
# ===========================================
# Get your API keys from https://app.alpaca.markets/
ALPACA_API_KEY=your-alpaca-api-key
ALPACA_SECRET_KEY=your-alpaca-secret-key

# Paper trading (recommended for testing)
ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_TRADING_MODE=paper

# Live trading (use with caution!)
# ALPACA_BASE_URL=https://api.alpaca.markets/v2
# ALPACA_TRADING_MODE=live

# ===========================================
# MAZO INTEGRATION
# ===========================================
MAZO_PATH=/path/to/mazo-hedge-fund/mazo
MAZO_TIMEOUT=300
DEFAULT_WORKFLOW_MODE=full
DEFAULT_RESEARCH_DEPTH=standard

# ===========================================
# WEB SEARCH (Optional)
# ===========================================
TAVILY_API_KEY=your-tavily-api-key
```

### Getting API Keys

| Service | URL | Purpose |
|---------|-----|---------|
| Financial Datasets | https://financialdatasets.ai/ | Market data |
| Alpaca | https://app.alpaca.markets/ | Trading execution |
| OpenAI | https://platform.openai.com/ | LLM (if not using proxy) |
| Anthropic | https://console.anthropic.com/ | LLM (Claude models) |
| Tavily | https://tavily.com/ | Web search (optional) |

## Trading with Alpaca

### Paper Trading (Recommended for Testing)

Paper trading uses virtual money to simulate real trading:

```bash
# Analyze and execute paper trades
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --execute

# Dry run (show what would be traded without executing)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --dry-run
```

### Trading Flow

```
1. USER REQUEST
   └── poetry run python -m integration.unified_workflow --tickers AAPL --execute

2. AI HEDGE FUND ANALYSIS
   ├── 18 agents analyze the stock
   ├── Each agent provides: Signal (BULLISH/BEARISH/NEUTRAL) + Confidence %
   └── Risk Manager calculates position limits

3. PORTFOLIO MANAGER DECISION
   ├── Aggregates all agent signals
   ├── Determines action: BUY, SELL, SHORT, COVER, or HOLD
   └── Calculates quantity based on risk limits

4. ALPACA EXECUTION
   ├── Connects to Alpaca API (paper or live)
   ├── Submits order (market order by default)
   └── Reports execution status

5. RESULT
   └── Order ID, filled price, updated positions
```

### Example Output

```
============================================================
ALPACA TRADING EXECUTION
============================================================
Account Status: ACTIVE
Mode: PAPER
Buying Power: $10,000.00
Cash: $5,000.00
============================================================

[AAPL] Executing: SHORT 91 shares...
[AAPL] SUCCESS: Order cefb3813-e0e8-4e2a-8de0-d6f7b46c5392

============================================================
CURRENT POSITIONS
============================================================
  AAPL: -91 shares @ $254.32
    Current: $253.50 | P/L: +$74.62 (+0.3%)
============================================================
```

### Trading Commands

```bash
# Signal-only analysis (no trading)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal

# Dry run (preview trades)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --dry-run

# Execute paper trades
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --execute

# Full workflow with Mazo research + trading
poetry run python -m integration.unified_workflow --tickers AAPL --mode full --execute

# Multiple tickers
poetry run python -m integration.unified_workflow --tickers AAPL MSFT GOOGL --mode signal --execute
```

### Direct Trading API

You can also use the Alpaca service directly:

```python
from src.trading.alpaca_service import AlpacaService

# Initialize
alpaca = AlpacaService()

# Check account
account = alpaca.get_account()
print(f"Buying Power: ${account.buying_power:,.2f}")

# Buy shares
result = alpaca.buy("AAPL", qty=10)
if result.success:
    print(f"Order placed: {result.order.id}")

# Sell shares
result = alpaca.sell("AAPL", qty=5)

# Short sell
result = alpaca.short("AAPL", qty=10)

# Cover short
result = alpaca.cover("AAPL", qty=10)

# Get positions
positions = alpaca.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.qty} shares, P/L: ${pos.unrealized_pl:.2f}")

# Get orders
orders = alpaca.get_orders(status="open")
```

## Workflow Examples

### Example 1: Quick Analysis (No Trading)

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal
```

Output:
```
SIGNAL: BEARISH (75% confidence)

AGENT SIGNALS:
  - Warren Buffett: NEUTRAL (65%) - "Great business, wrong price"
  - Valuation Analyst: BEARISH (100%) - "72% above intrinsic value"
  - Growth Analyst: BEARISH (82%) - "PEG ratio 2.5 is expensive"

RECOMMENDATIONS:
  - Recommended action: SHORT 91 shares
```

### Example 2: Full Workflow with Research

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode full \
  --depth standard
```

This runs:
1. **Mazo Research** - Initial company analysis
2. **AI Hedge Fund** - 18 agents generate signals
3. **Mazo Explanation** - Deep dive on the trading decision

### Example 3: Paper Trading Execution

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL MSFT GOOGL \
  --mode signal \
  --execute
```

This will:
1. Analyze all three stocks
2. Generate trading signals for each
3. Execute trades on Alpaca paper trading

### Example 4: Research Only (No Signals)

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode research \
  --depth deep
```

### Example 5: Export to Markdown

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode full \
  --output markdown \
  --output-file analysis.md
```

### Example 6: Backtesting

```bash
poetry run python src/backtester.py \
  --ticker AAPL,MSFT,NVDA \
  --start-date 2024-01-01 \
  --end-date 2024-12-01 \
  --initial-capital 100000
```

## Web Application

Start the web application for a visual interface:

```bash
cd app
./run.sh  # macOS/Linux
```

See [app/README.md](app/README.md) for details.

## Documentation

- [Mazo Integration Guide](docs/MAZO_INTEGRATION.md) - Detailed integration documentation
- [Trading Guide](docs/TRADING.md) - Alpaca trading documentation
- [API Reference](docs/API.md) - REST API documentation

## Author

**Vitale Mazo**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
