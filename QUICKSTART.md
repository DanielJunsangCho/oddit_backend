# Quick Start Guide

Get up and running with the AI Customer Support Evaluation Platform in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Verify setup:**
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key configured!' if os.getenv('ANTHROPIC_API_KEY') else 'Please set ANTHROPIC_API_KEY in .env')"
   ```

## Run Your First Evaluation

### Option 1: Quick Example Script

Run the example script to see a single simulation:

```bash
python example.py
```

This will:
- Run one conversation simulation (order delay scenario with frustrated customer)
- Show the full conversation transcript
- Display the LLM Judge's evaluation

### Option 2: CLI Tool

**See available scenarios:**
```bash
python run_eval.py list-scenarios
```

**See available personalities:**
```bash
python run_eval.py list-personalities
```

**Run a single test:**
```bash
python run_eval.py single \
  --scenario order_delay \
  --personality frustrated_impatient
```

**Run batch evaluation (10 tests):**
```bash
python run_eval.py batch --num 10
```

### Option 3: REST API

**Start the server:**
```bash
python app.py
```

**Visit interactive docs:**
Open http://localhost:8000/docs in your browser

**Run a simulation via API:**
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "refund_request",
    "personality_id": "calm_polite",
    "max_turns": 10
  }'
```

## What to Expect

### Single Simulation Output

You'll see:
1. **Conversation transcript** - Full dialogue between user and support agent
2. **Evaluation scores** - 12 categories rated 0-5 (0=perfect, 5=critical failure)
3. **Primary failure mode** - Most significant issue identified
4. **Improvement suggestion** - Actionable recommendation

### Batch Simulation Report

For batch runs, you get:
- Success/failure rates
- Goal completion statistics
- Worst performing failure categories
- Top failure modes
- Breakdown by scenario and personality type

## Example Scenarios to Try

**Easy scenarios:**
- `product_inquiry` - Customer asking for recommendations
- `password_reset` - Simple account issue

**Medium difficulty:**
- `order_delay` - Tracking delayed shipment
- `size_exchange` - Exchange wrong size

**Challenging scenarios:**
- `no_order_id` - Customer doesn't have order number
- `billing_dispute` - Duplicate charge investigation
- `policy_complaint` - Unhappy with company policy

## Personality Profiles to Test

**Cooperative:**
- `calm_polite` - Easy to help
- `casual_friendly` - Relaxed conversation

**Difficult:**
- `frustrated_impatient` - Annoyed and rushed
- `angry_demanding` - Hostile and aggressive
- `sarcastic_skeptical` - Distrustful and difficult

**Special cases:**
- `confused_anxious` - Needs extra guidance
- `elderly_patient` - Low tech literacy
- `technical_precise` - Expert user

## Tips for Beta/POC

1. **Start small**: Run single simulations first to understand the system
2. **Compare personalities**: Try same scenario with different personalities
3. **Batch testing**: Use 10-20 simulations for initial insights, 100+ for patterns
4. **Review transcripts**: Read actual conversations to understand failure modes
5. **Iterate**: Use evaluation feedback to improve your support agent

## Common Issues

**"Error: ANTHROPIC_API_KEY not set"**
- Make sure you created `.env` file and added your API key

**Slow performance:**
- Normal - each simulation makes multiple API calls
- Use smaller batch sizes or run asynchronously

**Rate limits:**
- Anthropic has rate limits on API calls
- Add delays between batch simulations if needed

## Next Steps

1. Run example.py to see basic functionality
2. Try different scenario/personality combinations
3. Run small batch (10-20) to see patterns
4. Review the README.md for full documentation
5. Customize scenarios in `config/scenarios.py` for your use case

## Need Help?

- Check README.md for detailed documentation
- Review code comments in source files
- All agents are intentionally simple (naive) for Beta/POC

Enjoy evaluating! 🚀
