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
- OpenAI API key (get [here](https://platform.openai.com/api-keys))
- Financial Datasets API key (get [here](https://financialdatasets.ai))
- Tavily API key (get [here](https://tavily.com)) - optional, for web search

### API Keys Explained

Mazo uses multiple APIs that serve different purposes:

| API | Purpose | Required |
|-----|---------|----------|
| **OpenAI** | LLM reasoning and analysis - the "brain" that thinks through research | Yes |
| **Tavily** | Real-time web search for current news, events, and market data | Optional |
| **Financial Datasets** | Structured financial data (income statements, balance sheets, etc.) | Yes |

**How they work together:**
1. You ask a question like "Research Apple"
2. Mazo uses **Tavily** to search the web for current Apple news, analyst reports, etc.
3. Mazo uses **Financial Datasets** to fetch structured financial statements
4. Mazo sends all this context to the **LLM (OpenAI)** for analysis and reasoning
5. The LLM synthesizes the data into a comprehensive research report

**Using an OpenAI-compatible proxy:**

Mazo supports routing all LLM requests through an OpenAI-compatible proxy. This is the recommended setup when using the AI Hedge Fund project, as it shares the same configuration.

```bash
OPENAI_API_BASE=https://your-proxy.com/v1
OPENAI_API_KEY=your-proxy-api-key
```

This is useful for:
- Cost tracking and rate limiting
- Using alternative LLM providers with OpenAI-compatible APIs (e.g., Claude via proxy)
- Enterprise deployments with custom endpoints

**How the proxy routing works:**

When `OPENAI_API_BASE` is set in your environment:
1. **All models route through the proxy** - including Claude, GPT, and other models
2. **Only `OPENAI_API_KEY` is required** - you don't need separate Anthropic/Google API keys
3. **The proxy handles model selection** - the model name (e.g., `claude-sonnet-4-5-20250929`) is passed to the proxy which routes to the correct provider

This means you can use Claude Sonnet 4.5 as your default model while routing through an OpenAI-compatible proxy service.

Note: The proxy only handles LLM calls. Tavily and Financial Datasets APIs are called directly with their own API keys.

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

Mazo automatically loads the `.env` file from the parent AI Hedge Fund project directory. This means both projects share the same API configuration.

**Required environment variables** (in the parent `.env` file):

```bash
# LLM Configuration (proxy setup - recommended)
OPENAI_API_KEY=your-proxy-api-key
OPENAI_API_BASE=https://your-proxy.com/v1

# Financial Data
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# Web Search (optional)
TAVILY_API_KEY=your-tavily-api-key
```

**Alternative: Direct API access** (without proxy):

```bash
# Use provider-specific keys directly
ANTHROPIC_API_KEY=your-anthropic-api-key  # For Claude models
OPENAI_API_KEY=your-openai-api-key        # For GPT models
GOOGLE_API_KEY=your-google-api-key        # For Gemini models
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

Type `/model` in the CLI to switch between:
- GPT 5.2 (OpenAI)
- Claude Sonnet 4.5 (Anthropic) - **Default**
- Gemini 3 (Google)

**Model routing with proxy:**

When using an OpenAI-compatible proxy (`OPENAI_API_BASE` is set):
- All models are routed through the proxy endpoint
- The model name is passed directly to the proxy (e.g., `claude-sonnet-4-5-20250929`)
- Only `OPENAI_API_KEY` is needed - no separate provider keys required
- The proxy service handles routing to the appropriate LLM provider

**Model routing without proxy:**

When no proxy is configured:
- Claude models use `ANTHROPIC_API_KEY` directly
- GPT models use `OPENAI_API_KEY` directly
- Gemini models use `GOOGLE_API_KEY` directly

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
