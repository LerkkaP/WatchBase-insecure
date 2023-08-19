from django.db import models

# Create your models here.

class Watch(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.brand
    
    def watch_price(self):
        return self.price
    
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username