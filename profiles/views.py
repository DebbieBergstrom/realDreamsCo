from django.shortcuts import render, get_object_or_404
from .models import UserProfile, HealthStatus
from .forms import HealthStatusForm


def profile(request):
    """Display the user's profile and health status."""
    profile = get_object_or_404(UserProfile, user=request.user)
    health_status, created = HealthStatus.objects.get_or_create(user_profile=profile)

    if request.method == "POST":
        form = HealthStatusForm(request.POST, instance=health_status)
        if form.is_valid():
            form.save()
    else:
        form = HealthStatusForm(instance=health_status)

    template = "profiles/profile.html"
    context = {
        "profile": profile,
        "health_status_form": form,
    }

    return render(request, template, context)
