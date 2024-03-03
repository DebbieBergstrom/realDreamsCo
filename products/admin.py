from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_category_friendly_name',
        'price',
        'duration',
        'available',
        'image',
        'created_at',
    )

    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)

    def get_category_friendly_name(self, obj):
        return obj.category.friendly_name if obj.category else '-'
    get_category_friendly_name.short_description = 'Category'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)