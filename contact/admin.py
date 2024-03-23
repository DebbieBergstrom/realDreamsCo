from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Display the user contact message submitted
    and whether the contact was made by a registered user."""

    list_display = [
        "subject",
        "email",
        "dream_center",
        "user_status",
        "created_at",
        "is_answered",
    ]
    list_editable = ["is_answered"]
    list_filter = [
        "is_answered",
        "created_at",
    ]

    def user_status(self, obj):
        return "Registered" if obj.user else "Not Registered"

    user_status.short_description = "User Status"

    def user_status(self, obj):
        return "Registered" if obj.user else "Not Registered"

    user_status.short_description = "User Status"
