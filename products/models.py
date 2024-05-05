from django.db import models

# Create your models here.

from base.models import Basemodel
from django.utils.text import slugify

class Category(Basemodel):
    category_name=models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True,blank=True)
    category_image=models.ImageField(upload_to="categories")

    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.category_name    


class ColorVariant(Basemodel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(Basemodel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name
    
class Product(Basemodel):
    slug = models.SlugField(unique=True, null=True,blank=True)
    product_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="products")
    price=models.IntegerField()
    product_description=models.TextField()
    color_variant = models.ManyToManyField(ColorVariant , blank=True)
    size_variant = models.ManyToManyField(SizeVariant , blank=True)

    def get_product_price_by_size(self,size):
        return self.price + SizeVariant.objects.get(size_name=size).price
    def save(self,*args,**kwargs): # always gets called when object is created.here we modify it
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.product_name   
    
    

class ProductImage(Basemodel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_images")
    image=models.ImageField(upload_to="product")


class Coupon(Basemodel):
    coupon_code=models.CharField(max_length=10)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount= models.IntegerField(default=500)