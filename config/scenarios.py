"""
Scenario templates and personality profiles for simulations.
"""

# Base scenario templates
SCENARIOS = [
    {
        "id": "order_delay",
        "type": "order_delay",
        "context": "Order placed 2 weeks ago, expected delivery was last week, still not received",
        "goal": "Get information about delayed order and resolution",
        "expected_info": ["order_id", "tracking_number", "estimated_delivery"]
    },
    {
        "id": "wrong_item",
        "type": "wrong_item",
        "context": "Received wrong item in package - ordered blue shirt size M, got red pants size L",
        "goal": "Get refund or replacement for wrong item",
        "expected_info": ["order_id", "return_process"]
    },
    {
        "id": "refund_request",
        "type": "refund_request",
        "context": "Product doesn't meet expectations, want to return and get refund",
        "goal": "Initiate refund process",
        "expected_info": ["refund_policy", "return_instructions"]
    },
    {
        "id": "no_order_id",
        "type": "refund_request",
        "context": "Want to return item but can't find order confirmation email",
        "goal": "Get refund without having order ID readily available",
        "expected_info": ["alternative_lookup_method"]
    },
    {
        "id": "account_locked",
        "type": "account_locked",
        "context": "Cannot log into account, getting 'account locked' error",
        "goal": "Regain access to account",
        "expected_info": ["unlock_process", "security_verification"]
    },
    {
        "id": "billing_dispute",
        "type": "billing_dispute",
        "context": "Charged twice for same order, credit card shows duplicate charges",
        "goal": "Get duplicate charge refunded",
        "expected_info": ["charge_investigation", "refund_timeline"]
    },
    {
        "id": "subscription_cancel",
        "type": "subscription_cancellation",
        "context": "Want to cancel monthly subscription but can't find cancellation option",
        "goal": "Cancel subscription successfully",
        "expected_info": ["cancellation_confirmation", "final_billing_date"]
    },
    {
        "id": "warranty_claim",
        "type": "warranty_claim",
        "context": "Product stopped working after 3 months, should be under warranty",
        "goal": "File warranty claim and get replacement or repair",
        "expected_info": ["warranty_coverage", "claim_process"]
    },
    {
        "id": "cross_sell",
        "type": "product_inquiry",
        "context": "Looking for recommendations for compatible accessories",
        "goal": "Get product recommendations",
        "expected_info": ["product_suggestions"]
    },
    {
        "id": "policy_complaint",
        "type": "complaint",
        "context": "Unhappy with return policy - only 14 days seems too short",
        "goal": "Express dissatisfaction and potentially get exception",
        "expected_info": ["policy_explanation", "exception_possibility"]
    },
    {
        "id": "shipping_damage",
        "type": "damaged_item",
        "context": "Package arrived damaged, item inside is broken",
        "goal": "Get replacement or refund for damaged item",
        "expected_info": ["damage_claim_process", "photo_requirements"]
    },
    {
        "id": "promo_code_issue",
        "type": "promo_code",
        "context": "Promo code not applying at checkout, getting error message",
        "goal": "Get promo code to work or receive discount",
        "expected_info": ["promo_validation", "alternative_solution"]
    },
    {
        "id": "size_exchange",
        "type": "exchange",
        "context": "Item doesn't fit, want to exchange for different size",
        "goal": "Exchange item for correct size",
        "expected_info": ["exchange_process", "size_availability"]
    },
    {
        "id": "payment_failed",
        "type": "payment_issue",
        "context": "Order keeps getting declined, payment method should be valid",
        "goal": "Successfully complete purchase",
        "expected_info": ["payment_troubleshooting"]
    },
    {
        "id": "gift_return",
        "type": "gift_return",
        "context": "Received item as gift but want to return, don't have receipt",
        "goal": "Return gift item without receipt",
        "expected_info": ["gift_return_policy", "store_credit_option"]
    },
    {
        "id": "international_shipping",
        "type": "shipping_inquiry",
        "context": "Want to know if you ship to specific country and customs fees",
        "goal": "Get international shipping information",
        "expected_info": ["shipping_availability", "customs_info"]
    },
    {
        "id": "loyalty_points",
        "type": "loyalty_program",
        "context": "Points from recent purchase not showing in account",
        "goal": "Get missing loyalty points credited",
        "expected_info": ["points_investigation", "crediting_timeline"]
    },
    {
        "id": "bulk_order",
        "type": "bulk_inquiry",
        "context": "Want to place large order for company, need bulk pricing",
        "goal": "Get bulk pricing and ordering information",
        "expected_info": ["bulk_discount", "business_account_info"]
    },
    {
        "id": "product_recall",
        "type": "product_recall",
        "context": "Heard about product recall, want to know if my item is affected",
        "goal": "Get recall information and next steps",
        "expected_info": ["recall_status", "return_instructions"]
    },
    {
        "id": "password_reset",
        "type": "password_reset",
        "context": "Forgot password, reset email not arriving",
        "goal": "Reset password and regain account access",
        "expected_info": ["alternative_reset_method", "email_troubleshooting"]
    }
]


# Personality profiles for user agents
PERSONALITIES = [
    # Calm and polite
    {
        "id": "calm_polite",
        "tone": "calm",
        "technical_literacy": "intermediate",
        "formality": "polite",
        "trust_level": "trusting"
    },
    # Frustrated and impatient
    {
        "id": "frustrated_impatient",
        "tone": "frustrated",
        "technical_literacy": "low",
        "formality": "casual",
        "trust_level": "cautious"
    },
    # Angry and demanding
    {
        "id": "angry_demanding",
        "tone": "angry",
        "technical_literacy": "intermediate",
        "formality": "casual",
        "trust_level": "distrustful"
    },
    # Confused and anxious
    {
        "id": "confused_anxious",
        "tone": "anxious",
        "technical_literacy": "low",
        "formality": "polite",
        "trust_level": "cautious"
    },
    # Professional and formal
    {
        "id": "professional_formal",
        "tone": "neutral",
        "technical_literacy": "high",
        "formality": "formal",
        "trust_level": "cautious"
    },
    # Casual and friendly
    {
        "id": "casual_friendly",
        "tone": "friendly",
        "technical_literacy": "intermediate",
        "formality": "casual",
        "trust_level": "trusting"
    },
    # Sarcastic and skeptical
    {
        "id": "sarcastic_skeptical",
        "tone": "sarcastic",
        "technical_literacy": "high",
        "formality": "casual",
        "trust_level": "distrustful"
    },
    # Urgent and stressed
    {
        "id": "urgent_stressed",
        "tone": "urgent",
        "technical_literacy": "intermediate",
        "formality": "casual",
        "trust_level": "neutral"
    },
    # Elderly and patient
    {
        "id": "elderly_patient",
        "tone": "patient",
        "technical_literacy": "low",
        "formality": "formal",
        "trust_level": "trusting"
    },
    # Technical and precise
    {
        "id": "technical_precise",
        "tone": "neutral",
        "technical_literacy": "expert",
        "formality": "formal",
        "trust_level": "neutral"
    }
]


# Perturbations to add noise and variation
PERTURBATIONS = [
    "add_typos",           # Add spelling mistakes
    "add_slang",           # Use informal language
    "mixed_language",      # Mix in words from other languages
    "very_short",          # Use very brief messages
    "very_long",           # Use overly detailed messages
    "missing_details",     # Omit key information
    "contradictory",       # Provide conflicting information
    "irrelevant_info",     # Include unnecessary details
    "all_caps",           # USE ALL CAPS
    "no_punctuation"      # remove all punctuation marks
]


def get_scenario(scenario_id: str):
    """Get scenario by ID."""
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def get_personality(personality_id: str):
    """Get personality by ID."""
    for personality in PERSONALITIES:
        if personality["id"] == personality_id:
            return personality
    return None


def get_random_scenario():
    """Get a random scenario."""
    import random
    return random.choice(SCENARIOS)


def get_random_personality():
    """Get a random personality."""
    import random
    return random.choice(PERSONALITIES)
