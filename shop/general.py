from .models import Categories

def category_data(request):
    data = {
        'categoryData': Categories.objects.filter(parent=None)
    }
    return data
