"""
Simple User Agent simulator for Beta/POC purposes.
Naive implementation - simulates customers with different personalities and goals.
"""

from anthropic import Anthropic
import os
from typing import List, Dict


class UserAgent:
    """Simple, naive user agent that simulates a customer."""

    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-haiku-20241022"  # Use faster model for simulation

    def generate_response(
        self,
        personality: Dict,
        goal: str,
        conversation_history: List[Dict],
        agent_response: str
    ) -> Dict:
        """
        Generate the user's next message based on personality and goal.

        Args:
            personality: User personality traits (tone, technical_literacy, formality, etc.)
            goal: What the user is trying to accomplish
            conversation_history: Previous messages
            agent_response: Latest response from customer support agent

        Returns:
            Dict with user's message and whether goal is met
        """
        # Build system prompt based on personality
        tone = personality.get("tone", "neutral")
        tech_literacy = personality.get("technical_literacy", "intermediate")
        formality = personality.get("formality", "neutral")
        trust_level = personality.get("trust_level", "cautious")

        system_prompt = f"""You are simulating a customer in a support conversation.

            Your personality:
                - Tone: {tone}
                - Technical literacy: {tech_literacy}
                - Formality: {formality}
                - Trust level: {trust_level}

            Your goal: {goal}

            Respond naturally as this person would. Keep messages short (1-3 sentences) like a real chat.
            If your goal has been met, say exactly "GOAL_MET" at the end of your message.
            If you're frustrated and want to give up, say exactly "GIVING_UP" at the end.
        """

        # Build message history
        messages = []
        for msg in conversation_history:
            if msg.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Add the agent's latest response
        messages.append({
            "role": "user",
            "content": f"The customer support agent just said: {agent_response}\n\nHow do you respond?"
        })

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=256,
                system=system_prompt,
                messages=messages
            )

            user_message = response.content[0].text

            # Check if goal is met or user is giving up
            goal_met = "GOAL_MET" in user_message
            giving_up = "GIVING_UP" in user_message

            # Clean up the message
            user_message = user_message.replace("GOAL_MET", "").replace("GIVING_UP", "").strip()

            return {
                "message": user_message,
                "goal_met": goal_met,
                "giving_up": giving_up,
                "meta": {
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            return {
                "message": "I need help with my issue.",
                "goal_met": False,
                "giving_up": False,
                "meta": {"error": str(e)}
            }

    def generate_initial_message(self, personality: Dict, scenario: Dict) -> str:
        """
        Generate the user's opening message.

        Args:
            personality: User personality traits
            scenario: Scenario definition with goal and context

        Returns:
            Initial message string
        """
        tone = personality.get("tone", "neutral")
        formality = personality.get("formality", "neutral")
        scenario_type = scenario.get("type", "general")
        context = scenario.get("context", "")

        system_prompt = f"""Generate a customer's opening message for a support chat.

            Scenario: {scenario_type}
            Context: {context}
            Tone: {tone}
            Formality: {formality}

            Generate a realistic opening message (1-2 sentences). Do not include any labels or meta-commentary.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=128,
                system=system_prompt,
                messages=[{"role": "user", "content": "Generate the message:"}]
            )

            return response.content[0].text.strip()
        except Exception as e:
            # Fallback to simple template
            return f"Hi, I need help with {scenario_type}."
