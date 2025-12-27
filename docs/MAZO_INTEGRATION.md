# Mazo Integration Guide

This document describes the integration between **AI Hedge Fund** and **Mazo**, two complementary AI-powered financial analysis systems.

## Table of Contents

1. [Overview](#overview)
2. [System Comparison](#system-comparison)
3. [Integration Architecture](#integration-architecture)
4. [Integration Patterns](#integration-patterns)
5. [Setup Guide](#setup-guide)
6. [LLM Proxy Configuration](#llm-proxy-configuration)
7. [Alpaca Trading Integration](#alpaca-trading-integration)
8. [Web UI Integration](#web-ui-integration)
9. [API Bridge](#api-bridge)
10. [Unified Workflow](#unified-workflow)
11. [Configuration](#configuration)
12. [Usage Examples](#usage-examples)
13. [Troubleshooting](#troubleshooting)

---

## Overview

### What is AI Hedge Fund?

AI Hedge Fund is a multi-agent trading signal generator that simulates how legendary investors would analyze stocks. It uses 18 specialized agents (Warren Buffett, Michael Burry, Cathie Wood, etc.) to generate BUY/SELL/HOLD signals with confidence scores.

**Key Features:**
- 12 investor persona agents + 4 analysis agents + 2 management agents
- Valuation analysis (DCF, Owner Earnings, EV/EBITDA)
- Technical analysis (momentum, mean reversion, volatility)
- Sentiment analysis (news, insider trading)
- Risk management with position sizing
- Backtesting capability
- Web UI for visual workflow building

### What is Mazo?

Mazo is an autonomous financial research agent that thinks, plans, and learns as it works. It's designed for deep, open-ended financial research questions.

**Key Features:**
- Multi-agent architecture (Planning, Action, Validation, Answer agents)
- Autonomous task decomposition
- Self-validation and iterative refinement
- Deep financial analysis with real-time data
- Natural language Q&A interface
- Safety mechanisms (loop detection, execution limits)

### Why Integrate Them?

| AI Hedge Fund | Mazo |
|---------------|------|
| Answers: "What should I do?" | Answers: "Why is this happening?" |
| Output: Trading signals | Output: Research reports |
| Structured decisions | Open-ended exploration |
| Quantitative focus | Qualitative + Quantitative |

**Together they provide:**
- Signal generation WITH deep research justification
- Better-informed agent decisions
- Complete due diligence workflow
- Actionable insights backed by thorough analysis

---

## System Comparison

### Architecture Comparison

```
AI HEDGE FUND                          MAZO
─────────────────────────────────────────────────────────────────
┌─────────────────────┐               ┌─────────────────────┐
│   12 Investor       │               │   Planning Agent    │
│   Persona Agents    │               │   (Task Decomp)     │
│   ├─ Buffett        │               └──────────┬──────────┘
│   ├─ Burry          │                          │
│   ├─ Graham         │               ┌──────────▼──────────┐
│   ├─ Lynch          │               │   Action Agent      │
│   ├─ Munger         │               │   (Tool Selection)  │
│   ├─ Wood           │               └──────────┬──────────┘
│   ├─ Ackman         │                          │
│   ├─ Fisher         │               ┌──────────▼──────────┐
│   ├─ Damodaran      │               │   Validation Agent  │
│   ├─ Druckenmiller  │               │   (Self-Check)      │
│   ├─ Pabrai         │               └──────────┬──────────┘
│   └─ Jhunjhunwala   │                          │
└──────────┬──────────┘               ┌──────────▼──────────┐
           │                          │   Answer Agent      │
┌──────────▼──────────┐               │   (Synthesis)       │
│   4 Analysis Agents │               └─────────────────────┘
│   ├─ Fundamentals   │
│   ├─ Technical      │
│   ├─ Sentiment      │
│   └─ Valuation      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   2 Management      │
│   ├─ Risk Manager   │
│   └─ Portfolio Mgr  │
└─────────────────────┘
```

### Technology Stack Comparison

| Component | AI Hedge Fund | Mazo |
|-----------|---------------|------|
| Language | Python | TypeScript |
| Runtime | Python 3.11+ | Bun |
| LLM Framework | LangChain (Python) | LangChain.js |
| UI | React + FastAPI | React + Ink (Terminal) |
| Data Source | Financial Datasets API | Financial Datasets API |
| LLM Access | Via Proxy | Via Proxy |

### Shared Components

Both systems share:
- **Single `.env` configuration** in the project root
- **OpenAI-compatible LLM proxy** for all model requests
- **Financial Datasets API** for market data
- **Same API key** for LLM access

---

## Integration Architecture

### High-Level Architecture

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
│  │  • Deep research            │             │  • Signal generation        │
│  │  • Thesis investigation     │             │  • Multi-agent analysis     │
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

---

## Integration Patterns

### Pattern 1: Pre-Decision Research

```
User Query → Mazo Research → Context Injection → AI HF Decision
```

Mazo researches a company first, then passes findings to AI Hedge Fund agents.

### Pattern 2: Post-Signal Deep Dive

```
User Query → AI HF Signal → Mazo Explanation
```

AI Hedge Fund generates a signal, then Mazo provides detailed justification.

### Pattern 3: Agent-Specific Research

```
Agent Request → Mazo Tailored Research → Agent Decision
```

Individual AI Hedge Fund agents request specific research from Mazo.

---

## Setup Guide

### Prerequisites

1. **Python 3.11+** - Install via Homebrew: `brew install python@3.13`
2. **Poetry** - Install via pipx: `pipx install poetry`
3. **Bun runtime** - Install via: `curl -fsSL https://bun.sh/install | bash`
4. **API keys**:
   - OpenAI-compatible proxy API key
   - Financial Datasets API key

### Installation

```bash
# Clone the repository
git clone https://github.com/vitalemazo/mazo-hedge-fund.git
cd mazo-hedge-fund

# Install Python dependencies
poetry install

# Set Poetry to use Python 3.13 (recommended)
poetry env use python3.13

# Install Mazo dependencies
cd mazo
bun install
cd ..
```

### Quick Start

```bash
# Run research on a stock
poetry run python -m integration.unified_workflow --tickers AAPL --mode research --depth quick

# Run full analysis (research + signals)
poetry run python -m integration.unified_workflow --tickers AAPL --mode full
```

---

## LLM Proxy Configuration

Both AI Hedge Fund and Mazo are designed to work with an **OpenAI-compatible LLM proxy**. This is the recommended setup as it provides:

- **Unified access** to multiple LLM providers (Claude, GPT, Gemini, etc.)
- **Single API key** for all models
- **Cost tracking** and rate limiting
- **Seamless switching** between models

### Setting Up the Proxy

Create a `.env` file in the project root:

```bash
# ===========================================
# LLM PROXY CONFIGURATION (Recommended)
# ===========================================
# All LLM requests route through this endpoint
OPENAI_API_KEY=sk-your-proxy-api-key
OPENAI_API_BASE=https://api.your-proxy-service.com/v1

# ===========================================
# FINANCIAL DATA API (Required)
# ===========================================
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# ===========================================
# WEB SEARCH (Optional)
# ===========================================
TAVILY_API_KEY=your-tavily-api-key

# ===========================================
# MAZO INTEGRATION
# ===========================================
MAZO_PATH=/path/to/mazo-hedge-fund/mazo
MAZO_TIMEOUT=300
DEFAULT_WORKFLOW_MODE=full
DEFAULT_RESEARCH_DEPTH=standard
```

### How Proxy Routing Works

When `OPENAI_API_BASE` is set:

1. **All models route through the proxy** - Claude, GPT, Gemini all use the same endpoint
2. **Single API key** - Only `OPENAI_API_KEY` is needed
3. **Model passthrough** - The model name (e.g., `claude-sonnet-4-5-20250929`) is passed directly to the proxy
4. **Provider routing** - The proxy handles routing to the correct LLM provider

**Default model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)

### Direct API Access (Alternative)

If you prefer not to use a proxy:

```bash
# Direct provider keys (no proxy)
ANTHROPIC_API_KEY=your-anthropic-api-key  # For Claude models
OPENAI_API_KEY=your-openai-api-key        # For GPT models
GOOGLE_API_KEY=your-google-api-key        # For Gemini models
```

---

## Alpaca Trading Integration

The system integrates with [Alpaca Markets](https://alpaca.markets/) to execute trades based on AI-generated signals. This enables the complete workflow from research to execution.

### Trading Flow

```
1. USER REQUEST
   └── poetry run python -m integration.unified_workflow --tickers AAPL --execute

2. MAZO RESEARCH (optional)
   └── Deep analysis of company fundamentals

3. AI HEDGE FUND ANALYSIS
   ├── 18 agents analyze the stock
   ├── Each agent provides: Signal (BULLISH/BEARISH/NEUTRAL) + Confidence %
   └── Risk Manager calculates position limits

4. PORTFOLIO MANAGER DECISION
   ├── Aggregates all agent signals
   ├── Determines action: BUY, SELL, SHORT, COVER, or HOLD
   └── Calculates quantity based on risk limits

5. ALPACA EXECUTION
   ├── Connects to Alpaca API (paper or live)
   ├── Submits order (market order by default)
   └── Reports execution status

6. RESULT
   └── Order ID, filled price, updated positions
```

### Setup Alpaca

1. **Create Account**: Go to [https://app.alpaca.markets/](https://app.alpaca.markets/)
2. **Generate API Keys**: Navigate to Paper Trading → API Keys
3. **Configure Environment**:

```bash
# Add to .env file
ALPACA_API_KEY=PKXXXXXXXXXXXXXXXXXX
ALPACA_SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_TRADING_MODE=paper
```

### Trading Commands

```bash
# Analyze only (no trading)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal

# Dry run (preview trades)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --dry-run

# Execute paper trades
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal --execute

# Full workflow with research + trading
poetry run python -m integration.unified_workflow --tickers AAPL --mode full --execute

# Multiple tickers
poetry run python -m integration.unified_workflow --tickers AAPL MSFT GOOGL --mode signal --execute
```

### Supported Actions

| Action | Description | When Used |
|--------|-------------|-----------|
| BUY | Purchase shares (go long) | Bullish signal |
| SELL | Sell existing long position | Bearish signal on long |
| SHORT | Sell shares you don't own | Bearish signal |
| COVER | Buy back shorted shares | Bullish signal on short |
| HOLD | No action | Neutral signal or low confidence |

### Risk Management

The system includes built-in protections:

| Protection | Description |
|------------|-------------|
| Position Limits | Maximum position size based on volatility |
| Confidence Threshold | Low confidence signals default to HOLD |
| Paper Trading Default | Uses paper trading unless explicitly configured |
| Dry Run Mode | Preview trades before executing |

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

### Python API

```python
from src.trading.alpaca_service import AlpacaService

alpaca = AlpacaService()

# Check account
account = alpaca.get_account()
print(f"Buying Power: ${account.buying_power:,.2f}")

# Execute trades
result = alpaca.buy("AAPL", qty=10)
result = alpaca.sell("AAPL", qty=5)
result = alpaca.short("AAPL", qty=10)
result = alpaca.cover("AAPL", qty=10)

# Get positions
positions = alpaca.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.qty} shares, P/L: ${pos.unrealized_pl:.2f}")
```

For complete trading documentation, see [TRADING.md](TRADING.md).

---

## Web UI Integration

The web application includes Mazo research capabilities directly in the interface.

### Starting the Web App

```bash
cd app
./run.sh   # macOS/Linux
# or
run.bat    # Windows
```

### Research Tab

The bottom panel includes a **Research** tab where you can:

- Ask natural language research questions
- Analyze companies in depth
- Compare multiple companies
- Get real-time research with confidence scores

```
┌─────────────────────────────────────────────────────────────────┐
│  Output  │  Research                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Research Depth: [Standard ▼]     [Analyze] [Compare] [Clear]   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ You: What's driving NVDA's growth?                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Mazo: NVIDIA's growth is driven by several key factors:  │   │
│  │ 1. AI/ML demand for GPUs...                              │   │
│  │ 2. Data center expansion...                              │   │
│  │ [85% confidence] [Sources: SEC filings, earnings calls]  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [Ask a research question...]                          [Send]   │
└─────────────────────────────────────────────────────────────────┘
```

### Signal Explanation

After running a workflow, each trading signal in the Output tab has an **Explain** button:

| Ticker | Action | Quantity | Confidence | Research |
|--------|--------|----------|------------|----------|
| AAPL   | BUY    | 100      | 85%        | [Explain] |
| MSFT   | HOLD   | 0        | 72%        | [Explain] |

Clicking **Explain** will:
1. Switch to the Research tab
2. Send the signal details to Mazo
3. Display a detailed explanation of why the signal was generated

### Research Depth Options

| Depth | Description | Use Case |
|-------|-------------|----------|
| Quick | Brief overview, key metrics | Fast decisions, screening |
| Standard | Comprehensive analysis | Normal research |
| Deep | Exhaustive research with scenarios | Due diligence |

### Backend API Endpoints

The web UI uses these REST endpoints:

#### Core Research
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mazo/research` | POST | Execute natural language research query |
| `/mazo/research/stream` | POST | Streaming research with SSE events |
| `/mazo/analyze` | POST | Comprehensive company analysis |
| `/mazo/compare` | POST | Compare multiple companies |
| `/mazo/explain-signal` | POST | Explain a trading signal |
| `/mazo/pre-research` | POST | Pre-workflow context gathering |

#### Templates & Batch Processing
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mazo/templates` | GET | List available research templates |
| `/mazo/research/template` | POST | Research using a predefined template |
| `/mazo/batch` | POST | Batch analyze multiple tickers |

#### Health
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mazo/health` | GET | Service health check |

### Available Research Templates

| Template ID | Name | Use Case |
|-------------|------|----------|
| `fundamental_analysis` | Fundamental Analysis | Deep dive into financials |
| `technical_analysis` | Technical Analysis | Chart patterns and price action |
| `risk_assessment` | Risk Assessment | Identify risks and downsides |
| `growth_catalyst` | Growth Catalysts | Upcoming events and catalysts |
| `competitor_analysis` | Competitor Analysis | Compare against competitors |
| `earnings_preview` | Earnings Preview | Pre-earnings analysis |
| `sector_overview` | Sector Overview | Industry dynamics |
| `quick_summary` | Quick Summary | Fast 2-minute overview |

---

## API Bridge

The `MazoBridge` class provides Python access to Mazo:

```python
from integration.mazo_bridge import MazoBridge

bridge = MazoBridge()

# Basic research
response = bridge.research("What is AAPL's competitive moat?")

# Company analysis
response = bridge.analyze_company("AAPL")

# Compare companies
response = bridge.compare_companies(["AAPL", "MSFT", "GOOGL"])

# Explain a signal
response = bridge.explain_signal(
    ticker="AAPL",
    signal="BULLISH",
    confidence=85.0,
    reasoning="Strong competitive position"
)

# Agent-specific context
response = bridge.get_agent_context("AAPL", "buffett")
```

---

## Unified Workflow

Run integrated analysis via CLI:

```bash
# Full workflow (Mazo research + AI HF signal + Mazo explanation)
poetry run python -m integration.unified_workflow --tickers AAPL --mode full

# Pre-research mode (Mazo first, then AI HF)
poetry run python -m integration.unified_workflow --tickers AAPL --mode pre-research

# Post-research mode (AI HF first, then Mazo explains)
poetry run python -m integration.unified_workflow --tickers AAPL --mode post-research

# Signal only (just AI Hedge Fund)
poetry run python -m integration.unified_workflow --tickers AAPL --mode signal

# Research only (just Mazo)
poetry run python -m integration.unified_workflow --tickers AAPL --mode research

# Multiple tickers
poetry run python -m integration.unified_workflow --tickers AAPL,MSFT,GOOGL --mode research
```

---

## Configuration

### Environment Variables

#### LLM Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for LLM proxy | Required |
| `OPENAI_API_BASE` | LLM proxy endpoint URL | Required for proxy |
| `ANTHROPIC_API_KEY` | Direct Anthropic API key | Optional |

#### Financial Data

| Variable | Description | Default |
|----------|-------------|---------|
| `FINANCIAL_DATASETS_API_KEY` | Financial data API key | Required |
| `TAVILY_API_KEY` | Web search API key | Optional |

#### Alpaca Trading

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPACA_API_KEY` | Alpaca API key | Required for trading |
| `ALPACA_SECRET_KEY` | Alpaca secret key | Required for trading |
| `ALPACA_BASE_URL` | Alpaca API endpoint | `https://paper-api.alpaca.markets/v2` |
| `ALPACA_TRADING_MODE` | Trading mode (paper/live) | `paper` |

#### Mazo Integration

| Variable | Description | Default |
|----------|-------------|---------|
| `MAZO_PATH` | Path to Mazo installation | `./mazo` |
| `MAZO_TIMEOUT` | Query timeout in seconds | `300` |
| `DEFAULT_WORKFLOW_MODE` | Default workflow mode | `full` |
| `DEFAULT_RESEARCH_DEPTH` | Research depth (quick/standard/deep) | `standard` |

### Research Depth Levels

- **quick**: Brief overview, key metrics (~30 seconds)
- **standard**: Comprehensive analysis with valuation (~1-2 minutes)
- **deep**: Exhaustive research with scenarios (~3-5 minutes)

---

## Usage Examples

### Example 1: Quick Research

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode research \
  --depth quick
```

### Example 2: Full Analysis with Multiple Tickers

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL MSFT GOOGL \
  --mode full \
  --depth standard
```

### Example 3: Signal Generation with Paper Trading

```bash
# Preview trades (dry run)
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --dry-run

# Execute paper trades
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --execute
```

### Example 4: Full Workflow with Trading Execution

```bash
# Research + Signal + Trading
poetry run python -m integration.unified_workflow \
  --tickers AAPL MSFT GOOGL NVDA \
  --mode full \
  --depth standard \
  --execute
```

### Example 5: Python Integration

```python
from integration.unified_workflow import UnifiedWorkflow, WorkflowMode, execute_trades

workflow = UnifiedWorkflow()
results = workflow.analyze(
    tickers=["AAPL", "MSFT"],
    mode=WorkflowMode.SIGNAL_ONLY,
)

# Preview signals
for result in results:
    print(f"{result.ticker}: {result.signal} ({result.confidence}%)")
    if result.recommended_action:
        print(f"  Recommendation: {result.recommended_action} {result.recommended_quantity} shares")

# Execute trades
results = execute_trades(results, dry_run=False)

# Check trade results
for result in results:
    if result.trade and result.trade.executed:
        print(f"{result.ticker}: Executed {result.trade.action} {result.trade.quantity} shares")
        print(f"  Order ID: {result.trade.order_id}")
```

### Example 6: Interactive Mazo Terminal

```bash
cd mazo
bun start
```

Then ask questions like:
- "Compare Microsoft and Google's operating margins for 2023"
- "What's driving NVIDIA's growth?"
- "Analyze Tesla's cash flow trends"

---

## Troubleshooting

### Schema Validation Warnings

When using a proxy, you may see warnings like:
```
Schema validation warning: Invalid option: expected one of "ticker"|"date"|...
```

**These warnings are normal and can be safely ignored.** They occur because:
- Proxies don't support OpenAI's native structured output format
- Mazo uses JSON prompting as a fallback
- The code handles this gracefully and continues working

### Python Version Issues

If you see:
```
The currently activated Python version 3.9.6 is not supported by the project (^3.11)
```

Fix by setting Poetry to use Python 3.13:
```bash
poetry env use python3.13
poetry install
```

### Mazo Not Found

If the bridge can't find Mazo:
1. Verify `MAZO_PATH` in your `.env` points to the correct directory
2. Ensure Bun is installed: `bun --version`
3. Ensure Mazo dependencies are installed: `cd mazo && bun install`

### LLM Timeouts

For complex queries that timeout:
1. Increase `MAZO_TIMEOUT` in `.env` (default: 300 seconds)
2. Use `--depth quick` for faster responses
3. Break complex queries into smaller questions

### Alpaca Connection Issues

**Error:** `Alpaca API credentials not found`

1. Verify your `.env` file contains:
```bash
ALPACA_API_KEY=your-key
ALPACA_SECRET_KEY=your-secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
```

2. Check credentials are valid at [https://app.alpaca.markets/](https://app.alpaca.markets/)

### Trading Order Rejected

**Error:** `insufficient buying power`

Check account balance:
```python
from src.trading.alpaca_service import AlpacaService
alpaca = AlpacaService()
account = alpaca.get_account()
print(f"Buying Power: ${account.buying_power:,.2f}")
```

**Error:** `market is not open`

Orders will be queued for next market open. Use `--dry-run` to preview trades outside market hours.

### Trading Documentation

For complete trading documentation, troubleshooting, and API reference, see [TRADING.md](TRADING.md).

---

## Author

**Vitale Mazo**
