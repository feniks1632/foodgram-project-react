# Generated by Django 3.2.15 on 2023-09-07 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': (['id'],), 'verbose_name': ('Подписка',), 'verbose_name_plural': ('Подписки',)},
        ),
    ]