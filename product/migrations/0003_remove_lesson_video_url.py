# Generated by Django 3.1.1 on 2021-06-12 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210612_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='video_url',
        ),
    ]
