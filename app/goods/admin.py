from django.contrib import admin

from .models import Categories, Products

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ["name",]

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "amount", "price", "discount"]
    list_editable = ["discount",]
    search_fields = ["name", "description"]
    list_filter = ["discount", "amount", "category"]
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "amount",
    ]