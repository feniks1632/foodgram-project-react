# Generated by Django 3.2.15 on 2023-09-07 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_description_recipe_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='measure',
            new_name='measure_unit',
        ),
    ]