from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.pagination import PageNumberPagination

from .models import Product, Category, Comment
from .paginations import DefaultPagination
from .serializers import ProductSerializers, CategorySerializers, CommentSerializers


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category_id', 'inventory']
    ordering_fields = ['name', 'price', 'inventory', ]
    search_fields = ['name', 'category__title']
    pagination_class = DefaultPagination

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id_parameter = self.request.query_params.get('category_id')
    #     if category_id_parameter is not None:
    #         queryset = queryset.filter(category_id=category_id_parameter)
    #     return queryset

    def get_serializer_context(self):  # صرفا در مواقع استفاده از hyperlink
        return {'request': self.request}

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'there is some order items including this product. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializers

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'there is some products including this category. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
