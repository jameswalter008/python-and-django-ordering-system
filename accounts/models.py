from django.db import models
from django.db.models.base import Model, ModelState
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=CASCADE,null=True)#if data for certain user model get deleted it will delete whole row in customer too
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    phno=models.CharField(max_length=200,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=(
        ('indoor',"In Door"),
        ('outdoor',"Out Door")
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,blank=True,choices=category)
    created_at=models.DateTimeField(auto_now_add=True)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    status=(
        ('pending','Pending'),
        ('out for delivery','Out for Delivery'),
        ('delivered','Delievered'),
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)#models.cascade means deleting all related table of customers.SET_NULL means it will onlly set null in related customer table.
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,null=True,choices=status)

    def __str__(self):
        return self.product.name