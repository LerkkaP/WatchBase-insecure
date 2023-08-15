from django.db import models

# Create your models here.

class Watch(models.Model):
    brand = models.CharField(max_length=200)
    price = models.IntegerField()
    model = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.brand
    
    def watch_price(self):
        return self.price