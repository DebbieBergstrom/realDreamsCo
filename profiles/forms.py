from django import forms
from .models import UserProfile
from django.utils.translation import gettext_lazy as _


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
        widgets = {
            "preferred_dreamcenter": forms.RadioSelect,
            "preferred_contact_method": forms.RadioSelect,
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

        self.fields["default_country"].widget.attrs["class"] = (
            "border-black rounded-0 profile-form-input"
        )
        self.fields["default_country"].label = False
