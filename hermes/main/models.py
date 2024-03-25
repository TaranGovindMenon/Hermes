from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField()


class Company(models.Model):
    comp_name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()

