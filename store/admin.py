from django.contrib import admin

from .models import Products, Variant

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'color', 'stock', 'category', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant_category', 'variant_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variant_category', 'variant_value')

admin.site.register(Products,ProductAdmin)
admin.site.register(Variant, VariantAdmin)
