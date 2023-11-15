from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    liked_novels = models.ManyToManyField('story_app.Novel', related_name='liked_by')
    
    def __str__(self):
        return self.username