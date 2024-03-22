from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.models import User


def contact_view(request):
    """Contact view that handles the ContactForm."""
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_instance = contact_form.save(commit=False)
            if request.user.is_authenticated:
                contact_instance.user = request.user
            contact_instance.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect("home")
    else:
        contact_form = ContactForm()

    context = {
        "contact_form": contact_form,
    }
    return render(request, "contact/contact.html", context)
