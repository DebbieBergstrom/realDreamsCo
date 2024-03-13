from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import UserProfile, HealthStatus
from .forms import UserProfileForm, HealthStatusForm
from checkout.models import Order


def profile(request):
    """Display the user's profile, health status, and order history."""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    orders = user_profile.orders.all()

    if request.method == "POST":
        # Handle profile form submission
        if "submit_profile_form" in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request, "Profile updated successfully", extra_tags="profile-update"
                )
        # Handle health status form submission
        elif "submit_health_status_form" in request.POST:
            health_status, _ = HealthStatus.objects.get_or_create(
                user_profile=user_profile
            )
            health_status_form = HealthStatusForm(request.POST, instance=health_status)
            if health_status_form.is_valid():
                health_status_form.save()
                messages.success(
                    request,
                    "Health status updated successfully",
                    extra_tags="health_status_update",
                )
        return redirect(reverse("profile"))
    else:
        profile_form = UserProfileForm(instance=user_profile)
        health_status, _ = HealthStatus.objects.get_or_create(user_profile=user_profile)
        health_status_form = HealthStatusForm(instance=health_status)

    template = "profiles/profile.html"
    context = {
        "profile_form": profile_form,
        "health_status_form": health_status_form,
        "orders": orders,
        "on_profile_page": True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        (
            f"This is a past confirmation for order number {order_number}. "
            "A confirmation email was sent on the order date."
        ),
    )

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
    }

    return render(request, template, context)
