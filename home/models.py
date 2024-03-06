from django.db import models
from django.utils import timezone

# Create your models here.

class users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)   
    contact = models.CharField(max_length=30)   
    address = models.TextField()   
    email = models.CharField(max_length=255)   
    password = models.CharField(max_length=30)       
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1,null=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default='Y')

    def __str__(self):
        return self.first_name
    
class details(models.Model):
    weight = models.FloatField(null=True)
    height_in = models.FloatField(null=True)
    height_feet = models.FloatField(null=True)
    activity_level = models.FloatField(null=True)
    weight_goal = models.CharField(max_length=255,null=True)
    bmi = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bmi