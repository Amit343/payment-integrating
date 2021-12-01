

# Create your models here.
from django.db import models

# Create your models here.
class book(models.Model):
    name=models.CharField(max_length=100)
    amount= models.CharField(max_length=100)
    email=models.CharField(max_length=100 ,default=" ")
    payment_id =models.CharField(max_length=100)
    paid= models.BooleanField(default=False)
