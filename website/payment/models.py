from django.contrib.auth.models import User
from django.db import models
from pyexpat import model


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

class payment_detail(models.Model):
    stripe_id = models.CharField(max_length=200)
    payment_intent_id = models.CharField(max_length=200)
    payment_status = models.BooleanField(default=False) 

    def __str__(self):
        return self.payment_intent_id

class Paypal_order(models.Model):
    pass
