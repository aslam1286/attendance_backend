from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    today_date = models.DateTimeField(default=datetime.now)
    from_time = models.TextField(max_length=255)
    to_time = models.TextField(max_length=255)
    total_time = models.TextField(max_length=255)

