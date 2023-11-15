# Generated by Django 3.2.21 on 2023-11-15 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0002_novel_created_at'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='liked_novels',
            field=models.ManyToManyField(related_name='liked_by', to='story_app.Novel'),
        ),
    ]