from django.db import models

# Create your models here.

# Defining the Product class which will be used to create object
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # To update everytime
    # use auto_now_add -> to only update when the object is created for the first time 
