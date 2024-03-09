from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """
    Handle the checkout process.
    """
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment.")
        return redirect(reverse("products"))

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

    template = "checkout/checkout.html"
    context = {
        "order_form": form,
        "stripe_public_key": "stripe_public_key",
        "client_secret": "test client secret",
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
