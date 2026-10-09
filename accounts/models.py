from django.db import models
from django.contrib.auth.models import User
from .regions import REGIONS

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=50, choices=[(r[0], r[1]) for r in REGIONS])

    def __str__(self):
        return f"{self.user.username} - {self.region}"

