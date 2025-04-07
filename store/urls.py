from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_list'),
    # path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
]
