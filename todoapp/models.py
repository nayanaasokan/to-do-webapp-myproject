from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title=models.CharField(max_length=200)
    status_options=(
        ('completed','completed'),
        ('pending','pending')
    )
    status=models.CharField(max_length=200,choices=status_options,default='pending')
    date=models.DateTimeField(auto_now_add=True)
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

