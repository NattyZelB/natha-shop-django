from django.contrib import admin
from .models import Categories

class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Categories,CategoriesAdmin)
