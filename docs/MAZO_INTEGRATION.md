# Mazo Integration Guide

This document describes the integration between **AI Hedge Fund** and **Mazo**, two complementary AI-powered financial analysis systems.

## Table of Contents

1. [Overview](#overview)
2. [System Comparison](#system-comparison)
3. [Integration Architecture](#integration-architecture)
4. [Integration Patterns](#integration-patterns)
5. [Setup Guide](#setup-guide)
6. [Web UI Integration](#web-ui-integration)
7. [API Bridge](#api-bridge)
8. [Unified Workflow](#unified-workflow)
9. [Configuration](#configuration)
10. [Usage Examples](#usage-examples)

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
| LLM Providers | OpenAI, Anthropic, Groq, etc. | OpenAI, Anthropic, Google |

### Shared Components

Both systems share:
- **Financial Datasets API** for market data
- **Same LLM providers** (OpenAI, Anthropic)

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
│  └─────────────────────────────┘             └─────────────────────────────┘
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

1. Python 3.11+ with Poetry
2. Bun runtime for Mazo
3. API keys for:
   - OpenAI or other LLM provider
   - Financial Datasets API

### Installation

```bash
# Clone the repository
git clone https://github.com/vitalemazo/mazo-hedge-fund.git
cd mazo-hedge-fund

# Install Python dependencies
poetry install

# Install Mazo dependencies
cd mazo
bun install
cd ..
```

### Configuration

Set up your `.env` file:

```bash
# LLM Configuration
OPENAI_API_KEY=your-key
OPENAI_API_BASE=https://api.openai.com/v1

# Financial Data
FINANCIAL_DATASETS_API_KEY=your-key

# Mazo Configuration
MAZO_PATH=./mazo
MAZO_TIMEOUT=300
DEFAULT_WORKFLOW_MODE=full
DEFAULT_RESEARCH_DEPTH=standard
```

---

## Web UI Integration

The web application includes Mazo research capabilities directly in the interface.

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

### Streaming Research (SSE)

The `/mazo/research/stream` endpoint provides real-time progress updates:

```typescript
// Frontend usage example
const controller = mazoApi.researchStream(
  { query: "What's driving NVDA's growth?", depth: 'standard' },
  (event) => {
    switch (event.type) {
      case 'start':
        console.log('Research started');
        break;
      case 'progress':
        console.log('Progress:', event.data.message);
        break;
      case 'complete':
        console.log('Answer:', event.data.answer);
        break;
      case 'error':
        console.error('Error:', event.data.message);
        break;
    }
  }
);

// Cancel stream if needed
controller.abort();
```

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
python -m integration.unified_workflow --tickers AAPL --mode full

# Pre-research mode (Mazo first, then AI HF)
python -m integration.unified_workflow --tickers AAPL --mode pre-research

# Post-research mode (AI HF first, then Mazo explains)
python -m integration.unified_workflow --tickers AAPL --mode post-research

# Signal only (just AI Hedge Fund)
python -m integration.unified_workflow --tickers AAPL --mode signal

# Research only (just Mazo)
python -m integration.unified_workflow --tickers AAPL --mode research
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAZO_PATH` | Path to Mazo installation | `./mazo` |
| `MAZO_TIMEOUT` | Query timeout in seconds | `300` |
| `DEFAULT_WORKFLOW_MODE` | Default workflow mode | `full` |
| `DEFAULT_RESEARCH_DEPTH` | Research depth (quick/standard/deep) | `standard` |

### Research Depth Levels

- **quick**: Brief overview, key metrics
- **standard**: Comprehensive analysis with valuation
- **deep**: Exhaustive research with scenarios

---

## Usage Examples

### Example 1: Full Analysis

```bash
python -m integration.unified_workflow \
  --tickers AAPL MSFT \
  --mode full \
  --depth deep \
  --output markdown \
  --output-file analysis.md
```

### Example 2: Python Integration

```python
from integration.unified_workflow import UnifiedWorkflow, WorkflowMode

workflow = UnifiedWorkflow()
results = workflow.analyze(
    tickers=["AAPL"],
    mode=WorkflowMode.FULL,
)

for result in results:
    print(f"{result.ticker}: {result.signal} ({result.confidence}%)")
    print(result.research_report)
```

---

## Author

**Vitale Mazo**
