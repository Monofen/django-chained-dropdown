from .models import Categories, Product

def category_data(request):
    categories = Categories.objects.filter(parent=None)
    return {
        'categoryData': categories,
    }

def product_data(request):
    productData = {category.id: Product.objects.filter(category=category) for category in Categories.objects.all()}
    return {
        'productData': productData,
    }
