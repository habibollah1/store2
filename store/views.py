from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Product, Category
from .serializers import ProductSerializers, CategorySerializers


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products_queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializers(products_queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE', ])
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializers(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializers(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.order_items.count() > 0:
            return Response({'error': 'there is some order items including this product. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# if serializer.is_valid():
# else:
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# return Response('all ok')

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        # category_queryset = Category.objects.prefetch_related('products').all()
        category_queryset = Category.objects.annotate(
            products_count=Count('products')
        ).all()
        serializer = CategorySerializers(category_queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # category_queryset = Category.objects.prefetch_related('products').all()
        serializer = CategorySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# .objects.prefetch_related('category')

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        serializer = CategorySerializers(category)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = CategorySerializers(category.objects.annotate(products_count=Count('products')), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if category.products.count() > 0:
            return Response({'error': 'there is some products including this category. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response()

# product = get_object_or_404(Product, pk=id)
# try: # نتیجه این 4 خط همون بالایی هس
#     product = Product.objects.get(pk=
# except Product.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
