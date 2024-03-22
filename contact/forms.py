from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form for creating contact messages.
    Inherits from Django's ModelForm to utilize the Contact model structure.
    If instantiated by a logged-in user, it pre-fills the email field with
    the user's email.
    """

    class Meta:
        model = Contact
        fields = ["subject", "email", "phone_number", "message"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-control m-0"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control mb-2", "placeholder": "Email Address"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control m-0",
                    "placeholder": "Phone Number (Optional)",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control m-0",
                    "placeholder": "Write Your Message Here",
                    "rows": 2,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ContactForm, self).__init__(*args, **kwargs)

        placeholders = {
            "subject": "Choose Subject",
            "email": "Email Address",
            "phone_number": "Phone Number (Optional)",
            "message": "Write Your Message Here",
        }

        self.fields["subject"].widget.attrs["autofocus"] = True

        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "form-control"

        # Pre-fill the email field if the user is logged in and it's a new instance
        if user and not self.instance.pk:
            self.fields["email"].initial = user.email
