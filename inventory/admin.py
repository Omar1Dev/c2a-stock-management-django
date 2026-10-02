from django.contrib import admin

from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "current_quantity",
        "unit_price",
        "status",
    )

    search_fields = (
        "name",
        "category",
    )