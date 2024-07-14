
from django.shortcuts import render, get_object_or_404
from .models import Categories, Product

def index(request):
    categories = Categories.objects.filter(parent=None)
    return render(request, 'test.html', {'categoryData': categories})

def category_view(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})
