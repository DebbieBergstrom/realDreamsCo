from django.shortcuts import render

def view_cart(request):
    """A view that render the shopping cart content page."""
    return render(request, 'cart/cart.html')
