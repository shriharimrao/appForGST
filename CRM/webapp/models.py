from django.db import models

# Create your models here.
class gstnum(models.Model):
    gstin=models.CharField(max_length=20)