from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    products_count=serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return obj.products.count()

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        total = sum([r.stars for r in reviews])
        return round(total / len(reviews), 1)

class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=255)

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    description = serializers.CharField(required=False, default="No text")
    price = serializers.IntegerField()
    categories = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_categories(self, categories):
        categories_from_db = Category.objects.filter(id__in=categories)
        if len(categories_from_db) != len(categories):
            raise ValidationError("Categories does not exist")
        return categories

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=255)
    product_id = serializers.IntegerField(min_value=1)
    stars = serializers.FloatField(min_value=1, max_value=10)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product does not exist")
        return product_id