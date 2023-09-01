from django.contrib import admin

# Register your models here.
from . models import Novel

# 管理ツールに登録
admin.site.register(Novel)