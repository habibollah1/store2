from django.urls import path, include
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, 'product')  # including: product-list | product-detail
router.register('categories', views.CategoryViewSet, basename='category')  # Even if you don't give it a bass-name,
# it will recognize it based on the model
router.register('carts', views.CartViewSet)

# my-website/store/products/27/comments/3
product_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_routers.register('comments', views.CommentViewSet, basename='comments_product')

cart_routers = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_routers.register('items', views.CartItemViewSet, 'cart_items')

urlpatterns = router.urls + product_routers.urls + cart_routers.urls
