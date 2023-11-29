from django.db import models
from django.utils import timezone

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
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  # 生成された時間を記録するフィールド

  
    def __str__(self):
        return self.genre