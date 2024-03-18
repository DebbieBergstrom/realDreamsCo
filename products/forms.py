from django import forms
from .models import Product, Category, DreamCenter


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("slug",)
        widgets = {
            "dream_center": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Categories with friendly names
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields["category"].choices = friendly_names

        # Dream Centers
        dream_centers = DreamCenter.objects.all()
        self.fields["dream_center"].queryset = dream_centers
        self.fields["dream_center"].label = DreamCenter._meta.verbose_name_plural
        self.fields["dream_center"].required = True

        # Adds a class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded-2"
