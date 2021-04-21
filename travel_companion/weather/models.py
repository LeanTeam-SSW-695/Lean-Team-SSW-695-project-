from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    usersname = models.ForeignKey(User, on_delete=models.CASCADE)