from django.urls import path, include
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, 'product')  # including: product-list | product-detail
router.register('category', views.CategoryViewSet, basename='category')  # Even if you don't give it a bass-name,
# it will recognize it based on the model

# my-website/store/products/27/comments/3
product_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_routers.register('comments', views.CommentViewSet, basename='comments_product')

urlpatterns = router.urls + product_routers.urls
