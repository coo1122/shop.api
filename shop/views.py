from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (CategorySerializer, CategoryDetailSerializer,
                          ProductSerializer, ProductDetailSerializer, ReviewSerializer, ReviewDetailSerializer,
                          CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
                          )
from django.db import transaction

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request,id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)
    else:
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        shop = Category.objects.all()
        data = CategorySerializer(shop, many=True).data
        return Response(data=data)
    else:
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = serializer.validated_data.get('name')

        with transaction.atomic():
            category = Category.objects.create(
                name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.categories.set(serializer.validated_data.get('categories'))
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(product).data)
    else:
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        shop = Product.objects.all()
        data = ProductSerializer(shop, many=True).data
        return Response(data=data)
    else:
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        categories = serializer.validated_data.get('categories')

        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price)
        product.categories.set(categories)
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.product_id = serializer.validated_data.get('product_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(review).data)
    else:
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        shop = Review.objects.all()
        data = ReviewSerializer(shop, many=True).data
        return Response(data=data)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        product_id = serializer.validated_data.get('product_id')
        stars = serializer.validated_data.get('stars')

        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                product_id=product_id,
                stars=stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer.data)