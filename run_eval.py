#!/usr/bin/env python3
"""
Command-line interface for running evaluations.
"""

import argparse
import json
import os
from dotenv import load_dotenv

from orchestrator.simulator import EvaluationOrchestrator
from orchestrator.reporter import EvaluationReporter
from config.scenarios import SCENARIOS, PERSONALITIES, get_scenario, get_personality

# Load environment variables
load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Run AI Customer Support Evaluations")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List scenarios
    list_scenarios_parser = subparsers.add_parser("list-scenarios", help="List available scenarios")

    # List personalities
    list_personalities_parser = subparsers.add_parser("list-personalities", help="List available personalities")

    # Run single simulation
    single_parser = subparsers.add_parser("single", help="Run single simulation")
    single_parser.add_argument("--scenario", required=True, help="Scenario ID")
    single_parser.add_argument("--personality", required=True, help="Personality ID")
    single_parser.add_argument("--max-turns", type=int, default=10, help="Maximum conversation turns")
    single_parser.add_argument("--output", help="Output file for results (JSON)")

    # Run batch simulations
    batch_parser = subparsers.add_parser("batch", help="Run batch simulations")
    batch_parser.add_argument("--num", type=int, default=100, help="Number of simulations")
    batch_parser.add_argument("--output", help="Output file for results (JSON)")
    batch_parser.add_argument("--report", help="Output file for report (TXT)")

    # Run targeted test
    targeted_parser = subparsers.add_parser("targeted", help="Run targeted test on specific scenario")
    targeted_parser.add_argument("--scenario", required=True, help="Scenario ID")
    targeted_parser.add_argument("--personality", help="Personality ID (optional)")
    targeted_parser.add_argument("--all-personalities", action="store_true", help="Test with all personalities")
    targeted_parser.add_argument("--output", help="Output file for results (JSON)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in environment")
        print("Please create a .env file with your API key or set the environment variable")
        return

    orchestrator = EvaluationOrchestrator()
    reporter = EvaluationReporter()

    if args.command == "list-scenarios":
        print(f"\nAvailable Scenarios ({len(SCENARIOS)}):\n")
        for scenario in SCENARIOS:
            print(f"  {scenario['id']}: {scenario['type']}")
            print(f"    Goal: {scenario['goal']}")
            print()

    elif args.command == "list-personalities":
        print(f"\nAvailable Personalities ({len(PERSONALITIES)}):\n")
        for personality in PERSONALITIES:
            print(f"  {personality['id']}:")
            print(f"    Tone: {personality['tone']}, Tech: {personality['technical_literacy']}")
            print(f"    Formality: {personality['formality']}, Trust: {personality['trust_level']}")
            print()

    elif args.command == "single":
        scenario = get_scenario(args.scenario)
        if not scenario:
            print(f"Error: Scenario '{args.scenario}' not found")
            return

        personality = get_personality(args.personality)
        if not personality:
            print(f"Error: Personality '{args.personality}' not found")
            return

        print(f"\nRunning simulation: {args.scenario} with {args.personality}")
        print(f"Goal: {scenario['goal']}\n")

        result = orchestrator.run_single_conversation(
            scenario=scenario,
            personality=personality,
            max_turns=args.max_turns
        )

        print("\n" + "=" * 80)
        print("CONVERSATION TRANSCRIPT")
        print("=" * 80 + "\n")

        for i, msg in enumerate(result["conversation_history"]):
            role = "USER" if msg["role"] == "user" else "AGENT"
            print(f"{role}: {msg['content']}\n")

        print("=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80 + "\n")

        evaluation = result["evaluation"]
        print(f"Overall Summary: {evaluation.get('overall_summary', 'N/A')}")
        print(f"Primary Failure Mode: {evaluation.get('primary_failure_mode', 'N/A')}")
        print(f"Suggestion: {evaluation.get('suggestion', 'N/A')}")
        print(f"\nGoal Met: {result['goal_met']}")
        print(f"Turns: {result['turns']}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to {args.output}")

    elif args.command == "batch":
        print(f"\nRunning {args.num} simulations...\n")

        results = orchestrator.run_batch_simulations(num_simulations=args.num)

        print("\nGenerating report...\n")
        report = reporter.generate_report(results)
        print(report)

        if args.output:
            reporter.save_results(results, args.output)
            print(f"\nResults saved to {args.output}")

        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")

    elif args.command == "targeted":
        scenario = get_scenario(args.scenario)
        if not scenario:
            print(f"Error: Scenario '{args.scenario}' not found")
            return

        if args.all_personalities:
            print(f"\nRunning targeted test: {args.scenario} with ALL personalities\n")
            results = orchestrator.run_targeted_test(
                scenario_id=args.scenario,
                all_personalities=True
            )
        else:
            personality_id = args.personality or PERSONALITIES[0]["id"]
            print(f"\nRunning targeted test: {args.scenario} with {personality_id}\n")
            results = orchestrator.run_targeted_test(
                scenario_id=args.scenario,
                personality_id=personality_id
            )

        print("\nGenerating report...\n")
        report = reporter.generate_report(results)
        print(report)

        if args.output:
            reporter.save_results(results, args.output)
            print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
