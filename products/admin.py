from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'get_image','is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
    
    get_image.short_description = 'Product Image'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Product, ProductAdmin)
