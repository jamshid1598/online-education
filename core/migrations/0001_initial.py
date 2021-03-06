# Generated by Django 3.1.1 on 2021-06-11 15:31

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sarlavha')),
                ('title_uz', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sarlavha')),
                ('title_en', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sarlavha')),
                ('title_ru', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sarlavha')),
                ('image', models.ImageField(blank=True, null=True, upload_to='about-us-images/%Y/%m/%d/', verbose_name='Rasm')),
                ('video', models.FileField(blank=True, null=True, upload_to='about-us-videos/%Y/%m/%d/', verbose_name='Video')),
                ('description', models.TextField(verbose_name='Tavsif')),
                ('description_uz', models.TextField(null=True, verbose_name='Tavsif')),
                ('description_en', models.TextField(null=True, verbose_name='Tavsif')),
                ('description_ru', models.TextField(null=True, verbose_name='Tavsif')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan Vaqti')),
            ],
            options={
                'verbose_name_plural': 'Biz haqimizda',
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article/%Y/%m/%d/', verbose_name='Rasm')),
                ('caption', models.CharField(blank=True, max_length=300, null=True, verbose_name='Titr')),
                ('title', models.CharField(max_length=350, unique=True, verbose_name='Sarlavha')),
                ('slug', models.SlugField(max_length=400)),
                ('description', models.TextField(verbose_name='Tavsif')),
                ('author', models.CharField(default='Mehroj', max_length=50, verbose_name='Avtor')),
                ('view_counter', models.PositiveIntegerField(default=0)),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Chiqarilgan sanasi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan sanasi')),
            ],
            options={
                'verbose_name': 'Maqola',
                'verbose_name_plural': 'Maqolalar',
                'ordering': ['published_at', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='PortFolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='portfolio/%Y/%m/%d/', verbose_name='Rasm')),
                ('caption', models.CharField(blank=True, max_length=300, null=True, verbose_name='Titr')),
                ('name', models.CharField(max_length=300, verbose_name='Nomi')),
                ('name_uz', models.CharField(max_length=300, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(max_length=300, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(max_length=300, null=True, verbose_name='Nomi')),
                ('slug', models.SlugField(max_length=320)),
                ('short_info', models.CharField(default='3D model', max_length=500, verbose_name="Qisqa ma'lumot")),
                ('description', models.TextField(verbose_name='Tavsif')),
                ('description_uz', models.TextField(null=True, verbose_name='Tavsif')),
                ('description_en', models.TextField(null=True, verbose_name='Tavsif')),
                ('description_ru', models.TextField(null=True, verbose_name='Tavsif')),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'PortFolio',
                'ordering': ['published_at', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField(blank=True, null=True, unique=True, verbose_name='Video URL')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/', verbose_name='Video Fayl')),
                ('title', models.CharField(max_length=300, verbose_name='Video sarlavhasi')),
                ('title_uz', models.CharField(max_length=300, null=True, verbose_name='Video sarlavhasi')),
                ('title_en', models.CharField(max_length=300, null=True, verbose_name='Video sarlavhasi')),
                ('title_ru', models.CharField(max_length=300, null=True, verbose_name='Video sarlavhasi')),
                ('description', models.TextField(verbose_name='Video tavsifi')),
                ('description_uz', models.TextField(null=True, verbose_name='Video tavsifi')),
                ('description_en', models.TextField(null=True, verbose_name='Video tavsifi')),
                ('description_ru', models.TextField(null=True, verbose_name='Video tavsifi')),
                ('published_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Videolar',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='portfolio-images/%Y/%m/%d/', verbose_name='Rasm')),
                ('caption', models.CharField(blank=True, max_length=300, null=True, verbose_name='Titr:')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_images', to='core.portfolio', verbose_name='3D Model')),
            ],
            options={
                'verbose_name_plural': 'Portfolio rasmlari',
            },
        ),
    ]
