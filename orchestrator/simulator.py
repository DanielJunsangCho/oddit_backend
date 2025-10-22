"""
Evaluation orchestrator - runs simulations and coordinates agents.
"""

import time
from typing import Dict, List
from agents.customer_support_agent import CustomerSupportAgent
from agents.user_agent import UserAgent
from evaluators.judge import LLMJudge
from config.scenarios import SCENARIOS, PERSONALITIES


class EvaluationOrchestrator:
    """Orchestrates conversations between user agents and customer support agent."""

    def __init__(self, api_key: str = None):
        self.support_agent = CustomerSupportAgent(api_key=api_key)
        self.user_agent = UserAgent(api_key=api_key)
        self.judge = LLMJudge(api_key=api_key)
        self.max_turns = 10  # Maximum conversation turns

    def run_single_conversation(
        self,
        scenario: Dict,
        personality: Dict,
        max_turns: int = None
    ) -> Dict:
        """
        Run a single conversation simulation.

        Args:
            scenario: Scenario definition
            personality: User personality profile
            max_turns: Maximum number of conversation turns (optional)

        Returns:
            Dict with conversation history, evaluation, and metadata
        """
        max_turns = max_turns or self.max_turns
        conversation_history = []
        goal = scenario["goal"]

        # Generate initial user message
        initial_message = self.user_agent.generate_initial_message(personality, scenario)

        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": initial_message
        })

        goal_met = False
        giving_up = False
        turns = 0

        # Conversation loop
        while turns < max_turns and not goal_met and not giving_up:
            # Customer support agent responds
            support_response = self.support_agent.respond(
                conversation_history=conversation_history,
                user_message=initial_message if turns == 0 else conversation_history[-1]["content"],
                user_profile=personality
            )

            # Add agent response to history
            conversation_history.append({
                "role": "assistant",
                "content": support_response["response"]
            })

            # Check if this was the last turn
            if turns >= max_turns - 1:
                break

            # User agent responds
            user_response = self.user_agent.generate_response(
                personality=personality,
                goal=goal,
                conversation_history=conversation_history,
                agent_response=support_response["response"]
            )

            # Add user response to history
            conversation_history.append({
                "role": "user",
                "content": user_response["message"]
            })

            goal_met = user_response["goal_met"]
            giving_up = user_response["giving_up"]
            turns += 1

        # Evaluate the conversation
        evaluation = self.judge.evaluate_conversation(
            conversation_history=conversation_history,
            user_goal=goal
        )

        return {
            "scenario_id": scenario["id"],
            "personality_id": personality["id"],
            "conversation_history": conversation_history,
            "turns": turns,
            "goal_met": goal_met,
            "giving_up": giving_up,
            "evaluation": evaluation,
            "timestamp": time.time()
        }

    def run_batch_simulations(
        self,
        num_simulations: int = 100,
        scenarios: List[Dict] = None,
        personalities: List[Dict] = None
    ) -> List[Dict]:
        """
        Run a batch of simulations with different scenarios and personalities.

        Args:
            num_simulations: Number of simulations to run
            scenarios: List of scenarios (uses defaults if None)
            personalities: List of personalities (uses defaults if None)

        Returns:
            List of simulation results
        """
        import random

        scenarios = scenarios or SCENARIOS
        personalities = personalities or PERSONALITIES

        results = []

        for i in range(num_simulations):
            # Randomly select scenario and personality
            scenario = random.choice(scenarios)
            personality = random.choice(personalities)

            print(f"Running simulation {i+1}/{num_simulations}: {scenario['id']} with {personality['id']}")

            try:
                result = self.run_single_conversation(scenario, personality)
                results.append(result)
            except Exception as e:
                print(f"Error in simulation {i+1}: {str(e)}")
                results.append({
                    "scenario_id": scenario["id"],
                    "personality_id": personality["id"],
                    "error": str(e),
                    "timestamp": time.time()
                })

        return results

    def run_targeted_test(
        self,
        scenario_id: str,
        personality_id: str = None,
        all_personalities: bool = False
    ) -> List[Dict]:
        """
        Run targeted test with specific scenario.

        Args:
            scenario_id: ID of scenario to test
            personality_id: ID of personality to use (optional)
            all_personalities: Test with all personalities (ignores personality_id)

        Returns:
            List of simulation results
        """
        # Find scenario
        scenario = None
        for s in SCENARIOS:
            if s["id"] == scenario_id:
                scenario = s
                break

        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")

        results = []

        if all_personalities:
            # Test with all personalities
            for personality in PERSONALITIES:
                result = self.run_single_conversation(scenario, personality)
                results.append(result)
        else:
            # Test with specific personality
            personality = None
            if personality_id:
                for p in PERSONALITIES:
                    if p["id"] == personality_id:
                        personality = p
                        break
            else:
                personality = PERSONALITIES[0]  # Default to first

            if not personality:
                raise ValueError(f"Personality {personality_id} not found")

            result = self.run_single_conversation(scenario, personality)
            results.append(result)

        return results
