from django.db import models

# Create your models here.
class Novel(models.Model):
    genre = models.TextField()
    where = models.TextField()
    when = models.TextField()
    content = models.TextField()
    title = models.TextField()
    
    def __str__(self):
        return self.genre
    

