from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

STARS = [(i, '*' * i) for i in range(1, 6)]

class Review(models.Model):
    text = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True)
    stars = models.IntegerField(default=5, choices=[(i, '*' * i) for i in range(1, 6)])

    def __str__(self):
        return self.text


# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.IntegerField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title