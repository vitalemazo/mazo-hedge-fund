# Alpaca Trading Guide

This document covers how to use the Alpaca trading integration with the Mazo Hedge Fund system.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Trading Modes](#trading-modes)
4. [Workflow Integration](#workflow-integration)
5. [Direct API Usage](#direct-api-usage)
6. [Order Types](#order-types)
7. [Position Management](#position-management)
8. [Risk Management](#risk-management)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The trading system integrates with [Alpaca Markets](https://alpaca.markets/) to execute trades based on AI-generated signals. The workflow is:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Input    │────▶│   AI Analysis   │────▶│ Portfolio Mgr   │────▶│ Alpaca Trading  │
│  (--tickers)    │     │  (18 Agents)    │     │   Decision      │     │   Execution     │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Risk Manager   │
                                               │ Position Limits │
                                               └─────────────────┘
```

### Supported Actions

| Action | Description | When Used |
|--------|-------------|-----------|
| BUY | Purchase shares (go long) | Bullish signal |
| SELL | Sell existing long position | Bearish signal on long |
| SHORT | Sell shares you don't own | Bearish signal |
| COVER | Buy back shorted shares | Bullish signal on short |
| HOLD | No action | Neutral signal or low confidence |

---

## Setup

### 1. Create Alpaca Account

1. Go to [https://app.alpaca.markets/](https://app.alpaca.markets/)
2. Sign up for a free account
3. Navigate to "Paper Trading" section
4. Generate API keys

### 2. Configure Environment

Add to your `.env` file:

```bash
# Alpaca API credentials
ALPACA_API_KEY=PKXXXXXXXXXXXXXXXX
ALPACA_SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Paper trading (recommended)
ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_TRADING_MODE=paper
```

### 3. Verify Connection

```bash
poetry run python -c "
from src.trading.alpaca_service import AlpacaService
service = AlpacaService()
status = service.get_status()
print(f'Connected: {status[\"connected\"]}')
print(f'Mode: {status[\"mode\"]}')
print(f'Buying Power: \${status[\"buying_power\"]:,.2f}')
"
```

---

## Trading Modes

### Paper Trading (Recommended)

Uses virtual money to simulate real trading. Perfect for testing strategies.

```bash
# Paper trading endpoint
ALPACA_BASE_URL=https://paper-api.alpaca.markets/v2
ALPACA_TRADING_MODE=paper
```

Paper accounts start with $100,000 virtual cash (can be reset in the Alpaca dashboard).

### Live Trading

Uses real money. **Use with extreme caution.**

```bash
# Live trading endpoint (REAL MONEY!)
ALPACA_BASE_URL=https://api.alpaca.markets/v2
ALPACA_TRADING_MODE=live
```

### Dry Run Mode

Preview trades without executing:

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --dry-run
```

Output:
```
[AAPL] DRY RUN: Would SHORT 91 shares
```

---

## Workflow Integration

### Basic Analysis (No Trading)

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal
```

### Analysis + Trading Execution

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --execute
```

### Full Workflow + Trading

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode full \
  --depth standard \
  --execute
```

### Multiple Tickers

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL MSFT GOOGL NVDA \
  --mode signal \
  --execute
```

### CLI Options

| Option | Description | Values |
|--------|-------------|--------|
| `--tickers` | Stock symbols to analyze | Space-separated list |
| `--mode` | Workflow mode | signal, research, pre-research, post-research, full |
| `--depth` | Research depth | quick, standard, deep |
| `--execute` | Execute trades on Alpaca | Flag |
| `--dry-run` | Preview trades without executing | Flag |
| `--output` | Output format | console, json, markdown |
| `--output-file` | Save output to file | File path |

---

## Direct API Usage

### Initialize Service

```python
from src.trading.alpaca_service import AlpacaService

# Uses environment variables
alpaca = AlpacaService()

# Or specify explicitly
alpaca = AlpacaService(
    api_key="PKXXXXXXXX",
    secret_key="XXXXXXXX",
    base_url="https://paper-api.alpaca.markets/v2",
    paper=True
)
```

### Account Information

```python
# Get account details
account = alpaca.get_account()
print(f"Status: {account.status}")
print(f"Cash: ${account.cash:,.2f}")
print(f"Buying Power: ${account.buying_power:,.2f}")
print(f"Portfolio Value: ${account.portfolio_value:,.2f}")
print(f"Shorting Enabled: {account.shorting_enabled}")
```

### Place Orders

```python
# Buy shares
result = alpaca.buy("AAPL", qty=10)
if result.success:
    print(f"Order ID: {result.order.id}")

# Sell shares
result = alpaca.sell("AAPL", qty=5)

# Short sell
result = alpaca.short("AAPL", qty=10)

# Cover short
result = alpaca.cover("AAPL", qty=10)

# Limit order
result = alpaca.buy("AAPL", qty=10, order_type=OrderType.LIMIT, limit_price=150.00)
```

### Execute Portfolio Manager Decision

```python
# Execute decision from AI Hedge Fund
result = alpaca.execute_decision(
    symbol="AAPL",
    action="short",  # buy, sell, short, cover, hold
    quantity=91
)

if result.success:
    print(f"Executed: {result.order.side} {result.order.qty} shares")
else:
    print(f"Failed: {result.error}")
```

### Get Positions

```python
# Get all positions
positions = alpaca.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.qty} shares")
    print(f"  Side: {pos.side}")
    print(f"  Entry: ${pos.avg_entry_price:.2f}")
    print(f"  Current: ${pos.current_price:.2f}")
    print(f"  P/L: ${pos.unrealized_pl:.2f} ({pos.unrealized_plpc*100:.1f}%)")

# Get specific position
aapl = alpaca.get_position("AAPL")
```

### Manage Orders

```python
# Get open orders
orders = alpaca.get_orders(status="open")
for order in orders:
    print(f"{order.symbol}: {order.side} {order.qty} ({order.status})")

# Get all orders
all_orders = alpaca.get_orders(status="all", limit=20)

# Cancel order
result = alpaca.cancel_order(order_id="xxx")

# Cancel all orders
result = alpaca.cancel_all_orders()
```

### Close Positions

```python
# Close specific position
result = alpaca.close_position("AAPL")

# Partial close
result = alpaca.close_position("AAPL", qty=5)

# Close all positions
results = alpaca.close_all_positions()
```

### Sync Portfolio

```python
# Get portfolio in AI Hedge Fund format
portfolio = alpaca.sync_portfolio()
print(f"Cash: ${portfolio['cash']:,.2f}")
print(f"Positions: {portfolio['positions']}")
```

---

## Order Types

### Market Order (Default)

Executes immediately at current market price.

```python
result = alpaca.buy("AAPL", qty=10)  # Market order
```

### Limit Order

Executes only at specified price or better.

```python
from src.trading.alpaca_service import OrderType

result = alpaca.buy(
    "AAPL",
    qty=10,
    order_type=OrderType.LIMIT,
    limit_price=150.00
)
```

### Stop Order

Triggers a market order when price reaches stop price.

```python
result = alpaca.submit_order(
    symbol="AAPL",
    qty=10,
    side=OrderSide.SELL,
    order_type=OrderType.STOP,
    stop_price=140.00
)
```

### Stop-Limit Order

Triggers a limit order when price reaches stop price.

```python
result = alpaca.submit_order(
    symbol="AAPL",
    qty=10,
    side=OrderSide.SELL,
    order_type=OrderType.STOP_LIMIT,
    stop_price=140.00,
    limit_price=139.00
)
```

### Time in Force

| Value | Description |
|-------|-------------|
| DAY | Order expires at end of trading day (default) |
| GTC | Good til cancelled |
| IOC | Immediate or cancel |
| FOK | Fill or kill |
| OPG | Market on open |
| CLS | Market on close |

```python
from src.trading.alpaca_service import TimeInForce

result = alpaca.submit_order(
    symbol="AAPL",
    qty=10,
    side=OrderSide.BUY,
    order_type=OrderType.LIMIT,
    time_in_force=TimeInForce.GTC,
    limit_price=150.00
)
```

---

## Position Management

### Long Positions

```python
# Buy to open long
alpaca.buy("AAPL", qty=10)

# Sell to close long
alpaca.sell("AAPL", qty=10)
```

### Short Positions

```python
# Short sell to open short
alpaca.short("AAPL", qty=10)

# Buy to cover short
alpaca.cover("AAPL", qty=10)
```

### Position Sizing

The Risk Manager calculates position limits based on:

1. **Volatility** - Higher volatility = smaller positions
2. **Correlation** - Higher correlation = smaller positions
3. **Portfolio Value** - Percentage-based limits

```python
# Risk Manager output example
{
    "AAPL": {
        "remaining_position_limit": 25000.0,
        "volatility_metrics": {
            "annualized_volatility": 0.125,
            "volatility_percentile": 50.0
        },
        "reasoning": {
            "base_position_limit_pct": 0.25,
            "risk_adjustment": "25.0% (base 25.0%)"
        }
    }
}
```

---

## Risk Management

### Built-in Protections

1. **Position Limits** - Maximum position size based on volatility
2. **Confidence Threshold** - Low confidence signals default to HOLD
3. **Paper Trading Default** - Uses paper trading unless explicitly configured
4. **Dry Run Mode** - Preview trades before executing

### Volatility-Based Limits

| Annualized Volatility | Max Position % |
|-----------------------|----------------|
| < 15% (Low) | 25% |
| 15-30% (Medium) | 15-20% |
| 30-50% (High) | 10-15% |
| > 50% (Very High) | 10% max |

### Correlation Adjustments

| Average Correlation | Multiplier |
|--------------------|------------|
| >= 0.8 (Very High) | 0.7x |
| 0.6-0.8 (High) | 0.85x |
| 0.4-0.6 (Moderate) | 1.0x |
| 0.2-0.4 (Low) | 1.05x |
| < 0.2 (Very Low) | 1.10x |

---

## Examples

### Example 1: Full Trading Workflow

```bash
# 1. Analyze stock
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal

# 2. Review signals and recommendations

# 3. Execute if satisfied
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --execute
```

### Example 2: Multi-Stock Portfolio

```bash
poetry run python -m integration.unified_workflow \
  --tickers AAPL MSFT GOOGL NVDA AMZN \
  --mode signal \
  --execute
```

### Example 3: Research Before Trading

```bash
# Deep research first
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode full \
  --depth deep \
  --dry-run

# Review the analysis, then execute
poetry run python -m integration.unified_workflow \
  --tickers AAPL \
  --mode signal \
  --execute
```

### Example 4: Python Integration

```python
from integration.unified_workflow import UnifiedWorkflow, WorkflowMode, execute_trades

# Run analysis
workflow = UnifiedWorkflow()
results = workflow.analyze(
    tickers=["AAPL", "MSFT"],
    mode=WorkflowMode.SIGNAL_ONLY
)

# Execute trades
results = execute_trades(results, dry_run=False)

# Check results
for result in results:
    if result.trade and result.trade.executed:
        print(f"{result.ticker}: {result.trade.action} {result.trade.quantity} shares")
        print(f"  Order ID: {result.trade.order_id}")
```

### Example 5: Scheduled Trading

```python
import schedule
import time
from integration.unified_workflow import UnifiedWorkflow, WorkflowMode, execute_trades

def run_daily_analysis():
    workflow = UnifiedWorkflow()
    results = workflow.analyze(
        tickers=["AAPL", "MSFT", "GOOGL"],
        mode=WorkflowMode.SIGNAL_ONLY
    )
    execute_trades(results, dry_run=False)

# Run at market open (9:30 AM ET)
schedule.every().monday.at("09:30").do(run_daily_analysis)
schedule.every().tuesday.at("09:30").do(run_daily_analysis)
schedule.every().wednesday.at("09:30").do(run_daily_analysis)
schedule.every().thursday.at("09:30").do(run_daily_analysis)
schedule.every().friday.at("09:30").do(run_daily_analysis)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Troubleshooting

### Connection Issues

**Error:** `Alpaca API credentials not found`

**Solution:** Check your `.env` file has:
```bash
ALPACA_API_KEY=your-key
ALPACA_SECRET_KEY=your-secret
```

### Order Rejected

**Error:** `insufficient buying power`

**Solution:** Check account balance:
```python
account = alpaca.get_account()
print(f"Buying Power: ${account.buying_power:,.2f}")
```

### Market Closed

**Error:** `market is not open`

**Solution:** Orders will be queued for next market open, or use:
- Extended hours trading (if enabled)
- Limit orders with GTC time-in-force

### Pattern Day Trader

**Error:** `pattern day trader restriction`

**Solution:**
- Paper trading accounts don't have this restriction
- For live accounts, maintain $25,000+ equity or limit day trades

### Rate Limits

**Error:** `too many requests`

**Solution:** Add delays between API calls:
```python
import time
for ticker in tickers:
    result = alpaca.buy(ticker, qty=1)
    time.sleep(0.5)  # 500ms delay
```

### SSL/Certificate Errors

**Error:** `SSL certificate verify failed`

**Solution:** Update certificates:
```bash
pip install --upgrade certifi
```

---

## API Reference

### AlpacaService

```python
class AlpacaService:
    def __init__(self, api_key=None, secret_key=None, base_url=None, paper=True)

    # Account
    def get_account() -> AlpacaAccount
    def get_buying_power() -> float
    def get_cash() -> float
    def get_portfolio_value() -> float

    # Positions
    def get_positions() -> List[AlpacaPosition]
    def get_position(symbol: str) -> Optional[AlpacaPosition]
    def close_position(symbol: str, qty: float = None) -> TradeResult
    def close_all_positions() -> List[TradeResult]

    # Orders
    def get_orders(status: str = "open", limit: int = 50) -> List[AlpacaOrder]
    def get_order(order_id: str) -> AlpacaOrder
    def submit_order(...) -> TradeResult
    def cancel_order(order_id: str) -> TradeResult
    def cancel_all_orders() -> TradeResult

    # Trading shortcuts
    def buy(symbol: str, qty: float, ...) -> TradeResult
    def sell(symbol: str, qty: float, ...) -> TradeResult
    def short(symbol: str, qty: float, ...) -> TradeResult
    def cover(symbol: str, qty: float = None, ...) -> TradeResult

    # Integration
    def execute_decision(symbol: str, action: str, quantity: int) -> TradeResult
    def sync_portfolio() -> Dict[str, Any]
    def get_status() -> Dict[str, Any]
```

### TradeResult

```python
@dataclass
class TradeResult:
    success: bool
    order: Optional[AlpacaOrder] = None
    error: Optional[str] = None
    message: str = ""
```

---

## Author

**Vitale Mazo**
