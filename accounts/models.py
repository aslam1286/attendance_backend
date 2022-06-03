from tkinter import PhotoImage
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=9)
    mobile_number = models.CharField(max_length=13)

    def __str__(self):
        return self.mobile_number
    
