# Generated by Django 2.2.16 on 2020-10-09 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20201008_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientproduct',
            name='stock',
            field=models.PositiveIntegerField(default=1, verbose_name='Cantidad en inventario'),
        ),
    ]
