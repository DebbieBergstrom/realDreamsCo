from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """A view that renders the shopping cart content page."""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['cart'] = cart
    request.session.save()
    return redirect(redirect_url)


def update_cart(request, item_id):
    """Update the quantity of the specified product in the shopping cart."""
    try:
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, pk=item_id)

        if quantity in range(1, 10):  # Ensures the quantity is within 1-9
            cart[str(item_id)] = quantity
            messages.success(request, f"Updated quantity for {product.name}.")
        else:
            messages.error(request, "Invalid quantity. Please enter a number between 1 and 9.")

        request.session['cart'] = cart
    except ValueError:
        messages.error(request, "Invalid input. Please enter a valid number.")

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """Remove the specified product from the shopping cart."""
    try:
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            product = get_object_or_404(Product, pk=item_id)  # Fetch the product before removing it
            cart.pop(str(item_id), None)
            request.session['cart'] = cart
            messages.success(request, f"{product.name} has been removed from your cart.")
        else:
            messages.error(request, "The item was not found in your cart.")
    except KeyError:
        messages.error(request, "There was an error removing the item from your cart.")
        return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

    return redirect('view_cart')

