from django.db import models

class NovelImage(models.Model):
    image_text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='novel_images/')


  # 画像をアップロード時にはpillowライブラリが使われるので、pipでインストールする必要あり


# Create your models here.
class Novel(models.Model):
    
    genre = models.TextField()
    where = models.TextField()
    when = models.TextField()
    content = models.TextField()
    title = models.TextField()
    image = models.ForeignKey(NovelImage, on_delete=models.SET_NULL, null=True, blank=True)

  
    def __str__(self):
        return self.genre