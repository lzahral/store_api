from django.db import models
    
    
class ProductCategory(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)


    def __str__(self):
        return self.title



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        ProductCategory, related_name='products', on_delete=models.CASCADE)
    discount_amount = models.IntegerField(default=1)
    only_at_razer = models.BooleanField(default=True)
    gift = models.ForeignKey(
        'self', null=True, blank=True, related_name='gift_for', on_delete=models.SET_NULL)
    fresh_off_the_line = models.BooleanField(default=False)
    final_round_gear = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    

    def __str__(self):
        return f"Image for {self.product.name}"
