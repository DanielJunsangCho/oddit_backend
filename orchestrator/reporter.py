"""
Results aggregation and reporting.
"""

import json
from typing import List, Dict
from collections import defaultdict


class EvaluationReporter:
    """Aggregates and reports on evaluation results."""

    def __init__(self):
        self.failure_categories = [
            "technical_failures",
            "comprehension_failures",
            "response_quality_failures",
            "knowledge_failures",
            "task_execution_failures",
            "interaction_design_failures",
            "safety_compliance_failures",
            "escalation_boundary_failures",
            "user_experience_failures",
            "business_logic_failures",
            "meta_cognitive_failures",
            "temporal_failures"
        ]

    def aggregate_results(self, results: List[Dict]) -> Dict:
        """
        Aggregate results from multiple simulations.

        Args:
            results: List of simulation results

        Returns:
            Aggregated statistics and insights
        """
        if not results:
            return {"error": "No results to aggregate"}

        # Filter out error results
        valid_results = [r for r in results if "error" not in r]
        error_results = [r for r in results if "error" in r]

        if not valid_results:
            return {"error": "No valid results to aggregate"}

        # Basic stats
        total_simulations = len(results)
        successful_simulations = len(valid_results)
        failed_simulations = len(error_results)

        # Goal completion stats
        goal_met_count = sum(1 for r in valid_results if r.get("goal_met", False))
        giving_up_count = sum(1 for r in valid_results if r.get("giving_up", False))

        # Average turns
        avg_turns = sum(r.get("turns", 0) for r in valid_results) / len(valid_results) if valid_results else 0

        # Aggregate scores by failure category
        category_scores = defaultdict(list)
        for result in valid_results:
            evaluation = result.get("evaluation", {})
            for category in self.failure_categories:
                if category in evaluation:
                    score = evaluation[category].get("score", 0)
                    category_scores[category].append(score)

        # Calculate average scores and identify problem areas
        avg_category_scores = {}
        for category, scores in category_scores.items():
            avg_category_scores[category] = sum(scores) / len(scores) if scores else 0

        # Identify worst performing categories (highest scores = worst performance)
        worst_categories = sorted(
            avg_category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Aggregate by scenario
        scenario_stats = self._aggregate_by_dimension(valid_results, "scenario_id")

        # Aggregate by personality
        personality_stats = self._aggregate_by_dimension(valid_results, "personality_id")

        # Collect primary failure modes
        failure_mode_counts = defaultdict(int)
        for result in valid_results:
            evaluation = result.get("evaluation", {})
            primary_failure = evaluation.get("primary_failure_mode", "Unknown")
            failure_mode_counts[primary_failure] += 1

        top_failure_modes = sorted(
            failure_mode_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            "summary": {
                "total_simulations": total_simulations,
                "successful_simulations": successful_simulations,
                "failed_simulations": failed_simulations,
                "goal_met_rate": goal_met_count / successful_simulations if successful_simulations > 0 else 0,
                "giving_up_rate": giving_up_count / successful_simulations if successful_simulations > 0 else 0,
                "avg_conversation_turns": round(avg_turns, 2)
            },
            "failure_analysis": {
                "avg_scores_by_category": avg_category_scores,
                "worst_performing_categories": worst_categories,
                "top_failure_modes": top_failure_modes
            },
            "scenario_breakdown": scenario_stats,
            "personality_breakdown": personality_stats
        }

    def _aggregate_by_dimension(self, results: List[Dict], dimension: str) -> Dict:
        """Aggregate results by a specific dimension (scenario_id or personality_id)."""
        dimension_data = defaultdict(lambda: {
            "count": 0,
            "goal_met": 0,
            "avg_turns": 0,
            "avg_total_score": 0
        })

        for result in results:
            key = result.get(dimension, "unknown")
            dimension_data[key]["count"] += 1

            if result.get("goal_met", False):
                dimension_data[key]["goal_met"] += 1

            dimension_data[key]["avg_turns"] += result.get("turns", 0)

            # Calculate total score across all categories
            evaluation = result.get("evaluation", {})
            total_score = 0
            for category in self.failure_categories:
                if category in evaluation:
                    total_score += evaluation[category].get("score", 0)
            dimension_data[key]["avg_total_score"] += total_score

        # Calculate averages
        for key, data in dimension_data.items():
            count = data["count"]
            data["goal_met_rate"] = data["goal_met"] / count if count > 0 else 0
            data["avg_turns"] = round(data["avg_turns"] / count, 2) if count > 0 else 0
            data["avg_total_score"] = round(data["avg_total_score"] / count, 2) if count > 0 else 0
            del data["goal_met"]  # Remove raw count

        return dict(dimension_data)

    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Generate a formatted report from results.

        Args:
            results: List of simulation results
            output_file: Optional file path to save report

        Returns:
            Formatted report as string
        """
        aggregated = self.aggregate_results(results)

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("AI CUSTOMER SUPPORT EVALUATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Summary section
        summary = aggregated.get("summary", {})
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Simulations: {summary.get('total_simulations', 0)}")
        report_lines.append(f"Successful: {summary.get('successful_simulations', 0)}")
        report_lines.append(f"Failed: {summary.get('failed_simulations', 0)}")
        report_lines.append(f"Goal Met Rate: {summary.get('goal_met_rate', 0):.2%}")
        report_lines.append(f"User Gave Up Rate: {summary.get('giving_up_rate', 0):.2%}")
        report_lines.append(f"Avg Conversation Turns: {summary.get('avg_conversation_turns', 0)}")
        report_lines.append("")

        # Failure analysis
        failure_analysis = aggregated.get("failure_analysis", {})
        report_lines.append("FAILURE ANALYSIS")
        report_lines.append("-" * 80)
        report_lines.append("Worst Performing Categories (0=perfect, 5=critical):")
        for category, score in failure_analysis.get("worst_performing_categories", []):
            report_lines.append(f"  {category}: {score:.2f}")
        report_lines.append("")

        report_lines.append("Top Failure Modes:")
        for failure_mode, count in failure_analysis.get("top_failure_modes", []):
            report_lines.append(f"  {failure_mode}: {count} occurrences")
        report_lines.append("")

        # Scenario breakdown
        report_lines.append("SCENARIO BREAKDOWN")
        report_lines.append("-" * 80)
        scenario_breakdown = aggregated.get("scenario_breakdown", {})
        for scenario_id, stats in sorted(scenario_breakdown.items(), key=lambda x: x[1]["avg_total_score"], reverse=True):
            report_lines.append(f"{scenario_id}:")
            report_lines.append(f"  Count: {stats['count']}, Goal Met: {stats['goal_met_rate']:.2%}, Avg Score: {stats['avg_total_score']:.2f}")
        report_lines.append("")

        # Personality breakdown
        report_lines.append("PERSONALITY BREAKDOWN")
        report_lines.append("-" * 80)
        personality_breakdown = aggregated.get("personality_breakdown", {})
        for personality_id, stats in sorted(personality_breakdown.items(), key=lambda x: x[1]["avg_total_score"], reverse=True):
            report_lines.append(f"{personality_id}:")
            report_lines.append(f"  Count: {stats['count']}, Goal Met: {stats['goal_met_rate']:.2%}, Avg Score: {stats['avg_total_score']:.2f}")
        report_lines.append("")

        report_lines.append("=" * 80)

        report = "\n".join(report_lines)

        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)

        return report

    def save_results(self, results: List[Dict], output_file: str):
        """Save raw results to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
