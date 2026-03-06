import stripe

stripe.api_key = "YOUR_STRIPE_SECRET"

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