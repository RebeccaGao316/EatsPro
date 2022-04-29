# Generated by Django 3.2.5 on 2022-04-28 05:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0003_auto_20220427_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('status', models.IntegerField(choices=[(1, 'Preparing'), (2, 'Ready'), (3, 'Picked')])),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coreapp.customer')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coreapp.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('fooditem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coreapp.fooditem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_info', to='coreapp.order')),
            ],
        ),
    ]