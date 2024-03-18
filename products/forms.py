from django import forms
from .models import Product, Category, DreamCenter
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "image": CustomClearableFileInput,
            "dream_center": forms.CheckboxSelectMultiple,
        }

    size = forms.ChoiceField(
        choices=Product.SIZE_CHOICES,
        initial="S",
        label=Product._meta.get_field("size").verbose_name,
    )
    image = forms.ImageField(
        label=Product._meta.get_field("image").verbose_name, required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields["category"].choices = friendly_names
        self.fields["category"].label = Category._meta.verbose_name
        self.fields["category"].required = True
        self.fields["dream_center"].queryset = DreamCenter.objects.all()
        self.fields["dream_center"].required = True
        self.fields["dream_center"].label = DreamCenter._meta.verbose_name_plural

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded-2"
