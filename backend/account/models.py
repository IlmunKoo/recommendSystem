from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

      id=models.AutoField(primary_key=True)
      email=models.EmailField(max_length=100)

