from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    objects = models.Manager()


class GSTIN(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    gstin_number = models.CharField(max_length=15, unique=True, default=None)
    objects = models.Manager()


class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gstin = models.ForeignKey(GSTIN, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
