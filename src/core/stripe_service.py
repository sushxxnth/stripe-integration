import stripe
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("Stripe API key is missing")

def create_checkout_session(amount: int, currency: str, success_url: str, cancel_url: str):

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": "Custom Payment"},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session  # Return full session details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_payment_intent(payment_intent_id: str):
    """Retrieves a Stripe PaymentIntent."""
    try:
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def create_payment_intent(amount: int, currency: str):
    """Creates a Stripe PaymentIntent."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return intent  # Return full PaymentIntent details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
