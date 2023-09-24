from django import forms
from .models import Novel

class NovelEditForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['ジャンル', '内容', 'タイトル']  # 編集可能なフィールドを指定
