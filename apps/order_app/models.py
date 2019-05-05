from django.db import models
from apps.login_reg.models import *

# Create your models here.
class Orders(models.Model):
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, related_name="order", null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Products(models.Model):
    name = models.CharField(max_length = 255)
    quantity = models.IntegerField()
    order = models.ManyToManyField(Orders, related_name="product")