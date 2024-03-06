from django.db import models
from django.utils import timezone
from home.models import *

# Create your models here.

class restaurants(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)   
    username = models.CharField(max_length=30)   
    password = models.CharField(max_length=30)       
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default='Y')
    image = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class menu_items(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)   
    calories = models.CharField(max_length=30)
    restaurant = models.ForeignKey("restaurants", on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default='Y')
    image = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class menu(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)   
    restaurant = models.ForeignKey("restaurants", on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default='Y')
    daily_plan_price = models.DecimalField(default=0.0, max_digits=12, decimal_places=6)
    weekly_plan_price = models.DecimalField(default=0.0, max_digits=12, decimal_places=6)
    monthly_plan_price = models.DecimalField(default=0.0, max_digits=12, decimal_places=6)
    image = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class bundle_type(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class bundle(models.Model):
    menu = models.ForeignKey("menu", on_delete=models.CASCADE)
    type = models.ForeignKey("bundle_type", on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey("menu_items", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.menu.name+' - '+self.type.name
    
class orders(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.FloatField(null=True)
    
class order_items(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    item = models.ForeignKey(menu, on_delete=models.CASCADE)
    plan = models.CharField(null=True, max_length=1)
    price = models.FloatField(null=True)