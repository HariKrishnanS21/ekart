# Generated by Django 3.2.15 on 2022-10-05 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_cate_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.product')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
    ]