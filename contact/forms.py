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
            "subject": forms.Select(attrs={"class": "form-control mb-1"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control mb-2", "placeholder": "Email Address"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control mb-1",
                    "placeholder": "Phone Number (Optional)",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control mb-1",
                    "placeholder": "Write Your Message Here",
                    "rows": 2,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ContactForm, self).__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields["email"].initial = user.email

        for field_name in self.fields:
            self.fields[field_name].label = False
