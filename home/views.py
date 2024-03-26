from django.shortcuts import render, redirect
from contact.forms import ContactForm
from django.contrib import messages


def landing_page(request):
    """Render the landing page."""
    return render(request, "home/landing_page.html")


def index(request):
    if request.method == "POST":
        contact_form = ContactForm(
            request.POST, user=request.user if request.user.is_authenticated else None
        )
        if contact_form.is_valid():
            contact_instance = contact_form.save(commit=False)
            if request.user.is_authenticated:
                contact_instance.user = request.user
            contact_instance.save()
            messages.info(request, "Thank you for contacting us!")
            return redirect("home")
    else:
        contact_form = ContactForm(
            user=request.user if request.user.is_authenticated else None
        )

    context = {"contact_form": contact_form}
    return render(request, "home/index.html", context)


def faqs_view(request):
    contact_form = ContactForm(
        request.POST or None,
        user=request.user if request.user.is_authenticated else None,
    )

    if request.method == "POST" and "contact_form" in request.POST:
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect("faqs")

    context = {
        "contact_form": contact_form,
    }

    return render(request, "home/faqs.html", context)
