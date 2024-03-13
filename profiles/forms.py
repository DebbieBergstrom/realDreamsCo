from django import forms
from .models import UserProfile, HealthStatus
from django.utils.translation import gettext_lazy as _


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information. This form allows users to update
    their default information and preferences. It includes fields for
    contact details, address, preferred contact method, and dream center selection.
    """

    class Meta:
        model = UserProfile
        exclude = ("user",)
        widgets = {
            "preferred_dreamcenter": forms.RadioSelect,
            "preferred_contact_method": forms.RadioSelect,
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "placeholder": "YYYY-MM-DD"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        placeholders = {
            "default_phone_number": "Phone Number",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_town_or_city": "Town or City",
            "default_county": "County, State or Locality",
            "default_postcode": "Postal Code",
            "country": "Country",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field in placeholders:
                placeholder = f"{placeholders[field]}"
                if self.fields[field].required:
                    placeholder += " *"
                self.fields[field].widget.attrs["placeholder"] = placeholder
                self.fields[field].widget.attrs["class"] = (
                    "border-black rounded-0 profile-form-input"
                )
                self.fields[field].label = False

        if "country" in self.fields:
            self.fields["country"].widget.attrs["class"] = (
                "border-black rounded-0 profile-form-input"
            )
            self.fields["country"].label = False


class HealthStatusForm(forms.ModelForm):
    """
    Form for updating user health status.
    """

    class Meta:
        model = HealthStatus
        fields = [
            "has_epilepsy",
            "has_heart_conditions",
            "has_mental_illness",
            "suffers_from_ptsd",
            "additional_information",
            "declaration_truthful",
        ]
        widgets = {
            "has_epilepsy": forms.RadioSelect(choices=((False, "No"), (True, "Yes"))),
            "has_heart_conditions": forms.RadioSelect(
                choices=((False, "No"), (True, "Yes"))
            ),
            "has_mental_illness": forms.RadioSelect(
                choices=((False, "No"), (True, "Yes"))
            ),
            "suffers_from_ptsd": forms.RadioSelect(
                choices=((False, "No"), (True, "Yes"))
            ),
            "additional_information": forms.Textarea(attrs={"rows": 2}),
            "declaration_truthful": forms.CheckboxInput(),
        }
        labels = {
            "declaration_truthful": _(
                "I confirm that the information provided is true and accurate to the best of my knowledge."
            )
        }
