from django.contrib import admin
from .models import Categories, Product, Order, Customer, ProductImage, ElectronicProduct, Comment
from django.db.models.signals import post_save
from django.dispatch import receiver

# Register your models here
admin.site.register(Customer)
admin.site.register(Comment)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','product','quantity','phone','date','status']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_electronics']
    list_filter = ['parent']
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ElectronicProductInline(admin.StackedInline):
    model = ElectronicProduct
    can_delete = False
    verbose_name_plural = 'Electronic Features'
    fk_name = 'product'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [ProductImageInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.category.is_electronics:
            inline_instances.append(ElectronicProductInline(self.model, self.admin_site))
        return inline_instances


@receiver(post_save, sender=Product)
def create_electronic_product(sender, instance, created, **kwargs):
    if created and instance.category.is_electronics:
        ElectronicProduct.objects.get_or_create(product=instance)
    elif not created and instance.category.is_electronics:
        if not hasattr(instance, 'electronic_features'):
            ElectronicProduct.objects.get_or_create(product=instance)
    elif not instance.category.is_electronics:
        if hasattr(instance, 'electronic_features'):
            instance.electronic_features.delete()
