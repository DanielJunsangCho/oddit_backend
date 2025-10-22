#!/usr/bin/env python3
"""
Quick example demonstrating the evaluation platform.
Run this after setting up your .env file with ANTHROPIC_API_KEY.
"""

import os
from dotenv import load_dotenv
from orchestrator.simulator import EvaluationOrchestrator
from orchestrator.reporter import EvaluationReporter
from config.scenarios import get_scenario, get_personality

# Load environment
load_dotenv()

def main():
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: Please set ANTHROPIC_API_KEY in .env file")
        return

    print("=" * 80)
    print("AI Customer Support Evaluation Platform - Quick Demo")
    print("=" * 80)
    print()

    # Initialize
    orchestrator = EvaluationOrchestrator()
    reporter = EvaluationReporter()

    # Example 1: Single simulation
    print("Running single simulation: Order delay with frustrated customer\n")

    scenario = get_scenario("order_delay")
    personality = get_personality("frustrated_impatient")

    result = orchestrator.run_single_conversation(
        scenario=scenario,
        personality=personality,
        max_turns=5
    )

    print("\nCONVERSATION TRANSCRIPT:")
    print("-" * 80)
    for msg in result["conversation_history"]:
        role = "USER" if msg["role"] == "user" else "AGENT"
        print(f"\n{role}:")
        print(msg["content"])

    print("\n" + "-" * 80)
    print("\nEVALUATION:")
    print(f"Goal Met: {result['goal_met']}")
    print(f"Turns: {result['turns']}")
    print(f"Summary: {result['evaluation'].get('overall_summary', 'N/A')}")
    print(f"Primary Failure: {result['evaluation'].get('primary_failure_mode', 'N/A')}")
    print(f"Suggestion: {result['evaluation'].get('suggestion', 'N/A')}")

    # Example 2: Small batch (uncomment to run)
    # print("\n\n" + "=" * 80)
    # print("Running 5 simulations...")
    # print("=" * 80)
    #
    # results = orchestrator.run_batch_simulations(num_simulations=5)
    #
    # print("\nGENERATING REPORT...")
    # report = reporter.generate_report(results)
    # print(report)

if __name__ == "__main__":
    main()
