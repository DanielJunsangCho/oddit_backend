# AI Customer Support Evaluation Platform

A comprehensive platform for evaluating AI customer support agents using red team simulations and LLM-based judging.

## Overview

This platform simulates 100+ diverse user agents that interact with an AI customer support agent to test its robustness, reliability, and performance across various scenarios. Each interaction is evaluated by an LLM Judge using a 12-category failure ontology.

## Features

- **20 Scenario Templates**: Order delays, refunds, billing disputes, account issues, and more
- **10 Personality Profiles**: Diverse user personalities (frustrated, calm, technical, confused, etc.)
- **12-Category Failure Ontology**: Comprehensive evaluation across technical, comprehension, response quality, safety, and more
- **Simple Naive Agents**: Customer support and user agents kept intentionally simple for Beta/POC
- **Automated Simulations**: Run single or batch simulations with aggregated reporting
- **REST API**: FastAPI-based API for programmatic access
- **CLI Tool**: Command-line interface for quick evaluations

## Project Structure

```
oddit_backend/
├── agents/
│   ├── customer_support_agent.py  # Simple customer support agent
│   └── user_agent.py              # User simulator agent
├── evaluators/
│   └── judge.py                   # LLM Judge with 12-category ontology
├── orchestrator/
│   ├── simulator.py               # Conversation orchestrator
│   └── reporter.py                # Results aggregation and reporting
├── config/
│   └── scenarios.py               # 20 scenarios + 10 personalities
├── app.py                         # FastAPI application
├── run_eval.py                    # CLI tool
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## Installation

1. Clone the repository:
```bash
cd /Users/juncho/Desktop/oddit_backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### CLI Tool

The CLI provides an easy way to run evaluations from the command line.

**List available scenarios:**
```bash
python run_eval.py list-scenarios
```

**List available personalities:**
```bash
python run_eval.py list-personalities
```

**Run a single simulation:**
```bash
python run_eval.py single --scenario order_delay --personality frustrated_impatient
```

**Run batch simulations:**
```bash
python run_eval.py batch --num 100 --report report.txt --output results.json
```

**Run targeted test (one scenario, all personalities):**
```bash
python run_eval.py targeted --scenario refund_request --all-personalities
```

### REST API

Start the FastAPI server:
```bash
python app.py
```

Or with uvicorn:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

**Example API calls:**

Get available scenarios:
```bash
curl http://localhost:8000/scenarios
```

Run a single simulation:
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "order_delay",
    "personality_id": "frustrated_impatient",
    "max_turns": 10
  }'
```

Run batch simulations:
```bash
curl -X POST http://localhost:8000/batch_simulate \
  -H "Content-Type: application/json" \
  -d '{
    "num_simulations": 50
  }'
```

## 12-Category Failure Ontology

The LLM Judge evaluates conversations across these categories:

1. **Technical Failures**: Downtime, latency, API issues
2. **Comprehension Failures**: Intent misclassification, entity extraction errors
3. **Response Quality Failures**: Hallucinations, irrelevant responses
4. **Knowledge Failures**: Knowledge gaps, outdated information
5. **Task Execution Failures**: Action failures, workflow errors
6. **Interaction Design Failures**: Inappropriate tone, cultural insensitivity
7. **Safety & Compliance Failures**: Privacy breaches, security vulnerabilities
8. **Escalation & Boundary Failures**: Over-confidence, premature escalation
9. **User Experience Failures**: Frustration amplification, expectation mismatch
10. **Business Logic Failures**: Policy misapplication, exception handling
11. **Meta-Cognitive Failures**: Calibration errors, self-awareness gaps
12. **Temporal Failures**: State management, timing errors

Each category is scored 0-5 (0=perfect, 5=critical failure) with justification and confidence level.

## Scenarios

20 pre-configured scenarios covering common customer support interactions:

- Order delay
- Wrong item received
- Refund request
- Missing order ID
- Account locked
- Billing dispute
- Subscription cancellation
- Warranty claim
- Product inquiry
- Policy complaint
- Shipping damage
- Promo code issue
- Size exchange
- Payment failed
- Gift return
- International shipping
- Loyalty points
- Bulk order
- Product recall
- Password reset

## Personality Profiles

10 diverse user personalities to stress-test the support agent:

- Calm & Polite
- Frustrated & Impatient
- Angry & Demanding
- Confused & Anxious
- Professional & Formal
- Casual & Friendly
- Sarcastic & Skeptical
- Urgent & Stressed
- Elderly & Patient
- Technical & Precise

## Architecture

### Customer Support Agent (Simple & Naive)
- Uses Claude 3.5 Sonnet
- Basic system prompt with common e-commerce support scenarios
- No RAG, no tool use, no complex logic
- Just responds to customer messages conversationally

### User Agent (Simple & Naive)
- Uses Claude 3.5 Haiku (faster)
- Simulates customer based on personality profile
- Tracks goal completion
- Generates realistic chat messages

### LLM Judge
- Uses Claude 3.5 Sonnet
- Evaluates full conversation transcripts
- Returns structured JSON with scores, justifications, and suggestions
- Implements 12-category failure ontology

### Orchestrator
- Manages conversation loop between user and support agent
- Runs single or batch simulations
- Handles timeouts and error cases

### Reporter
- Aggregates results across multiple simulations
- Identifies patterns by scenario and personality
- Generates human-readable reports

## Example Output

```
================================================================================
AI CUSTOMER SUPPORT EVALUATION REPORT
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Total Simulations: 100
Successful: 98
Failed: 2
Goal Met Rate: 67.35%
User Gave Up Rate: 12.24%
Avg Conversation Turns: 5.23

FAILURE ANALYSIS
--------------------------------------------------------------------------------
Worst Performing Categories (0=perfect, 5=critical):
  task_execution_failures: 2.34
  knowledge_failures: 1.89
  comprehension_failures: 1.45
  business_logic_failures: 1.23
  user_experience_failures: 0.98

Top Failure Modes:
  Knowledge Failures - Missing product information: 23 occurrences
  Task Execution - Unable to process refund: 18 occurrences
  Comprehension - Missing order ID context: 15 occurrences
  ...
```

## Development Notes

This is a **Beta/POC implementation** with intentionally simple agents:

- Customer support agent has no RAG, tools, or advanced capabilities
- User agent uses basic prompting without sophisticated behavior modeling
- No database or persistence layer
- No authentication or rate limiting
- Synchronous processing only

For production use, consider:
- Adding RAG for knowledge retrieval
- Implementing tool use for actions (refunds, cancellations, etc.)
- Adding conversation memory and state management
- Using async processing for batch simulations
- Adding database for results persistence
- Implementing more sophisticated user behavior models
- Adding perturbations (typos, mixed language, etc.)

## License

MIT

## Contributing

This is a POC implementation. Feel free to extend and improve!
