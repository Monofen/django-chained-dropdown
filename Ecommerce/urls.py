from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Shop menu'
admin.site.site_title = 'Shop menu'
admin.site.index_title = 'Shop Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
