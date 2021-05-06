from django.db import models

# Create your models here.
class User(models.Model):
    SID=models.CharField(max_length=20,primary_key=True)
    fullname=models.CharField(max_length=40)
    email=models.EmailField(max_length=40)
    password=models.CharField(max_length=40)
    type=models.CharField(max_length=10)
class UserActivity(models.Model):
    SID=models.CharField(max_length=20)
    fullname=models.CharField(max_length=20)
    lastlogin=models.DateTimeField(max_length=20)
    lastlogout=models.DateTimeField(max_length=20)
    count=models.IntegerField()