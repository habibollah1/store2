from decimal import Decimal
from django.utils.text import slugify
from rest_framework import serializers
from django.core.validators import MinValueValidator

from store.models import Category, Product, Comment

DOLLARS_TO_RIALS = 900000
PRODUCT_TAX = 1.09


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body', ]

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CategorySerializers(serializers.ModelSerializer):
    # num_of_products = serializers.SerializerMethodField()
    num_of_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'top_product', 'num_of_products']

    # def get_num_of_products(self, category):
    #     return category.products.count()


class ProductSerializers(serializers.ModelSerializer):
    unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tex')
    price_rials = serializers.SerializerMethodField()

    # category = CategorySerializers()
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(),
    #     view_name='category_detail',
    # )
    # price = serializers.DecimalField(max_digits=6, decimal_places=2,
    #                                  validators=[MinValueValidator(0.01)], source='unit_price')
    # inventory = serializers.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'unit_price', 'unit_price_after_tax', 'inventory',
                  'price_rials', ]

    def get_price_rials(self, product):
        return int(product.unit_price * DOLLARS_TO_RIALS)

    def calculate_tex(self, product):
        return round(product.unit_price * Decimal(PRODUCT_TAX), 2)

    def validate(self, data):
        print(data)
        if len(data['name']) < 6:
            raise serializers.ValidationError('Product name length should be more than 6')
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product

    # def update(self, instance, validated_data):
    #     instance.inventory = validated_data.get('inventory')
    #     instance.save()
    #     return instance

# category = serializers.PrimaryKeyRelatedField(
# صرفا میاد تعداد category ها را نمایش میدهد اما تعداد کوئری ها 3تا هستن
#     queryset=Category.objects.all()
# )
# category = serializers.StringRelatedField()
# # برای هر str ی که تعریف کردیم کوئری میزنه پس از select related در views.py استفاده کنم
