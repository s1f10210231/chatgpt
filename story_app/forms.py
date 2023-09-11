from django import forms
from .models import Novel

class NovelEditForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['genre', 'content', 'title']  # 編集可能なフィールドを指定
