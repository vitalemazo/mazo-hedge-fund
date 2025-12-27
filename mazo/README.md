# Mazo

Mazo is an autonomous financial research agent that thinks, plans, and learns as it works. It performs analysis using task planning, self-reflection, and real-time market data. Think Claude Code, but built specifically for financial research.


## Overview

Mazo takes complex financial questions and turns them into clear, step-by-step research plans. It runs those tasks using live market data, checks its own work, and refines the results until it has a confident, data-backed answer.

**Key Capabilities:**
- **Intelligent Task Planning**: Automatically decomposes complex queries into structured research steps
- **Autonomous Execution**: Selects and executes the right tools to gather financial data
- **Self-Validation**: Checks its own work and iterates until tasks are complete
- **Real-Time Financial Data**: Access to income statements, balance sheets, and cash flow statements
- **Safety Features**: Built-in loop detection and step limits to prevent runaway execution

### Prerequisites

- [Bun](https://bun.com) runtime (v1.0 or higher)
- OpenAI-compatible API proxy (recommended) OR direct provider API keys
- Financial Datasets API key (get [here](https://financialdatasets.ai))
- Tavily API key (get [here](https://tavily.com)) - optional, for web search

### API Configuration

Mazo uses multiple APIs that serve different purposes:

| API | Purpose | Required |
|-----|---------|----------|
| **LLM Proxy** | Routes all LLM requests (Claude, GPT, etc.) through a single endpoint | Yes (recommended) |
| **Financial Datasets** | Structured financial data (income statements, balance sheets, etc.) | Yes |
| **Tavily** | Real-time web search for current news, events, and market data | Optional |

**How they work together:**
1. You ask a question like "Compare Microsoft and Google's operating margins"
2. Mazo uses **Financial Datasets** to fetch structured financial statements
3. Mazo uses **Tavily** (if configured) to search for current news and context
4. Mazo sends all this context to the **LLM** (via proxy) for analysis and reasoning
5. The LLM synthesizes the data into a comprehensive research report

## LLM Proxy Configuration (Recommended)

Mazo is designed to work with an OpenAI-compatible proxy API. This is the **recommended setup** as it:
- Provides unified access to multiple LLM providers (Claude, GPT, Gemini, etc.)
- Requires only a single API key for all models
- Enables cost tracking and rate limiting
- Works seamlessly with the AI Hedge Fund project

### Setting Up the Proxy

Add these to your `.env` file (in the parent directory):

```bash
# LLM Proxy Configuration
OPENAI_API_KEY=your-proxy-api-key
OPENAI_API_BASE=https://your-proxy.com/v1
```

**Example with a proxy service:**
```bash
OPENAI_API_KEY=sk-your-proxy-key
OPENAI_API_BASE=https://api.your-proxy-service.com/v1
```

### How Proxy Routing Works

When `OPENAI_API_BASE` is set:

1. **All models route through the proxy** - Claude, GPT, Gemini, and other models all use the same endpoint
2. **Single API key** - Only `OPENAI_API_KEY` is needed (no separate Anthropic/Google keys)
3. **Model passthrough** - The model name (e.g., `claude-sonnet-4-5-20250929`) is passed directly to the proxy
4. **Provider routing** - The proxy service handles routing to the correct LLM provider

**Default model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)

### Schema Validation Warnings

When using a proxy, you may see schema validation warnings like:
```
Schema validation warning: Invalid option: expected one of "ticker"|"date"|...
```

**These warnings are normal and can be safely ignored.** They occur because:
- Proxies don't support OpenAI's native structured output format
- Mazo uses JSON prompting as a fallback
- The LLM occasionally returns slightly different values than the strict schema expects
- The code handles this gracefully and continues working

Your queries will still complete successfully despite these warnings.

### Direct API Access (Alternative)

If you prefer not to use a proxy, you can configure direct API access:

```bash
# Direct provider keys (no proxy)
ANTHROPIC_API_KEY=your-anthropic-api-key  # For Claude models
OPENAI_API_KEY=your-openai-api-key        # For GPT models
GOOGLE_API_KEY=your-google-api-key        # For Gemini models
```

Note: Without a proxy, each provider requires its own API key, and you cannot mix providers through a single endpoint.

#### Installing Bun

If you don't have Bun installed, you can install it using curl:

**macOS/Linux:**
```bash
curl -fsSL https://bun.com/install | bash
```

**Windows:**
```bash
powershell -c "irm bun.sh/install.ps1|iex"
```

After installation, restart your terminal and verify Bun is installed:
```bash
bun --version
```

### Installing Mazo

1. Navigate to the mazo directory:
```bash
cd mazo
```

2. Install dependencies with Bun:
```bash
bun install
```

3. Set up your environment variables:

Mazo automatically loads the `.env` file from the parent AI Hedge Fund project directory. See [LLM Proxy Configuration](#llm-proxy-configuration-recommended) above for details.

**Minimum required variables** (in the parent `.env` file):

```bash
# LLM (via proxy - recommended)
OPENAI_API_KEY=your-proxy-api-key
OPENAI_API_BASE=https://your-proxy.com/v1

# Financial Data (required)
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# Web Search (optional)
TAVILY_API_KEY=your-tavily-api-key
```

### Usage

**Starting Mazo:**

Mazo requires an interactive terminal with TTY support. Run it directly in your terminal (not through automated scripts or non-interactive shells):

```bash
# Navigate to the mazo directory
cd /path/to/mazo-hedge-fund/mazo

# Install dependencies (first time only)
bun install

# Start Mazo in interactive mode
bun start
```

**Development mode** (auto-restart on file changes):
```bash
bun dev
```

**Quick start from any directory:**
```bash
cd /path/to/mazo-hedge-fund/mazo && bun start
```

**Important:** Mazo uses [Ink](https://github.com/vadimdemedes/ink) for its terminal UI, which requires raw mode support. You must run it in a proper terminal application (Terminal.app, iTerm2, Windows Terminal, etc.), not through:
- CI/CD pipelines
- Non-interactive SSH sessions
- Subprocess shells without TTY

### Example Queries

Try asking Mazo questions like:
- "What was Apple's revenue growth over the last 4 quarters?"
- "Compare Microsoft and Google's operating margins for 2023"
- "Analyze Tesla's cash flow trends over the past year"
- "What is Amazon's debt-to-equity ratio based on recent financials?"

Mazo will automatically:
1. Break down your question into research tasks
2. Fetch the necessary financial data
3. Perform calculations and analysis
4. Provide a comprehensive, data-rich answer

## Architecture

Mazo uses a multi-agent architecture with specialized components:

- **Planning Agent**: Analyzes queries and creates structured task lists
- **Action Agent**: Selects appropriate tools and executes research steps
- **Validation Agent**: Verifies task completion and data sufficiency
- **Answer Agent**: Synthesizes findings into comprehensive responses

## Tech Stack

- **Runtime**: [Bun](https://bun.sh)
- **UI Framework**: [React](https://react.dev) + [Ink](https://github.com/vadimdemedes/ink) (terminal UI)
- **LLM Integration**: [LangChain.js](https://js.langchain.com) with multi-provider support (OpenAI, Anthropic, Google)
- **Schema Validation**: [Zod](https://zod.dev)
- **Language**: TypeScript


### Changing Models

Type `/model` in the CLI to switch between available models:

| Model | Provider | Model ID |
|-------|----------|----------|
| Claude Sonnet 4.5 | Anthropic | `claude-sonnet-4-5-20250929` **(Default)** |
| GPT 5.2 | OpenAI | `gpt-5.2` |
| Gemini 3 | Google | `gemini-3` |

When using a proxy, all models route through the same endpoint. The proxy handles provider routing based on the model ID. See [How Proxy Routing Works](#how-proxy-routing-works) for details.

## Integration with AI Hedge Fund

Mazo is designed to work seamlessly with the AI Hedge Fund trading system:

- **Pre-Signal Research**: Gather context before AI Hedge Fund generates signals
- **Post-Signal Explanation**: Deep dive into why signals were generated
- **Agent-Specific Context**: Provide tailored research for each investor persona

See the parent project's `integration/` directory for bridge code.

### Shared Configuration

Mazo and AI Hedge Fund share the same `.env` configuration file located in the parent directory. This ensures:

1. **Consistent API access** - Both projects use the same API keys and proxy settings
2. **Single configuration point** - Update keys in one place
3. **Unified proxy routing** - LLM requests from both projects go through the same proxy

**File structure:**
```
mazo-hedge-fund/
├── .env                    # Shared environment configuration
├── mazo/                   # Mazo agent (this project)
│   └── src/
│       └── index.tsx       # Loads ../.env automatically
├── src/                    # AI Hedge Fund Python code
└── app/                    # Web application
```

Mazo automatically detects and loads the parent `.env` file on startup, so you don't need to duplicate configuration.

## License

This project is licensed under the MIT License.

## Author

Vitale Mazo
