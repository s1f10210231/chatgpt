# Generated by Django 4.2.4 on 2023-08-18 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.TextField()),
                ('where', models.TextField()),
                ('when', models.TextField()),
                ('content', models.TextField()),
                ('title', models.TextField()),
            ],
        ),
    ]
