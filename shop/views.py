from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (CategorySerializer, CategoryDetailSerializer,
                          ProductSerializer, ProductDetailSerializer, ReviewSerializer, ReviewDetailSerializer
                          )

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
        category.name = request.data.get('name')
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
        name = request.data.get('name')

        category = Category.objects.create(name=name)
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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.categories.set(request.data.get('categories'))
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
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        categories = request.data.get('categories')

        product = Product.objects.create(title=title, description=description, price=price)
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
        review.text = request.data.get('text')
        review.product = request.data.get('product')
        review.stars = request.data.get('stars')
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
        text = request.data.get('text')
        product = request.data.get('product')
        stars = request.data.get('stars')

        review = Review.objects.create(text=text, product=product, stars=stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer.data)