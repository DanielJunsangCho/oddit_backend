"""
AI Customer Support Evaluation Platform
FastAPI application for running evaluations and simulations.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

from agents.customer_support_agent import CustomerSupportAgent
from agents.user_agent import UserAgent
from evaluators.judge import LLMJudge
from orchestrator.simulator import EvaluationOrchestrator
from orchestrator.reporter import EvaluationReporter
from config.scenarios import SCENARIOS, PERSONALITIES, get_scenario, get_personality

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Customer Support Evaluation Platform",
    description="Platform for evaluating AI customer support agents with red team simulations",
    version="1.0.0"
)

# Initialize components
orchestrator = EvaluationOrchestrator()
reporter = EvaluationReporter()


# API Models
class RespondRequest(BaseModel):
    conversation_history: List[Dict]
    user_message: str
    user_profile: Optional[Dict] = None


class SingleSimulationRequest(BaseModel):
    scenario_id: str
    personality_id: str
    max_turns: Optional[int] = 10


class BatchSimulationRequest(BaseModel):
    num_simulations: int = 100
    scenario_ids: Optional[List[str]] = None
    personality_ids: Optional[List[str]] = None


class EvaluateRequest(BaseModel):
    conversation_history: List[Dict]
    user_goal: Optional[str] = None


# Endpoints
@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Customer Support Evaluation Platform",
        "version": "1.0.0",
        "endpoints": {
            "scenarios": "/scenarios",
            "personalities": "/personalities",
            "simulate": "/simulate",
            "batch_simulate": "/batch_simulate",
            "evaluate": "/evaluate",
            "respond": "/respond"
        }
    }


@app.get("/scenarios")
def list_scenarios():
    """Get list of available scenarios."""
    return {
        "count": len(SCENARIOS),
        "scenarios": SCENARIOS
    }


@app.get("/personalities")
def list_personalities():
    """Get list of available personality profiles."""
    return {
        "count": len(PERSONALITIES),
        "personalities": PERSONALITIES
    }


@app.post("/respond")
def respond(request: RespondRequest):
    """
    Customer support agent responds to user message.
    """
    try:
        support_agent = CustomerSupportAgent()
        response = support_agent.respond(
            conversation_history=request.conversation_history,
            user_message=request.user_message,
            user_profile=request.user_profile
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    """
    Evaluate a conversation using the LLM Judge.
    """
    try:
        judge = LLMJudge()
        evaluation = judge.evaluate_conversation(
            conversation_history=request.conversation_history,
            user_goal=request.user_goal
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate")
def simulate_single(request: SingleSimulationRequest):
    """
    Run a single simulation with specified scenario and personality.
    """
    try:
        scenario = get_scenario(request.scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail=f"Scenario {request.scenario_id} not found")

        personality = get_personality(request.personality_id)
        if not personality:
            raise HTTPException(status_code=404, detail=f"Personality {request.personality_id} not found")

        result = orchestrator.run_single_conversation(
            scenario=scenario,
            personality=personality,
            max_turns=request.max_turns
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch_simulate")
def simulate_batch(request: BatchSimulationRequest):
    """
    Run batch simulations and return aggregated results.
    """
    try:
        # Filter scenarios and personalities if specified
        scenarios = SCENARIOS
        if request.scenario_ids:
            scenarios = [s for s in SCENARIOS if s["id"] in request.scenario_ids]

        personalities = PERSONALITIES
        if request.personality_ids:
            personalities = [p for p in PERSONALITIES if p["id"] in request.personality_ids]

        # Run simulations
        results = orchestrator.run_batch_simulations(
            num_simulations=request.num_simulations,
            scenarios=scenarios,
            personalities=personalities
        )

        # Generate aggregated report
        aggregated = reporter.aggregate_results(results)
        report = reporter.generate_report(results)

        return {
            "results": results,
            "aggregated": aggregated,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "api_key_configured": bool(os.getenv("ANTHROPIC_API_KEY"))}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
