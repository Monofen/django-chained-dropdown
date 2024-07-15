
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('billing/<int:product_id>/', views.billing_page, name='billing_page'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('login/', views.login, name='login'),
    path('login/password/', views.login_password, name='login_password'),
    path('create_password/', views.create_password, name='create_password'),
    path('order-list/', views.order_list, name='order_list'),
    path('signup/', views.signup_view, name='signup'),
]
