from decimal import Decimal
from django.conf import settings

def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_CONSULTATION_THRESHOLD:
        consultation = total * Decimal(settings.STANDARD_CONSULTATION_PERCENTAGE / 100)
        free_consultation_delta = settings.FREE_CONSULTATION_THRESHOLD - total
    else:
        consultation = 0
        free_consultation_delta = 0
    
    grand_total = consultation + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'consultation': consultation,
        'free_consultation_delta': free_consultation_delta,
        'free_consultation_threshold': settings.FREE_CONSULTATION_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
