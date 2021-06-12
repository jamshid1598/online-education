# Generated by Django 3.1.1 on 2021-06-11 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False, verbose_name='Bajarildi')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Buyurtma sanasi')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.customer')),
            ],
            options={
                'verbose_name': 'Buyurtma',
                'verbose_name_plural': 'Buyurtmalar',
            },
        ),
        migrations.CreateModel(
            name='OrderSingleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_single_item', to='cart.customer')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Order Date')),
                ('cart_field', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered_lesson', to='product.lesson', verbose_name='Lesson')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Lesson',
                'verbose_name_plural': 'Order Lesson',
            },
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=300, null=True, verbose_name='Model')),
                ('image', models.ImageField(blank=True, null=True, upload_to='ordered-product/%Y/%m/%d/', verbose_name='Rasm')),
                ('model_quantity', models.IntegerField(default=0, verbose_name='Model miqdori')),
                ('single_price', models.FloatField(default=0, verbose_name='Narxi')),
                ('total_price', models.FloatField(default=0, verbose_name='Umumiy narx')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Yuklangan sanasi')),
                ('completed', models.BooleanField(default=False, verbose_name='Bajarildi')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to='cart.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Buyurtma modellar',
                'verbose_name_plural': 'Buyurtma modellar',
                'ordering': ['-date_ordered'],
            },
        ),
    ]
