import stripe
import os
from fastapi import HTTPException
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
from .models import Payment, PaymentStatus  

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("Stripe API key is missing")

payments_db = []

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
        
        payment = Payment(
            payment_id=str(uuid4()),
            amount=amount,
            currency=currency,
            status=PaymentStatus.pending,
        )
        
        payments_db.append(payment)
        
        return session  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_payment_status(payment_id: str, status: PaymentStatus):
    try:
        payment = next((p for p in payments_db if p.payment_id == payment_id), None)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found.")
        
        payment.status = status
        payment.updated_at = datetime.now()  
        
        return payment  
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_payment_status(payment_id: str):
    try:
        payment = next((p for p in payments_db if p.payment_id == payment_id), None)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found.")
        
        return {"payment_id": payment.payment_id, "status": payment.status}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_payment_intent(payment_intent_id: str):
    try:
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def create_payment_intent(amount: int, currency: str):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return intent  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_checkout_session(session_id: str):
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":
            status = PaymentStatus.success
        elif session.payment_status in ["unpaid", "open"]:
            status = PaymentStatus.pending
        else:
            status = PaymentStatus.failed

        return {"session_id": session.id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
