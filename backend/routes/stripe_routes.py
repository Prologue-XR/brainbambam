from fastapi import APIRouter, Depends, HTTPException
from models import UserIdentity
from repository.user.get_user_email_by_user_id import get_user_email_by_user_id
import os
import stripe
from auth import AuthBearer, get_current_user

stripe_router = APIRouter()

# Set your secret key: remember to change this to your live secret key in production
stripe.api_key = os.environ.get("STRIPE_API_KEY")

@stripe_router.post("/create-customer", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def create_customer(current_user: UserIdentity = Depends(get_current_user)):
    user_email = get_user_email_by_user_id(str(current_user.id))
    if not user_email:
        raise HTTPException(status_code=404, detail="User email not found")

    customer = stripe.Customer.create(
        email=user_email,
        metadata={"user_id": str(current_user.id)}
    )
    return {"customer_id": customer.id}

@stripe_router.get("/find-customer", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def find_customer(current_user: UserIdentity = Depends(get_current_user)):

    search_results = stripe.Customer.search(query=f"metadata['user_id']:'{str(current_user.id)}'")
    for customer in search_results.auto_paging_iter():
        return customer
    raise HTTPException(status_code=404, detail="Stripe customer not found")

@stripe_router.get("/available-subscriptions", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def list_available_subscriptions(current_user: UserIdentity = Depends(get_current_user)):
    plans = stripe.Plan.list(active=True)
    return {"plans": plans}

@stripe_router.get("/subscription-status", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def check_subscription_status(subscription_id: str, current_user: UserIdentity = Depends(get_current_user)):
    subscription = stripe.Subscription.retrieve(subscription_id)
    if subscription.status == "active":
        # Register user in the subscription
        return {"status": "active", "message": "User is registered in the subscription"}
    else:
        return {"status": subscription.status, "message": "Payment not completed or subscription not active"}
    
@stripe_router.get("/user-subscriptions", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def list_user_subscriptions(current_user: UserIdentity = Depends(get_current_user), show_only_available: bool = False):
    customer = await find_customer(current_user)
    if show_only_available:
        # Show only active subscriptions
        subscriptions = stripe.Subscription.list(customer=customer['id'], status='active')
    else:
        # Show all subscriptions, including inactive and canceled
        subscriptions = stripe.Subscription.list(customer=customer['id'], status='all')
    return {"subscriptions": subscriptions}

@stripe_router.post("/cancel-subscription", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def cancel_subscription(subscription_id: str, current_user: UserIdentity = Depends(get_current_user)):
    subscription = stripe.Subscription.retrieve(subscription_id)
    if subscription.customer != (await find_customer(current_user))['id']:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this subscription")
    canceled_subscription = stripe.Subscription.delete(subscription_id)
    return {"status": canceled_subscription.status, "message": "Subscription canceled successfully"}


@stripe_router.post("/create-payment-link", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def create_payment_link(plan_id: str, current_user: UserIdentity = Depends(get_current_user)):
    # Retrieve the Stripe customer ID for the current user
    customer = await find_customer(current_user)
    if not customer:
        raise HTTPException(status_code=404, detail="Stripe customer not found")

    # Create a checkout session for the given plan and customer
    checkout_session = stripe.checkout.Session.create(
        success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://yourdomain.com/cancel",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": plan_id,  # Assuming plan_id is actually the price ID for the subscription
            "quantity": 1,
        }],
        customer=customer['id']  # Associate the checkout session with the existing customer
    )

    # Return the URL to the frontend
    return {"checkout_url": checkout_session.url}

@stripe_router.post("/update-subscription", dependencies=[Depends(AuthBearer())], tags=["Stripe"])
async def update_subscription(subscription_id: str, new_price_id: str, current_user: UserIdentity = Depends(get_current_user)):
    # Retrieve the subscription to update
    subscription = stripe.Subscription.retrieve(subscription_id)
    if subscription.customer != (await find_customer(current_user))['id']:
        raise HTTPException(status_code=403, detail="Not authorized to update this subscription")

    # Update the subscription with the new price
    updated_subscription = stripe.Subscription.modify(
        subscription_id,
        items=[{"id": subscription["items"]["data"][0]["id"], "price": new_price_id}],
    )
    return {"status": updated_subscription.status, "message": "Subscription updated successfully"}