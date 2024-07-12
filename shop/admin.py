from django.contrib import admin
from .models import Categories, Product, Order, Customer

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']
