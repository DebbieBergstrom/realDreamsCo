from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("home/", views.index, name="home"),
    path("faqs/", views.faqs_view, name="faqs"),
]
