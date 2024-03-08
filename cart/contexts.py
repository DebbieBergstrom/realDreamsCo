from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """
    Compile the contents of the shopping cart, including subtotal for each item, total cost, 
    and consultation fee if applicable. Determines the grand total and the amount needed to 
    reach the free consultation threshold.
    """
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = round(quantity * product.price)
        total += subtotal
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'subtotal': subtotal,
        })

    if total < settings.FREE_CONSULTATION_THRESHOLD:
        consultation = settings.FIXED_CONSULTATION_COST if total + settings.FIXED_CONSULTATION_COST < settings.FREE_CONSULTATION_THRESHOLD else 0
        free_consultation_delta = settings.FREE_CONSULTATION_THRESHOLD - total
    else:
        consultation = 0
        free_consultation_delta = 0

    grand_total = total + consultation

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'consultation': consultation,
        'free_consultation_delta': max(0, free_consultation_delta),  # Ensure it doesn't go negative
        'free_consultation_threshold': settings.FREE_CONSULTATION_THRESHOLD,
        'grand_total': grand_total,
    }

    return context