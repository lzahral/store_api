from django.db import models

# Create your models here.


class ProductType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
