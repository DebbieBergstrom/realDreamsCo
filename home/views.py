from django.shortcuts import render

def landing_page(request):
    """Render the landing page."""
    return render(request, 'home/landing_page.html')

def index(request):
    """Render the main content page."""
    return render(request, 'home/index.html')
