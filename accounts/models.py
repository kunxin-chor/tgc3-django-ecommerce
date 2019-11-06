from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    job_title = models.CharField(max_length=50, blank=False)
    
