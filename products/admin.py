from django.contrib import admin
from .models import Product, Category, DreamCenter

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_category_friendly_name',
        'price',
        'size',
        'duration',
        'available',
        'image',
        'created_at',
    )

    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)
    list_filter = ('available', 'category', 'dream_center', 'size',)

    def get_category_friendly_name(self, obj):
        return obj.category.friendly_name if obj.category else '-'
    get_category_friendly_name.short_description = 'Category'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )
    
class DreamCenterAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'location',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DreamCenter, DreamCenterAdmin)


