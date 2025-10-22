"""
LLM Judge for evaluating customer support conversations.
Implements the 12-category failure ontology.
"""

from anthropic import Anthropic
import os
import json
from typing import List, Dict


class LLMJudge:
    """Evaluates customer support conversations using structured failure taxonomy."""

    FAILURE_CATEGORIES = [
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

    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    def evaluate_conversation(self, conversation_history: List[Dict], user_goal: str = None) -> Dict:
        """
        Evaluate a complete conversation between user and support agent.

        Args:
            conversation_history: Full conversation transcript
            user_goal: Optional - what the user was trying to accomplish

        Returns:
            Structured evaluation with scores, justifications, and recommendations
        """
        # Format conversation for the judge
        transcript = self._format_transcript(conversation_history)

        # Build evaluation prompt
        prompt = self._build_judge_prompt(transcript, user_goal)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system="You are an expert evaluator assessing AI customer support agent performance.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse the JSON response
            result_text = response.content[0].text

            # Extract JSON from the response
            # Try to find JSON in code blocks first
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()

            evaluation = json.loads(result_text)

            # Add metadata
            evaluation["meta"] = {
                "model": self.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens
            }

            return evaluation

        except Exception as e:
            # Return a fallback evaluation on error
            return {
                "error": str(e),
                "technical_failures": {"score": 5, "justification": "Judge failed to evaluate", "confidence": 0.0},
                "overall_summary": f"Evaluation error: {str(e)}",
                "primary_failure_mode": "Technical - Evaluation system failure",
                "suggestion": "Review evaluation system logs"
            }

    def _format_transcript(self, conversation_history: List[Dict]) -> str:
        """Format conversation history into readable transcript."""
        lines = []
        for msg in conversation_history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            if role == "user":
                lines.append(f"USER: {content}")
            elif role == "assistant":
                lines.append(f"AGENT: {content}")

        return "\n\n".join(lines)

    def _build_judge_prompt(self, transcript: str, user_goal: str = None) -> str:
        """Build the evaluation prompt for the judge."""
        goal_section = f"\nUser's Goal: {user_goal}\n" if user_goal else ""

        return f"""You are an expert evaluator assessing the performance of an AI Customer Support Agent.

            Given the conversation transcript below, evaluate the interaction across the following 12 categories of failure.
            For each category, assign:
            - A **score from 0-5** (0 = perfect, 5 = critical failure)
            - A **short justification** (1-2 sentences)
            - A **confidence level** (0-1)

            Categories:
            1. technical_failures: Downtime, latency, API issues, data quality
            2. comprehension_failures: Intent misclassification, entity extraction, context loss
            3. response_quality_failures: Hallucinations, irrelevant responses, contradictions
            4. knowledge_failures: Knowledge gaps, outdated info, retrieval failures
            5. task_execution_failures: Action failures, workflow errors, authorization issues
            6. interaction_design_failures: Inappropriate tone, cultural insensitivity
            7. safety_compliance_failures: Privacy breaches, security vulnerabilities
            8. escalation_boundary_failures: Over-confidence, premature escalation
            9. user_experience_failures: Frustration amplification, expectation mismatch
            10. business_logic_failures: Policy misapplication, exception handling errors
            11. meta_cognitive_failures: Calibration errors, self-awareness gaps
            12. temporal_failures: State management, timing errors, sequencing failures

            Then, provide:
            1. overall_summary: Brief summary of the conversation quality
            2. primary_failure_mode: The single most significant failure (if any)
            3. suggestion: One actionable improvement recommendation
            {goal_section}
            Return ONLY valid JSON in this exact format (no additional text):

            {{
            "technical_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "comprehension_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "response_quality_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "knowledge_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "task_execution_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "interaction_design_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "safety_compliance_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "escalation_boundary_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "user_experience_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "business_logic_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "meta_cognitive_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "temporal_failures": {{"score": 0, "justification": "...", "confidence": 0.9}},
            "overall_summary": "...",
            "primary_failure_mode": "...",
            "suggestion": "..."
            }}

            [Transcript begins below]

            {transcript}
        """
