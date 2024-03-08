from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def view_cart(request):
    """A view that renders the shopping cart content page."""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)
    

def update_cart(request, item_id):
    """Update the quantity of the specified product in the shopping cart"""
    
    # Attempt to get the quantity from the POST data, default to None if not found
    quantity_str = request.POST.get('quantity', None)

    # Check if quantity_str is not None and is a digit, else redirect or handle error
    if quantity_str and quantity_str.isdigit():
        quantity = int(quantity_str)
    else:
        # Handle the case where quantity is not provided or invalid
        # For example, redirect back to the cart with an error message
        # You might want to pass a message to the user indicating the input was invalid
        return redirect('view_cart')  # Adjust the redirect as necessary

    cart = request.session.get('cart', {})
    
    product = get_object_or_404(Product, pk=item_id)

    if quantity > 0:
        cart[str(item_id)] = quantity
    else:
        cart.pop(str(item_id), None)
    
    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """Remove the specified product from the shopping cart"""

    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)

    request.session['cart'] = cart
    return redirect('view_cart')
