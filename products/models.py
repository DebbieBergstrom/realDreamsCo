from django.db import models
from django.utils.text import slugify


class DreamCenter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Dream Centers"

    def __str__(self):
        return f"{self.name} - {self.location}"


class Category(models.Model):
    """
    Model representing various dream product categories.
    """
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name
        

class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    )

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    dream_center = models.ManyToManyField(DreamCenter, related_name='products')
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='S')
    duration = models.IntegerField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
