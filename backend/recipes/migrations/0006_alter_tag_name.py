# Generated by Django 3.2.15 on 2023-09-07 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_rename_measure_unit_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Тег'),
        ),
    ]