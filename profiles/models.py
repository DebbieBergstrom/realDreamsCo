from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information, order history, and additional preferences.
    """

    DREAMCENTER_CHOICES = [
        ("STOCKHOLM", "Stockholm"),
        ("BERLIN", "Berlin"),
        ("PARIS", "Paris"),
    ]

    CONTACT_METHOD_CHOICES = [
        ("EMAIL", "Email"),
        ("PHONE", "Phone"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_METHOD_CHOICES,
        default="EMAIL",
        null=True,
        blank=False,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_dreamcenter = models.CharField(
        max_length=20,
        choices=DREAMCENTER_CHOICES,
        default="STOCKHOLM",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class HealthStatus(models.Model):
    user_profile = models.OneToOneField(
        "UserProfile", on_delete=models.CASCADE, related_name="health_status"
    )
    has_epilepsy = models.BooleanField(_("Do you have epilepsy?"), default=False)
    has_heart_conditions = models.BooleanField(
        _("Do you have any heart conditions?"), default=False
    )
    has_mental_illness = models.BooleanField(
        _("Do you have any mental illnesses?"), default=False
    )
    suffers_from_ptsd = models.BooleanField(
        _("Do you suffer from PTSD?"), default=False
    )
    additional_information = models.TextField(
        _("Anything else we need to know prior a realDream session?"), blank=True
    )
    last_updated = models.DateTimeField(_("Last Updated"), auto_now_add=True)
    declaration_truthful = models.BooleanField(
        _(
            "I confirm that the information provided is true and accurate to the best of my knowledge."
        ),
        default=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Health Status")
        verbose_name_plural = _("Health Status Declarations")

    def __str__(self):
        return f"Health Status Declaration of {self.user_profile.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile, and create a health status profile if not already existing.
    """
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        HealthStatus.objects.create(user_profile=user_profile)
    else:
        instance.userprofile.save()
        # Update health status, or create if it doesn't exist
        HealthStatus.objects.get_or_create(user_profile=instance.userprofile)
