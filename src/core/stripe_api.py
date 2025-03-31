from fastapi import APIRouter, HTTPException
from src.core.stripe_service import (
    create_checkout_session,  
    retrieve_payment_intent,  
    create_payment_intent,
    retrieve_checkout_session,  
)

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout(amount: int, currency: str, success_url: str, cancel_url: str):
    session = create_checkout_session(amount, currency, success_url, cancel_url)
    if "error" in session:
        raise HTTPException(status_code=400, detail=session["error"])
    return session

@router.get("/payment-intent/{payment_intent_id}")
async def get_payment_intent(payment_intent_id: str):
    payment_intent = retrieve_payment_intent(payment_intent_id)
    if "error" in payment_intent:
        raise HTTPException(status_code=400, detail=payment_intent["error"])
    return payment_intent

@router.post("/create-payment-intent")
async def create_intent(amount: int, currency: str):
    intent = create_payment_intent(amount, currency)
    if "error" in intent:
        raise HTTPException(status_code=400, detail=intent["error"])
    return intent

@router.get("/payment-status/{session_id}")
async def get_payment_status(session_id: str):
    try:
        session = retrieve_checkout_session(session_id)
        return {"session_id": session.id, "status": session.payment_status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving session: {str(e)}")
