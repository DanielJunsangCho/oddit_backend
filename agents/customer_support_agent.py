"""
Simple Customer Support Agent for Beta/POC purposes.
Naive implementation - just responds to basic customer queries.
"""

from anthropic import Anthropic
import os
from typing import List, Dict


class CustomerSupportAgent:
    """Simple, naive customer support agent."""

    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    def respond(self, conversation_history: List[Dict], user_message: str, user_profile: Dict = None) -> Dict:
        """
        Generate a response to the user's message.

        Args:
            conversation_history: Previous messages in the conversation
            user_message: Current message from the user
            user_profile: Optional user profile information

        Returns:
            Dict with response, actions, and metadata
        """
        # Build system prompt - keep it simple and naive
        system_prompt = """
            You are a customer support agent for an e-commerce company.
            Your job is to help customers with their issues including:
                - Order delays and tracking
                - Refunds and returns
                - Wrong items received
                - Account issues
                - Billing disputes
                - Subscription cancellations

            Be helpful and friendly. Keep responses concise.
        """

        # Build message history for Claude
        messages = []
        for msg in conversation_history:
            if msg.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )

            response_text = response.content[0].text

            return {
                "response": response_text,
                "actions": [],  # Simple agent doesn't take actions
                "meta": {
                    "model": self.model,
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            return {
                "response": f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}",
                "actions": [],
                "meta": {"error": str(e)}
            }
