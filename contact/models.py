from django.conf import settings
from django.db import models
from products.models import DreamCenter


class Contact(models.Model):
    SUBJECT_CHOICES = [
        ("purchase", "Purchase"),
        ("experience", "realDreams Experience"),
        ("health", "Health Status Concerns"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    dream_center = models.ForeignKey(
        DreamCenter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Dream Center",
    )
    is_answered = models.BooleanField(default=False, verbose_name="Answered?")
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default="other")
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_subject_display()} by {self.email}"
