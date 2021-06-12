# Generated by Django 3.1.1 on 2021-06-12 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleModel',
        ),
        migrations.RemoveField(
            model_name='images',
            name='portfolio',
        ),
        migrations.DeleteModel(
            name='VideoModel',
        ),
        migrations.AlterModelOptions(
            name='aboutus',
            options={'ordering': ['pub_date'], 'verbose_name_plural': 'About Us'},
        ),
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.DeleteModel(
            name='PortFolio',
        ),
    ]
