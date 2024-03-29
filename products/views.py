from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def is_superuser(user):
    return user.is_superuser


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)


@login_required
@user_passes_test(is_superuser, login_url="/accounts/login/", redirect_field_name=None)
def add_product(request):
    """Add a product to the front end form"""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added realDream!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(request, "Failed to add item. Check if form is valid.")
    else:
        form = ProductForm()

    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
@user_passes_test(is_superuser, login_url="/accounts/login/", redirect_field_name=None)
def edit_product(request, product_id):
    """Edit a product in the front end form"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated realDream!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(request, "Failed to update item. Check if form is valid.")
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You're now editing {product.name}")

    template = "products/edit_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
@user_passes_test(is_superuser, login_url="/accounts/login/", redirect_field_name=None)
def delete_product(request, product_id):
    """Delete a product in the front end form"""
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "realDream deleted!")
    return redirect(reverse("products"))
