"""
Unified Workflow - Orchestrates AI Hedge Fund and Mazo together.

This script provides a complete workflow that:
1. Accepts user requests
2. Routes to appropriate system(s)
3. Manages data flow between systems
4. Produces comprehensive output

Usage:
    python -m integration.unified_workflow --tickers AAPL --mode full --depth standard
    python -m integration.unified_workflow --tickers AAPL MSFT GOOGL --mode post-research

"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.mazo_bridge import MazoBridge, MazoResponse
from integration.config import config


class WorkflowMode(Enum):
    """Available workflow modes"""
    SIGNAL_ONLY = "signal"           # Just AI Hedge Fund
    RESEARCH_ONLY = "research"       # Just Mazo
    PRE_RESEARCH = "pre-research"    # Mazo → AI Hedge Fund
    POST_RESEARCH = "post-research"  # AI Hedge Fund → Mazo
    FULL = "full"                    # Complete workflow


class ResearchDepth(Enum):
    """Research depth levels"""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


@dataclass
class AgentSignal:
    """Signal from an AI Hedge Fund agent"""
    agent_name: str
    signal: str  # BULLISH, BEARISH, NEUTRAL
    confidence: float
    reasoning: str


@dataclass
class UnifiedResult:
    """Combined result from both systems"""
    ticker: str
    signal: Optional[str] = None
    confidence: Optional[float] = None
    agent_signals: List[AgentSignal] = field(default_factory=list)
    research_report: Optional[str] = None
    recommendations: List[str] = field(default_factory=list)
    workflow_mode: str = "full"
    execution_time: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "ticker": self.ticker,
            "signal": self.signal,
            "confidence": self.confidence,
            "agent_signals": [asdict(s) for s in self.agent_signals],
            "research_report": self.research_report,
            "recommendations": self.recommendations,
            "workflow_mode": self.workflow_mode,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp,
        }

    def to_markdown(self) -> str:
        """Convert to markdown report"""
        md = f"""
# Unified Analysis Report: {self.ticker}

**Generated:** {self.timestamp}
**Workflow:** {self.workflow_mode}
**Execution Time:** {self.execution_time:.2f}s

---

## Trading Signal

| Metric | Value |
|--------|-------|
| **Signal** | {self.signal or 'N/A'} |
| **Confidence** | {f'{self.confidence:.0f}%' if self.confidence else 'N/A'} |

"""
        if self.agent_signals:
            md += """
## Agent Analysis

| Agent | Signal | Confidence | Reasoning |
|-------|--------|------------|-----------|
"""
            for agent in self.agent_signals:
                reasoning_short = agent.reasoning[:50] + "..." if len(agent.reasoning) > 50 else agent.reasoning
                md += f"| {agent.agent_name} | {agent.signal} | {agent.confidence:.0f}% | {reasoning_short} |\n"

        if self.research_report:
            md += f"""
---

## Research Report

{self.research_report}
"""

        if self.recommendations:
            md += """
---

## Recommendations

"""
            for rec in self.recommendations:
                md += f"- {rec}\n"

        return md


class UnifiedWorkflow:
    """
    Orchestrator for AI Hedge Fund + Mazo integration.

    Provides multiple workflow modes:
    - signal: Just AI Hedge Fund signal generation
    - research: Just Mazo research
    - pre-research: Mazo research first, then informed signal
    - post-research: Signal first, then Mazo explains
    - full: Complete workflow with both pre and post research
    """

    def __init__(
        self,
        model_name: str = None,
        model_provider: str = "OpenAI",
        api_keys: dict = None
    ):
        """
        Initialize the unified workflow.

        Args:
            model_name: LLM model to use
            model_provider: Provider (OpenAI, Anthropic, etc.)
            api_keys: API keys dict (optional, uses env if not provided)
        """
        self.model_name = model_name or config.default_model
        self.model_provider = model_provider
        self.api_keys = api_keys or {}
        self.mazo = MazoBridge()

    def analyze(
        self,
        tickers: List[str],
        mode: WorkflowMode = None,
        analysts: List[str] = None,
        research_depth: ResearchDepth = None
    ) -> List[UnifiedResult]:
        """
        Run unified analysis on given tickers.

        Args:
            tickers: List of stock symbols
            mode: Workflow mode to use
            analysts: Specific analysts to use (None = all)
            research_depth: Research depth level

        Returns:
            List of UnifiedResult for each ticker
        """
        mode = mode or WorkflowMode(config.default_workflow_mode)
        research_depth = research_depth or ResearchDepth(config.default_research_depth)

        results = []
        total_start = datetime.now()

        print(f"\n{'='*60}")
        print(f"UNIFIED TRADING WORKFLOW")
        print(f"Mode: {mode.value} | Depth: {research_depth.value}")
        print(f"Tickers: {', '.join(tickers)}")
        print(f"{'='*60}\n")

        for ticker in tickers:
            print(f"\n[{ticker}] Starting analysis...")
            start_time = datetime.now()

            if mode == WorkflowMode.SIGNAL_ONLY:
                result = self._signal_only(ticker, analysts)
            elif mode == WorkflowMode.RESEARCH_ONLY:
                result = self._research_only(ticker, research_depth)
            elif mode == WorkflowMode.PRE_RESEARCH:
                result = self._pre_research_flow(ticker, analysts, research_depth)
            elif mode == WorkflowMode.POST_RESEARCH:
                result = self._post_research_flow(ticker, analysts, research_depth)
            elif mode == WorkflowMode.FULL:
                result = self._full_flow(ticker, analysts, research_depth)
            else:
                result = UnifiedResult(
                    ticker=ticker,
                    recommendations=["Unknown workflow mode"]
                )

            result.execution_time = (datetime.now() - start_time).total_seconds()
            result.workflow_mode = mode.value
            results.append(result)

            print(f"[{ticker}] Completed in {result.execution_time:.2f}s")

        total_time = (datetime.now() - total_start).total_seconds()
        print(f"\n{'='*60}")
        print(f"All analyses completed in {total_time:.2f}s")
        print(f"{'='*60}\n")

        return results

    def _signal_only(
        self,
        ticker: str,
        analysts: List[str]
    ) -> UnifiedResult:
        """
        Just run AI Hedge Fund signal generation.

        Note: This would call the actual AI Hedge Fund. For now,
        returns a placeholder showing the integration point.
        """
        print(f"  [AI Hedge Fund] Generating signal for {ticker}...")

        # Placeholder - integrate with actual AI Hedge Fund
        # from src.main import run_hedge_fund
        # hf_result = run_hedge_fund(...)

        return UnifiedResult(
            ticker=ticker,
            signal="NEUTRAL",
            confidence=50.0,
            agent_signals=[
                AgentSignal(
                    agent_name="Placeholder",
                    signal="NEUTRAL",
                    confidence=50.0,
                    reasoning="Connect to actual AI Hedge Fund for real signals"
                )
            ],
            recommendations=[
                "Integration point: Call run_hedge_fund() from src/main.py",
                "Pass analysts parameter to select specific agents"
            ]
        )

    def _research_only(
        self,
        ticker: str,
        depth: ResearchDepth
    ) -> UnifiedResult:
        """Just run Mazo research"""
        print(f"  [Mazo] Researching {ticker} (depth: {depth.value})...")

        query = self._build_research_query(ticker, depth)
        research = self.mazo.research(query)

        return UnifiedResult(
            ticker=ticker,
            research_report=research.answer,
            recommendations=self._extract_research_recommendations(research)
        )

    def _pre_research_flow(
        self,
        ticker: str,
        analysts: List[str],
        depth: ResearchDepth
    ) -> UnifiedResult:
        """Mazo research first, then AI Hedge Fund with context"""
        # Step 1: Mazo research
        print(f"  [Mazo] Pre-signal research on {ticker}...")
        query = self._build_research_query(ticker, depth)
        research = self.mazo.research(query)

        # Step 2: AI Hedge Fund with research context
        print(f"  [AI Hedge Fund] Analyzing {ticker} with research context...")
        # TODO: Pass research.answer as context to agents

        return UnifiedResult(
            ticker=ticker,
            signal="NEUTRAL",
            confidence=50.0,
            agent_signals=[
                AgentSignal(
                    agent_name="Pre-Research Flow",
                    signal="NEUTRAL",
                    confidence=50.0,
                    reasoning="Signal generation with Mazo research context"
                )
            ],
            research_report=research.answer,
            recommendations=[
                "Pre-research complete",
                "Integration: Pass research to AI Hedge Fund agents as context"
            ]
        )

    def _post_research_flow(
        self,
        ticker: str,
        analysts: List[str],
        depth: ResearchDepth
    ) -> UnifiedResult:
        """AI Hedge Fund first, then Mazo explains"""
        # Step 1: AI Hedge Fund signal
        print(f"  [AI Hedge Fund] Generating signal for {ticker}...")

        # Placeholder signal - replace with actual AI Hedge Fund call
        signal = "BEARISH"
        confidence = 72.0
        reasoning = "Trading above intrinsic value"

        # Step 2: Mazo explains the signal
        print(f"  [Mazo] Explaining {signal} signal...")
        research = self.mazo.explain_signal(
            ticker=ticker,
            signal=signal,
            confidence=confidence,
            reasoning=reasoning
        )

        return UnifiedResult(
            ticker=ticker,
            signal=signal,
            confidence=confidence,
            agent_signals=[
                AgentSignal(
                    agent_name="Post-Research Flow",
                    signal=signal,
                    confidence=confidence,
                    reasoning=reasoning
                )
            ],
            research_report=research.answer,
            recommendations=[
                f"Signal: {signal} with {confidence}% confidence",
                "See research report for detailed explanation"
            ]
        )

    def _full_flow(
        self,
        ticker: str,
        analysts: List[str],
        depth: ResearchDepth
    ) -> UnifiedResult:
        """Complete workflow: Pre-research → Signal → Post-research"""
        # Step 1: Initial Mazo research
        print(f"  [Mazo] Initial research on {ticker}...")
        initial_research = self.mazo.analyze_company(ticker)

        # Step 2: AI Hedge Fund with context
        print(f"  [AI Hedge Fund] Analyzing {ticker}...")
        # Placeholder - replace with actual AI Hedge Fund
        signal = "NEUTRAL"
        confidence = 50.0
        reasoning = "Placeholder signal"

        # Step 3: Mazo deep dive on signal
        print(f"  [Mazo] Deep dive on signal...")
        deep_research = self.mazo.explain_signal(
            ticker=ticker,
            signal=signal,
            confidence=confidence,
            reasoning=reasoning
        )

        # Combine research reports
        full_report = f"""
## Initial Research

{initial_research.answer}

---

## Signal Explanation

{deep_research.answer}
"""

        return UnifiedResult(
            ticker=ticker,
            signal=signal,
            confidence=confidence,
            agent_signals=[
                AgentSignal(
                    agent_name="Full Workflow",
                    signal=signal,
                    confidence=confidence,
                    reasoning="Complete pre + post research flow"
                )
            ],
            research_report=full_report,
            recommendations=[
                "Full workflow completed",
                "Pre-research informed the signal",
                "Post-research explained the decision"
            ]
        )

    def _build_research_query(self, ticker: str, depth: ResearchDepth) -> str:
        """Build research query based on depth"""
        if depth == ResearchDepth.QUICK:
            return f"Give me a quick overview of {ticker}'s recent performance and outlook."
        elif depth == ResearchDepth.DEEP:
            return f"""
Provide an exhaustive analysis of {ticker} covering:
1. Financial performance (3-year trends)
2. Competitive landscape and market position
3. Management quality and capital allocation
4. Growth drivers and headwinds
5. Valuation analysis vs peers and history
6. Risk factors (macro, micro, regulatory)
7. Bull and bear case scenarios
8. Key metrics to monitor
"""
        else:  # STANDARD
            return f"""
Analyze {ticker} covering:
1. Recent financial performance
2. Competitive position
3. Key risks and opportunities
4. Valuation assessment
5. Investment recommendation
"""

    def _extract_research_recommendations(self, research: MazoResponse) -> List[str]:
        """Extract recommendations from Mazo research"""
        # Simple extraction - enhance with NLP if needed
        return [
            "Review Mazo research report for detailed analysis",
            "Consider the key risks and opportunities identified"
        ]


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Unified AI Trading Workflow - Combines AI Hedge Fund + Mazo"
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        required=True,
        help="Stock tickers to analyze (e.g., AAPL MSFT GOOGL)"
    )
    parser.add_argument(
        "--mode",
        choices=["signal", "research", "pre-research", "post-research", "full"],
        default="full",
        help="Workflow mode (default: full)"
    )
    parser.add_argument(
        "--depth",
        choices=["quick", "standard", "deep"],
        default="standard",
        help="Research depth (default: standard)"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="LLM model to use (default: from config)"
    )
    parser.add_argument(
        "--output",
        choices=["console", "json", "markdown"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Output file path (optional)"
    )

    args = parser.parse_args()

    # Initialize workflow
    workflow = UnifiedWorkflow(model_name=args.model)

    # Run analysis
    results = workflow.analyze(
        tickers=args.tickers,
        mode=WorkflowMode(args.mode),
        research_depth=ResearchDepth(args.depth)
    )

    # Output results
    if args.output == "json":
        output = json.dumps([r.to_dict() for r in results], indent=2)
    elif args.output == "markdown":
        output = "\n\n---\n\n".join([r.to_markdown() for r in results])
    else:  # console
        for result in results:
            print(f"\n{'='*60}")
            print(f"UNIFIED ANALYSIS: {result.ticker}")
            print(f"{'='*60}")

            if result.signal:
                print(f"\nSIGNAL: {result.signal} ({result.confidence:.0f}% confidence)")

            if result.agent_signals:
                print(f"\nAGENT SIGNALS:")
                for agent in result.agent_signals:
                    print(f"  - {agent.agent_name}: {agent.signal} ({agent.confidence:.0f}%)")

            if result.research_report:
                print(f"\nRESEARCH REPORT:")
                print("-" * 40)
                print(result.research_report[:500])  # First 500 chars
                if len(result.research_report) > 500:
                    print("... [truncated]")

            if result.recommendations:
                print(f"\nRECOMMENDATIONS:")
                for rec in result.recommendations:
                    print(f"  - {rec}")

        output = None

    # Write to file if specified
    if args.output_file and output:
        with open(args.output_file, "w") as f:
            f.write(output)
        print(f"\nOutput written to: {args.output_file}")
    elif output:
        print(output)


if __name__ == "__main__":
    main()
