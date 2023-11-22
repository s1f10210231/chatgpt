# Generated by Django 3.2.21 on 2023-11-22 06:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='story_app.novelimage')),
            ],
        ),
    ]
