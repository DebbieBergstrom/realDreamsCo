from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from cart.contexts import cart_contents
import stripe


def checkout(request):
    """
    Handle the checkout process.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment.")
        return redirect(reverse("products"))

    current_cart = cart_contents(request)
    total = current_cart["grand_total"]
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process payment and complete order
            # Assuming a function `process_payment` exists and returns a success indicator and order instance
            success, order = process_payment(form.cleaned_data, cart)
            if success:
                messages.success(request, "Your order has been successfully processed!")
                # Clear the cart
                request.session["cart"] = {}
                # Redirect to a success page, passing the order number for reference
                return redirect(reverse("checkout_success", args=[order.order_number]))
            else:
                messages.error(
                    request, "There was an issue with your payment. Please try again."
                )
    else:
        form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. \
            Did you forget to set it in your environment?",
        )

    template = "checkout/checkout.html"
    context = {
        "order_form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    A view to handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request, f"Order successfully processed! Your order number is {order_number}."
    )

    context = {
        "order": order,
    }

    return render(request, "checkout/checkout_success.html", context)
