import stripe
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout():

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "VIP Betting Signals"
                },
                "unit_amount": 1500
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel"
    )

    return session.url