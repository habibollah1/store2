from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product, Category
from .serializers import ProductSerializers, CategorySerializers


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializers

    def get_serializer_context(self):  # صرفا در مواقع استفاده از hyperlink
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializers

    def delete(self, request, *args, **kwargs):
        product = Product.objects.select_related('category')
        if product.order_items.count() > 0:
            return Response({'error': 'there is some order items including this product. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializers


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializers

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'there is some products including this category. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response()
