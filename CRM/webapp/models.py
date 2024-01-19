
from django.db import models

class User(models.Model):
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name
