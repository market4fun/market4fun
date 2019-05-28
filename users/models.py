from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
# Create your models here.

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):

    cash = models.DecimalField(max_digits=15,decimal_places=2,default=100000)
    objects = CustomUserManager()
