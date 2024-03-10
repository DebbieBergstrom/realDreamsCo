from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """
    Compile the contents of the shopping cart, including subtotal for each item, total cost,
    and consultation fee if applicable. Determines the grand total and the amount needed to
    reach the free consultation threshold, or indicates qualification for free consultation.
    """
    cart_items = []
    total = Decimal("0.00")
    product_count = 0
    cart = request.session.get("cart", {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity
        cart_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
                "subtotal": subtotal,
            }
        )

    consultation = settings.FIXED_CONSULTATION_COST
    free_consultation_delta = settings.FREE_CONSULTATION_THRESHOLD - total

    # Logic to account for free consultation qualification
    if total >= settings.FREE_CONSULTATION_THRESHOLD:
        consultation = Decimal("0.00")
        free_consultation_message = "Free consultation earned!"
    else:
        free_consultation_message = (
            f"€{free_consultation_delta} away from a free consultation!"
        )

    grand_total = total + consultation

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "consultation": consultation,
        "free_consultation_message": free_consultation_message,
        "grand_total": grand_total,
        "free_consultation_threshold": settings.FREE_CONSULTATION_THRESHOLD,
    }

    return context
