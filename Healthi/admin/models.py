from django.db import models
from django.utils import timezone

# Create your models here.


class admins(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)   
    username = models.CharField(max_length=30)   
    password = models.CharField(max_length=30)       
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, default='Y')
    image = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name
    