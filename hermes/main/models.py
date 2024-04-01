from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField()

# additional fields as per your requirement
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comp_name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    openings = models.IntegerField(default=1) 

    
