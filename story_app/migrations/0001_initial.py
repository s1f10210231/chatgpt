# Generated by Django 4.1.2 on 2023-09-13 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NovelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_text', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='novel_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.TextField()),
                ('where', models.TextField()),
                ('when', models.TextField()),
                ('content', models.TextField()),
                ('title', models.TextField()),
                ('like', models.IntegerField(default=0)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='story_app.novelimage')),
            ],
        ),
    ]
