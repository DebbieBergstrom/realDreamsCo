from django import forms
from .models import Contact, DreamCenter


class ContactForm(forms.ModelForm):
    """
    Form for creating contact messages.
    Inherits from Django's ModelForm to utilize the Contact model structure.
    If instantiated by a logged-in user, it pre-fills the email field with
    the user's email.
    """

    dream_center = forms.ModelChoiceField(
        queryset=DreamCenter.objects.all(),
        required=False,
        empty_label="Any Center",
        widget=forms.Select(attrs={"class": "form-control text-dark"}),
        label="Select the center you wish to contact",
    )

    class Meta:
        model = Contact
        fields = ["subject", "dream_center", "email", "phone_number", "message"]
        labels = {
            "subject": "Select Subject",
            "dream_center": "Select the center you wish to contact",
        }
        widgets = {
            "subject": forms.Select(attrs={"class": "form-control mb-1 text-dark"}),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control mb-2 text-dark",
                    "placeholder": "Email Address",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control mb-1 text-dark",
                    "placeholder": "Phone Number (Optional)",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control mb-1 text-dark",
                    "placeholder": "Write Your Message Here",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Pre-fill the email field if the user is authenticated
        if user and user.is_authenticated:
            self.fields["email"].initial = user.email

        for field_name in self.fields:
            if field_name not in ["subject", "dream_center"]:
                self.fields[field_name].label = False
