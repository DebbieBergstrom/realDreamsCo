from django.shortcuts import render, redirect
from contact.forms import ContactForm
from django.contrib import messages


def landing_page(request):
    """Render the landing page."""
    return render(request, "home/landing_page.html")


from django.shortcuts import render, redirect
from contact.forms import ContactForm
from django.contrib import messages


def index(request):
    contact_form = ContactForm(
        request.POST or None,
        user=request.user if request.user.is_authenticated else None,
    )

    if request.method == "POST":
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect("home")

    context = {
        "contact_form": contact_form,
    }
    return render(request, "home/index.html", context)
