# Mazo Hedge Fund

An AI-powered hedge fund that combines multi-agent trading signal generation with autonomous financial research.


## Overview

This system combines two powerful components:

1. **AI Hedge Fund** - Multi-agent trading signal generator with 18 specialized agents
2. **Mazo** - Autonomous financial research agent for deep analysis

The goal is to explore the use of AI to make informed trading decisions. This project is for **educational** purposes only and is not intended for real trading or investment.

## Architecture

### Trading Agents

1. Aswath Damodaran Agent - The Dean of Valuation, focuses on story, numbers, and disciplined valuation
2. Ben Graham Agent - The godfather of value investing, only buys hidden gems with a margin of safety
3. Bill Ackman Agent - An activist investor, takes bold positions and pushes for change
4. Cathie Wood Agent - The queen of growth investing, believes in the power of innovation and disruption
5. Charlie Munger Agent - Warren Buffett's partner, only buys wonderful businesses at fair prices
6. Michael Burry Agent - The Big Short contrarian who hunts for deep value
7. Mohnish Pabrai Agent - The Dhandho investor, who looks for doubles at low risk
8. Peter Lynch Agent - Practical investor who seeks "ten-baggers" in everyday businesses
9. Phil Fisher Agent - Meticulous growth investor who uses deep "scuttlebutt" research
10. Rakesh Jhunjhunwala Agent - The Big Bull of India
11. Stanley Druckenmiller Agent - Macro legend who hunts for asymmetric opportunities with growth potential
12. Warren Buffett Agent - The oracle of Omaha, seeks wonderful companies at a fair price
13. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
14. Sentiment Agent - Analyzes market sentiment and generates trading signals
15. Fundamentals Agent - Analyzes fundamental data and generates trading signals
16. Technicals Agent - Analyzes technical indicators and generates trading signals
17. Risk Manager - Calculates risk metrics and sets position limits
18. Portfolio Manager - Makes final trading decisions and generates orders

### Mazo Research Agent

Mazo is an autonomous financial research agent that:
- Takes complex financial questions and turns them into step-by-step research plans
- Executes research tasks using live market data
- Validates its own work and refines results
- Provides data-backed answers with confidence scores

See [mazo/README.md](mazo/README.md) for detailed documentation.

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [How to Install](#how-to-install)
- [How to Run](#how-to-run)
  - [Command Line Interface](#command-line-interface)
  - [Web Application](#web-application)
  - [Mazo Research](#mazo-research)
  - [Unified Workflow](#unified-workflow)
- [Credits](#credits)
- [License](#license)

## How to Install

### 1. Clone the Repository

```bash
git clone https://github.com/vitalemazo/mazo-hedge-fund.git
cd mazo-hedge-fund
```

### 2. Set up API keys

Create a `.env` file for your API keys:
```bash
cp .env.example .env
```

Open and edit the `.env` file to add your API keys:
```bash
# For running LLMs (required)
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1  # or your custom endpoint

# For getting financial data
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### 3. Install AI Hedge Fund dependencies

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### 4. Install Mazo dependencies

```bash
# Install Bun (if not already installed)
curl -fsSL https://bun.sh/install | bash

# Install Mazo dependencies
cd mazo
bun install
cd ..
```

## How to Run

### Command Line Interface

Run the AI Hedge Fund via terminal:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

With date range:
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

Run the backtester:
```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

### Web Application

Start the web application for a user-friendly interface:

```bash
cd app
# Follow instructions in app/README.md
```

### Mazo Research

Run Mazo for autonomous financial research:

```bash
cd mazo
bun start
```

Example queries:
- "What was Apple's revenue growth over the last 4 quarters?"
- "Compare Microsoft and Google's operating margins for 2023"
- "Analyze Tesla's cash flow trends over the past year"

### Unified Workflow

Use the unified workflow to combine AI Hedge Fund signals with Mazo research:

```bash
poetry run python -m integration.unified_workflow --tickers AAPL --mode full --depth standard
```

Workflow modes:
- `signal` - Just AI Hedge Fund signal generation
- `research` - Just Mazo research
- `pre-research` - Mazo research first, then informed signal
- `post-research` - Signal first, then Mazo explains
- `full` - Complete workflow with both pre and post research

## Author

**Vitale Mazo**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
